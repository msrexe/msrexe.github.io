---
layout: post
title: "Go derleyicisine genel bakış"
description: "Go dilinde compiler hakkında genel bilgiler ve compiler'ın hızlı çalışmasını sağlayan mekanizmalar."
image: https://miro.medium.com/v2/resize:fit:720/format:webp/1*fm_2f3N7U64ykEIJmoLqaQ.png
category: go
slug: go-derleyicisine-genel-bakis
author: msrexe
---

![Go derleyicisine genel bakış](https://miro.medium.com/v2/resize:fit:720/format:webp/1*fm_2f3N7U64ykEIJmoLqaQ.png)

Selamlar bu yazımızda Go dilinde compiler hakkında konuşacağız. Go çalışma ve derleme hızı ile öne çıkan bir dil. Peki Go compiler’ının bu performansı sağlayan mekanizması nedir, nasıl çalışır? Hadi bunun nedenlerine girmeden önce kısaca Go compiler yapısını ve compile adımlarını inceleyelim.

<b>Go derleyicisi, Go kodunu makine diline derlemekten sorumludur. Temel olarak 4 aşamadan oluşur:</b>
**1. Ayrıştırma:** Kod lexemlere (sözcük) ve söz dizimsel yapılara ayrıştırılır. Böylece kodun anlamı çözümlenir.
**2. Tip denetimi:** Değişkenlerin ve ifadelerin doğru veri tiplerine sahip olup olmadığı kontrol edilir.
**3. Ara temsil oluşturma:** Derleyicinin kendi soyut söz dizimi ağacı (AST) oluşturulur. Bu soyut dil ile kod üzerinde işlem yapılabilir.
**4. SSA oluşturma:** Soyut söz dizimi, SSA formuna dönüştürülür.
**5. Makine kodu üretimi:** Hedef işlemci mimarisine özgü optimizasyonlar uygulanır ve nihai makine kodu üretilir.

![Go compile adımları](https://miro.medium.com/v2/resize:fit:720/format:webp/1*P0P3NdFZsiDJQ5ZLp-nc6w.png)  

**SSA Nedir?**

SSA (Static Single Assignment), her değişkenin tam olarak bir kez atanmasını ve kullanılmadan önce tanımlanmasını gerektiren bir ara temsil biçimidir.

![SSA](https://miro.medium.com/v2/resize:fit:720/format:webp/1*atcd1AttViKSP07RNIzeMg.png)

Normal kodda bir değişken birden fazla kez atanabilir:

```go
x = 2 
x = x + 1
```
SSA formunda ise her atama yeni bir değişken versiyonu oluşturur:
    
```go
x1 = 2
x2 = x1 + 1
```

Böylece değişkenin her kullanımının hangi tanımdan geldiği netleşir. Bu da optimizasyonlar için çok faydalıdır.

Bu temel bilgileri aldıktan sonra Go compiler’ının avantajlarına bakabiliriz.

**1- Sade ve Anlaşılır Söz Dizimi**
Go dili, C gibi geleneksel sistem dillerine benzer sade ve anlaşılır bir sözdizimine sahiptir. Karmaşık ve çok fazla özelliği olmayan bu sözdizimi, compiler’ın işini oldukça kolaylaştırır. Compiler, kaynak kodu çok daha hızlı bir şekilde ayrıştırabilir ve çözümleyebilir.

**2- Hızlı Lexer ve Parser**
Go derleyicisi, lexing ve parsing işlemlerini çok hızlı bir şekilde gerçekleştirebilmektedir.

Lexer, geleneksel deterministik sonlu otomat (DFA) yerine daha basit ve hızlı çalışan bir Regular Expression tabanlı lexing algoritması kullanır. Böylece token’lara ayırma işlemi çok daha hızlı tamamlanır.

Parser ise Pratt ayrıştırıcı olarak bilinen özel bir top-down ayrıştırma algoritmasıyla çalışır. Bu algoritma, operator önceliği ve associativity kurallarını kod içine gömülü şekilde barındırır. Böylece parsing süreci önemli ölçüde hızlanır.
Ayrıca parser, kaynak koddaki hataları eşzamanlı olarak bulmaya çalışır. Tüm dosyanın ayrıştırılmasını beklemez. Bu da parser’ın çok daha erken sonuç üretmesini sağlar.

Lexer ve parser’daki bu optimizasyonlar sayesinde Go derleyicisi, geleneksel derleyicilere göre çok daha hızlı bir şekilde kaynak kodu ayrıştırabilmektedir.

**3- İyi Tasarlanmış Tip Sistemi**
Compile işleminde tip denetimi de önemli bir adımdır. Go’nun iyi tasarlanmış ve tutarlı tip sistemi, bu denetimleri çok hızlı yapabilmesini sağlar. Ayrıca tip çıkarımı da developer’ın iş yükünü azaltır.

**4- Statik Tipleme**
Go statik bir dil olduğu için, birçok tip denetimi derleme zamanında yapılabilmektedir. Bu da programa hız kazandırır. Dinamik dillerde bu denetimler çalışma zamanında (runtime) yapılır.

**5- SSA Tabanlı Optimizasyon**
SSA sayesinde kod üzerinde aşağıdaki gibi oldukça etkili optimizasyonlar uygulanabilmektedir.

- **Ölü kod eleme:** Kullanılmayan kod blokları temizlenir.
-  **Değer aralığı yayılımı:** Değişkenin alabileceği değerler önceden hesaplanır.
- **Koşullu sabit yayılımı:** Bazı koşulların her zaman doğru olacağı tespit edilir.
- **Aritmetik optimizasyon:** Pahalı işlemler daha ucuzlarıyla değiştirilir. Örneğin çarpma, kaydırma ile.
- **Kayıt tahsisi:** İşlemcide sınırlı sayıda kayıt olduğundan, bunlar en verimli şekilde kullanılır.

***SSA*** hakkında detaylı bilgiye [buradan](https://mattermost.com/blog/diving-into-static-single-assignment-with-the-go-compiler/) ulaşabilirsiniz.

**6- Basitlik ve Tutarlılık**
Go dili, C diline benzer şekilde basit ve tutarlı bir yapı sunar. Karmaşık özellikler yerine temel mekanizmaları iyi yapmaya odaklanmıştır. Bu da derleyicinin işini kolaylaştırır.

**Sonuç**
Genel olarak bakacak olursak Go compiler’ının sağladığı hızın ardındaki faktörler; sade ve anlaşılır sözdizimi, hızlı lexer/parser, iyi tasarlanmış tip sistemi, SSA tabanlı optimizasyonlar, statik tipleme, basitlik ve hızlı derleme süreleridir.

Bu özellikler sayesinde Go, C/C++ gibi geleneksel sistem dillerinin hızına yaklaşırken, derleme hızı, type-safety, otomatik bellek yönetimi gibi modern dillerin avantajlarını da sunabilmektedir. Ayrıca büyük projelerde bile derleme ve bağlantı işlemleri çok kısa sürmesi geliştiricinin en değerli kaynağından yani zamandan tasarruf etmesini sağlar.

Kısaca Go compiler’dan bahsetmeye çalıştım, umarım faydalı olmuştur. Geri bildirimlerinizi Twitter üzerinden yapabilirsiniz.
