---
layout: post
title: "Go dilinde Concurrency ve Waitgroup kullanımı"
description: "Go'da Concurrency ve WaitGroup kullanımından bahsettiğimiz bu yazıda, WaitGroup'ların ne işe yaradığını ve nasıl kullanıldığını öğreneceksiniz."
image: https://miro.medium.com/v2/resize:fit:640/format:webp/0*g3r6gLwL2t7fv0Sm.png
category: go
slug: go-dilinde-concurrency-ve-waitgroup-kullanimi
author: msrexe
lang: tr
---

![Go dilinde Concurrency ve WaitGroup kullanımı](https://miro.medium.com/v2/resize:fit:640/format:webp/0*g3r6gLwL2t7fv0Sm.png)

Merhaba, bu yazımda dilim döndüğünce “Go dilinde WaitGroup’lar ne işe yarar ve nasıl kullanabiliriz ?” sorusunu yanıtlayacağım. Ufaktan başlayalım.

Öncelikle Go’da bize concurrent (eşzamanlı) fonksiyonlar çalıştırma imkanı veren goroutine’den bahsedelim. Goroutine işletim sistemi seviyesinde, düşük maliyetli, thread benzeri yapılar oluşturmamızı sağlayan Go dilinin sunduğu nimetlerden biridir. Ve bunu kullanmak için de tek yapmanız gereken eşzamanlı hale getirmek istediğiniz işlemlerin başına “go” ifadesini eklemek.
Aşağıdaki görselde basit bir örnek verilmiştir.

![Örnek 1](https://miro.medium.com/v2/resize:fit:720/format:webp/1*hCFjoWx-Yq9kEW5pcCtmEQ.png)


Bu koddan beklenen konsola sırası farketmeksizin “app started”, “concurrent func 1”, “concurrent func 2”, “app finished” yazmasıdır. Bakalım öyle mi oluyor.

![Örnek 2](https://miro.medium.com/v2/resize:fit:546/format:webp/1*Ih_Oc0k3Rhn-TfF10oUxcQ.png)

Gördüğünüz gibi bizim func1() ve func2() fonksiyonlarımız hiç çalışmamış bile. Bunun sebebi bizim hali hazırda çalışan main goroutine’imizin haricinde 2 goroutine daha başlatmamış olmamız. Ancak bizim main goroutine’imiz biz aksini söylemediğimiz sürece sadece kendi işini bitirip, yani ekrana “app started” ve “app finished” yazıp tamamlanacak ve diğer goroutinelerin tamamlanmasını beklemeyecek. Peki bunu çözmek için ne yapabiliriz ? İki yolumuz var:

#### 1- time.Sleep() kullanmak

![Örnek 3](https://miro.medium.com/v2/resize:fit:720/format:webp/1*zB4maCiFhqXf8lW3GR6GhQ.png)

Koda time.Sleep() ekleyerek main goroutine’imizin 1 saniye uyumasını sağladık. Ve bu uyku esnasında diğer goroutine’ler işini tamamladı ve ortaya şöyle bir sonuç çıktı.

![Örnek 4](https://miro.medium.com/v2/resize:fit:618/format:webp/1*j38ENSFqlOcYHO40ITQ0nQ.png)

Evet istediğimiz şeyi aldık. Tüm goroutine’ler üstüne düşeni yaptı ve uygulamamız tamamlandı. Ancak burada sıkıntılı bir durum ortaya çıkıyor. Milisaniyelerin bile önemli olduğu uygulamalarda bir goroutine’i 1 saniye boyunca uyutmak oldukça ciddi bir verim kaybı olurdu. İşte bu noktada yardımımıza asıl konumuz olan WaitGroup yetişiyor.

#### 2- sync.WaitGroup kullanmak

![Örnek 5](https://miro.medium.com/v2/resize:fit:720/format:webp/1*sxsZfX76PEnCVjGJrxtRGg.png)

Kodu açıklamak gerekirse başta “wg” adında bir WaitGroup tanımladık. Daha sonra wg.Add(2) diyerek 2 adet goroutine oluşturacağımızı söyledik ve WaitGroup’umuzun pointer’ını func1 ve func2 içerisine parametre olarak gönderdik. Burası önemli, pointer olarak göndermezseniz WaitGroup beklediği uyandırma sinyallerini alamaz ve uygulamanız şöyle bir hata verir.

![Örnek 6](https://miro.medium.com/v2/resize:fit:720/format:webp/1*EPtB0M25K0OzJIa9P2TDJA.png)

Her neyse tüm adımları doğru bir şekilde yazdıktan sonra yapmamız gereken şey wg.Wait() diyerek main goroutine’imizi diğer fonksiyonlardan “done” sinyali gelene kadar uyutmak olacaktır. Böylece uygulamamız sorunsuz ve gecikme yaşamadan çalışacaktır.

![Örnek 7](https://miro.medium.com/v2/resize:fit:626/format:webp/1*Owmanw8DxmpJwWuVDYi22g.png)

Böylelikle benim paylaştığım ilk içeriğin sonuna geldik. Umarım faydalı olabilmişimdir. Geri bildirimleriniz veya sorularınız için Twitter üzerinden bana ulaşabilirsiniz.
