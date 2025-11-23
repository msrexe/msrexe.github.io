---
layout: post
title: "BPF Günlükleri: Packet Counter'dan Trafik Analizine – BPF CO-RE ile Gelişmiş Uygulamalar"
description: "Bu yazıda, eBPF CO-RE desteği ile taşınabilir bir trafik analiz uygulaması geliştireceğiz."
image: assets/images/bpf-core-network-analysis.png
category: linux
slug: bpf-core-ile-trafik-analizi
author: msrexe
lang: tr
---

![Image](assets/images/bpf-core-network-analysis.png)

Bir önceki yazıda, eBPF mimarisini kullanarak temel bir **packet counter** uygulaması geliştirmiştik. Ancak klasik yöntemle yazılmış bu eBPF programları, kernel versiyonlarına göre farklılık gösteren `linux/bpf.h` gibi bağımlılıklara sahipti. Bu da taşınabilirliği oldukça azaltıyor ve farklı linux çekirdeklerinde kernellarında çalıştırmayı zorlaştırıyordu.

İşte bu yazıda, **CO-RE (Compile Once – Run Everywhere)** özelliğini kullanarak farklı sistemlerde çalışabilen bir trafik analiz uygulaması yazacağız. Hedefimiz gelen paketlerin kaynak IP adreslerine göre sınıflandırılması ve yoğunluk analizi olacak.

---

## Gereksinimler

- Linux 5.8+ (BTF desteği için)
- `bpftool` (vmlinux.h üretimi için)
- Clang & LLVM (11+)
- Go
- [libbpf](https://github.com/libbpf/libbpf)
- [cilium/ebpf](https://github.com/cilium/ebpf)

---

## 1. BPF CO-RE Nedir?

**CO-RE**, eBPF programlarını bir kere derleyip farklı Linux çekirdek sürümlerinde çalıştırmamıza olanak tanır. Bunu çekirdeğin kendi tür tanımlarına erişerek (`BTF`) yapar. Bu şekilde `linux/bpf.h` gibi dış bağımlılıklardan kurtuluruz.

---

## 2. C ile eBPF Programı: IP Sayaç

`ip_counter.bpf.c` dosyasını aşağıdaki gibi oluşturun:

```c
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

char LICENSE[] SEC("license") = "Dual MIT/GPL";

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);
    __type(value, __u64);
    __uint(max_entries, 1024);
} ip_count SEC(".maps");

SEC("xdp")
int count_src_ips(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data     = (void *)(long)ctx->data;

    struct ethhdr *eth = data;
    if ((void*)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto != __bpf_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *iph = (void*)(eth + 1);
    if ((void*)(iph + 1) > data_end)
        return XDP_PASS;

    __u32 src_ip = bpf_ntohl(iph->saddr);

    __u64 *count = bpf_map_lookup_elem(&ip_count, &src_ip);
    if (count)
        __sync_fetch_and_add(count, 1);
    else {
        __u64 init_val = 1;
        bpf_map_update_elem(&ip_count, &src_ip, &init_val, BPF_ANY);
    }

    return XDP_PASS;
}
```

> `vmlinux.h` dosyasını şu komutla oluşturabilirsiniz:
```sh
> `bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h`
```

---

## 3. Go ile kernel’a yükleme ve izleme

`main.go` dosyasını şu şekilde yazalım:

```go
package main

import (
    "encoding/binary"
    "fmt"
    "log"
    "net"
    "os"
    "os/signal"
    "time"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
    "github.com/cilium/ebpf/rlimit"
)

func ipToStr(ip uint32) string {
    bytes := make([]byte, 4)
    binary.BigEndian.PutUint32(bytes, ip)
    return net.IP(bytes).String()
}

func main() {
    if err := rlimit.RemoveMemlock(); err != nil {
        log.Fatalf("Removing memlock: %v", err)
    }

    spec, err := ebpf.LoadCollectionSpec("ip_counter.bpf.o")
    if err != nil {
        log.Fatalf("Loading collection spec: %v", err)
    }

    objs := struct {
        Program  *ebpf.Program `ebpf:"count_src_ips"`
        IpCount  *ebpf.Map     `ebpf:"ip_count"`
    }{}

    if err := spec.LoadAndAssign(&objs, nil); err != nil {
        log.Fatalf("Loading and assigning: %v", err)
    }
    defer objs.Program.Close()
    defer objs.IpCount.Close()

    ifaceName := "eth0"
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        log.Fatalf("Getting interface %s: %v", ifaceName, err)
    }

    l, err := link.AttachXDP(link.XDPOptions{
        Program:   objs.Program,
        Interface: iface.Index,
    })
    if err != nil {
        log.Fatalf("Attaching XDP: %v", err)
    }
    defer l.Close()

    log.Printf("Tracking source IPs on %s...", ifaceName)

    ticker := time.NewTicker(2 * time.Second)
    stop := make(chan os.Signal, 1)
    signal.Notify(stop, os.Interrupt)

    for {
        select {
        case <-ticker.C:
            var ip uint32
            var count uint64
            iter := objs.IpCount.Iterate()
            fmt.Println("Top Source IPs:")
            for iter.Next(&ip, &count) {
                fmt.Printf("  %s => %d packets\n", ipToStr(ip), count)
            }
            if err := iter.Err(); err != nil {
                log.Printf("Error iterating map: %v", err)
            }
        case <-stop:
            log.Println("Exiting..")
            return
        }
    }
}
```

---

## 4. Derleme ve Çalıştırma

### C Kodunu Derleme

```sh
clang -O2 -g -target bpf -D__TARGET_ARCH_x86 -I. -c ip_counter.bpf.c -o ip_counter.bpf.o
```

> `-I.` parametresi ile bulunduğunuz klasördeki `vmlinux.h` dosyasını da eklemeyi unutmayın.

### Go kodunu çalıştırma

```sh
go mod init ip-analyzer
go mod tidy
go run main.go
```

---

## Örnek çıktı

```
2025/06/16 21:45:00 Tracking source IPs on eth0...
Top Source IPs:
  192.168.1.101 => 15 packets
  10.0.0.5      => 7 packets
  8.8.8.8       => 2 packets
```

---

## Sonuç

Bu yazıda, **CO-RE** desteği ile yazılmış taşınabilir bir eBPF uygulaması geliştirdik. Packet counter uygulamasını bir adım ileri taşıyarak, **kaynak IP adreslerine göre trafik analizi** gerçekleştirdik.

Bu yapı sayesinde artık kernel header'larını elle ayarlamaya gerek kalmadan, farklı sistemlerde çalışabilen bir analiz aracı elde ettik.

Bir sonraki yazıda, eBPF üzerine öğrendiğim yeni şeyleri paylaşacağım. Şimdilik esenlikle kalın..