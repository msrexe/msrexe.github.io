---
layout: post
title: "Configuration hot-reloading konsepti"
description: "Cloud-native web uygulamalarında konfigürasyon yönetiminde kullanılan configuration hot-reloading konseptinden bahsedeceğim."
image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ffhf9kxwn1ge92rbtq1cb.jpeg
category: software-design, cloud-native, devops
slug: configuration-hot-reloading-konsepti
author: msrexe
lang: tr
---

![Configuration hot-reloading konsepti](https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ffhf9kxwn1ge92rbtq1cb.jpeg)

Merhaba, bu yazımda cloud-native web uygulamalarında konfigürasyon yönetiminde kullanılan configuration hot-reloading konseptinden bahsedeceğim. Ufaktan başlayalım.

Öncelikle geleneksel web servislerinde konfigürasyonların nasıl yönetildiğine bakalım. 
- Genelde servis ayağa kalkarken dışarıdaki bir kaynaktan önceden tanımlanmış tüm değerleri alır. Bu kaynak bir environment dosyası, bir configuration manager veya direkt üzerinde çalıştığı işletim sistemi de olabilir. 
- Devamında uygulamamız aldığı değerlerle uygulamada gerekli olan işlemleri yapar ve çalışmaya başlar. 
- Restart atılana kadar konfigürasyon değişiklikleri ile ilgilenmez.

Peki bu sistemde anlık olarak değişiklikleri izleyerek veya dışarıdan tetiklenerek konfigürasyon değiştirme ihtiyacımız neden olsun ?

Bir çok sebebi olabilir ancak en yaygın olanından bahsetmek gerekirse loglama. 
Sunucunuzda çalışan tüm testlerden geçmiş, sorunsuzca çalıştığına inandığınız bir uygulama düşünün. Bir gün aniden anlam veremediğiniz bir sebepten dolayı istediğimiz gibi çalışmamaya başlıyor. 
Restart attığınızda ise tekrar çalışır hale geliyor. İlk işiniz logları okumak oluyor ancak loglarda problem görünmüyor çünkü loglama seviyenizden dolayı o an neler olduğuna dair yeterince detay bulamıyorsunuz. 
Bu büyük bir sistemde oldukça tehlikeli bir durumdur. Pimi çekilmiş bomba gibi gezen bir servisiniz var, her an bozulup diğer servisleri dolayısıyla production ortamını tehlikeye atabilir.

Bunun gibi nadiren karşılaştığınız hatalarda production ortamında mevcut state'i koruyarak yani restart atmadan debugging yapma ihtiyacınız olur. İşte bu anlarda uygulamayı kapatmadan loglama seviyenizi değiştirmek yani hot-reloading için yardımımıza bu pattern yetişiyor.

Aşağıdaki basit web-server uygulamasında bu yapının nasıl çalıştığını görebilirsiniz.

![Configuration hot-reloading örnek](https://res.cloudinary.com/practicaldev/image/fetch/s--jDUMbh8T--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kihettcgf92l75rfqf94.gif)

Örnek uygulamanın kodlarına [buradan](https://github.com/msrexe/configuration-hot-reload) ulaşabilirsiniz. Başka bir yazıda görüşmek üzere...

###### Kaynak: Justin Garrison, Kris Nova - Cloud Native Infrastructure Patterns for Scalable Infrastructure and Applications in a Dynamic Environment
