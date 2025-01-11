---
layout: post
title: "BPF Günlükleri: Sıfırdan Packet Counter Uygulaması"
description: "Bu yazıda, eBPF yapısını kullanarak sıfırdan bir paket sayacı uygulaması geliştireceğiz."
image: https://networkop.co.uk/img/xdp-xconnect.png
category: linux
slug: bpf-ile-packet-counter-uygulamasi
author: msrexe
---

![eBPF XDP](https://networkop.co.uk/img/xdp-xconnect.png)

Bu yazıda, eBPF yapısını kullanarak sıfırdan bir paket sayacı uygulaması geliştireceğiz. Uygulamamızı C dili ile yazdıktan sonra Cilium'un `bpf2go` aracı ile derleyeceğiz. Sonrasında uygulamamızı kernel'a atacağımız bir Go kodu ile yazımızı tamamlayacağız. Şimdi malzeme listesiyle başlayalım.
 
### Gereksinimler
- Linux (BPF desteği olan bir kernel)
- Clang ve LLVM (eBPF programlarını derlemek için) 
- Go (eBPF programlarını yüklemek ve kontrol etmek için)


### Uygulama
- Öncelikle eBPF ile çalışacak programımızı yazalım. Bu program, gelen paketleri sayacak ve bir sayaç değerini arttıracak. 

```c
//go:build ignore

#include <linux/bpf.h> // Bu header dosyası her kernel sürümü için farklılık gösterir. "apt-get install linux-headers-$(uname -r)" komutu ile kernelinize uygun header dosyalarını yükleyebilirsiniz

#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, __u64);
    __uint(max_entries, 1);
} pkt_count SEC(".maps");

SEC("xdp") // XDP hook'unu kullanarak çalışacak
int count_packets() {
    __u32 key    = 0;
    __u64 *count = bpf_map_lookup_elem(&pkt_count, &key);
    if (count) {
        __sync_fetch_and_add(count, 1);
    }

    return XDP_PASS;
}
```

- Ardından, bu programı `bpf2go` aracı ile derleyebilmemizi sağlayacak Go programını yazalım.

```go
package main

//go:generate go run github.com/cilium/ebpf/cmd/bpf2go counter counter.c
```

- Şimdi, bu Go kodunu çalıştırarak C kodumuzu derleyelim. 

```bash
go mod init ebpf-test && go mod tidy

go generate
```

- Derleme işlemi başarılı bir şekilde tamamlandıysa birkaç tane dosya oluşmuş olmalı. 
    - `counter_bpfeb.go`
    - `counter_bpfel.go`
    - `counter_bpfeb.o` 
    - `counter_bpfel.o`
- Not: Go kodlarını incelediğimizde kernel'a yükleyeceğimiz programdan okuma işlemleri yapmak için gerekli yapıları oluşturduğunu görebiliriz.

- Son olarak, bu programı kernele yükleyecek ve kontrol edecek Go kodunu yazalım ve çalıştıralım.

```go
package main

import (
    "log"
    "net"
    "os"
    "os/signal"
    "time"

    "github.com/cilium/ebpf/link"
    "github.com/cilium/ebpf/rlimit"
)

func main() {
    // Remove resource limits for kernels <5.11.
    if err := rlimit.RemoveMemlock(); err != nil { 
        log.Fatal("Removing memlock:", err)
    }

    // Load the compiled eBPF ELF and load it into the kernel.
    var objs counterObjects 
    if err := loadCounterObjects(&objs, nil); err != nil {
        log.Fatal("Loading eBPF objects:", err)
    }
    defer objs.Close() 

    ifname := "eth0" // Change this to an interface on your machine.
    iface, err := net.InterfaceByName(ifname)
    if err != nil {
        log.Fatalf("Getting interface %s: %s", ifname, err)
    }

    // Attach count_packets to the network interface.
    link, err := link.AttachXDP(link.XDPOptions{ 
        Program:   objs.CountPackets,
        Interface: iface.Index,
    })
    if err != nil {
        log.Fatal("Attaching XDP:", err)
    }
    defer link.Close() 

    log.Printf("Counting incoming packets on %s..", ifname)

    // Periodically fetch the packet counter from PktCount,
    // exit the program when interrupted.
    tick := time.Tick(time.Second)
    stop := make(chan os.Signal, 5)
    signal.Notify(stop, os.Interrupt)
    for {
        select {
        case <-tick:
            var count uint64
            err := objs.PktCount.Lookup(uint32(0), &count) 
            if err != nil {
                log.Fatal("Map lookup:", err)
            }
            log.Printf("Received %d packets", count)
        case <-stop:
            log.Print("Received signal, exiting..")
            return
        }
    }
}
```

```bash
go run main.go
```

- Terminalde şunu gördüyseniz ilk eBPF uygulamanızı başarıyla geliştirdiniz demektir.

```bash
msrexe@ubuntu:~/ebpf-test$ sudo go run .
2024/05/29 23:41:44 Counting incoming packets on eth0..
2024/05/29 23:41:45 Received 0 packets
2024/05/29 23:41:50 Received 0 packets
2024/05/29 23:41:51 Received 1 packets
2024/05/29 23:41:54 Received 3 packets
2024/05/29 23:41:55 Received 4 packets
```

### Sonuç
Bu yazıda, eBPF yapısını kullanarak sıfırdan bir paket sayacı uygulaması geliştirdik. Bu uygulamada eğer linux/bpf.h sebebiyle hata aldıysanız ve kernel headerları ile çok uğraştıysanız bir sonraki yazıda anlatacağım portable bpf uygulamaları geliştirmek için kullanılan [BPF CO-RE](https://thegraynode.io/posts/portable_bpf_programs/) yapısını inceleyebilirsiniz.

#### Kaynaklar
- [Getting Started with eBPF and Go](https://ebpf-go.dev/guides/getting-started)
