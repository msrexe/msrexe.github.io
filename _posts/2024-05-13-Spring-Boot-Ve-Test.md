---
layout: post
title: "Spring Boot ve Test"
description: "Spring Boot uygulamalarında unit, integration, controller ve servis testlerini nasıl yazabileceğimizi öğreneceğiz."
image: https://miro.medium.com/v2/resize:fit:720/format:webp/1*2nsd5m6n8XPb9fegxMVwAg.png
category: java
slug: spring-boot-ve-test
author: msrexe
---

![Spring Boot ve Test](https://miro.medium.com/v2/resize:fit:720/format:webp/1*2nsd5m6n8XPb9fegxMVwAg.png)

Selamlar, günümüzde test odaklı geliştirme (TDD) sadece bir trend veya koduna güvenmeyen yazılımcıların kurtarıcısı(!) değil, aynı zamanda kaliteli ve sürdürülebilir yazılım geliştirme pratiğinin vazgeçilmez bir parçasıdır. Her ne kadar zaman kısıtı olan geliştirme süreçlerine dahil edilmekten korkulsa da aslında çoğu hatayı canlı ortamdan önce bulup çözmemizi sağlayarak bize ciddi bir ivme kazandırabilir. Burada kritik nokta coverage olacaktır ki bunun için [Üstad Testivus’un felsefesini](https://imantung.medium.com/testivus-unit-testing-philosophy-7f4a7f6a43da) okuyabilirsiniz. 

Bizim konumuz daha çok Spring Boot uygulamalarımızda nasıl etkili testler yazabileceğimiz olacak. Örneklerimizde Java üzerinden ilerleyeceğiz. Ufaktan başlayalım.

#### 1. Junit Kurulumu
JUnit, Java topluluğu tarafından en geniş kabul gören test framework’üdür. Spring Boot projelerinde test yazımını kolaylaştırmak için aşağıdaki adımı uygulayarak JUnit’i ve Spring Boot’un testler için sağladığı isviçre çakımızı projeye dahil edebiliriz:

```xml
<! - pom.xml dosyanıza ekleyeceğiniz bağımlılık ->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

#### 2. Unit Testler
Unit testleri, bir uygulamanın temel taşlarını oluşturan en küçük kod parçalarını, yani fonksiyonları veya metotları test etmek için kullanılır. Bu testler sayesinde, her bir modülün beklenen davranışları sergilediğinden emin olabiliriz. Çok yaygın bir örnek olacak ama hesap makinesi üstünden gidersek toplama fonksiyonunu aşağıdaki gibi test edebiliriz:
```java
// CalculatorService.java
public class CalculatorService {

 public int add(int a, int b) {
 return a + b;
 }

}

// CalculatorServiceTest.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CalculatorServiceTest {

 @Test
 void testAdd() {
 CalculatorService calculatorService = new CalculatorService();
 int result = calculatorService.add(2, 3);
 assertEquals(5, result, "Toplama işlemi doğru çalışmalı.");
 }

}
```
#### 3. Integration Testleri
Integration testleri, uygulamanın farklı modüllerinin birlikte sorunsuz çalıştığını doğrulamak için kritik öneme sahiptir. Bu testler, özellikle veritabanları, API’lar veya harici servisler gibi üçüncü taraflarla etkileşimde bulunan bileşenler için önemlidir. Örnek olarak, bir kullanıcıyı veritabanında doğru bir şekilde sorgulayıp sorgulayamadığımızı test edelim:
```java
// UserRepositoryIntegrationTest.java
@SpringBootTest // Daha spesifik contextler kullanarak her testte test etmeyeceğimiz kısımları load etmekten kaçınabiliriz.
@AutoConfigureTestDatabase
class UserRepositoryIntegrationTest {

 @Autowired
 private UserRepository userRepository;

@Test
 void testFindByUsername() {
 User user = new User("john_doe", "John", "Doe");
 userRepository.save(user);
Optional<User> foundUser = userRepository.findByUsername("john_doe");
 assertTrue(foundUser.isPresent(), "Kullanıcı bulunamadı.");
 assertEquals("John", foundUser.get().getFirstName(), "İsim alanı doğru olmalı.");
 }

}
```

#### 4. Controller Testleri
Web uygulamalarında, olayın kritik kısımlarından biri HTTP request ve response’larını test etmek diyebiliriz. Burada bize Spring‘in MockMvc aracı, yardımcı olacak. Aşağıdaki örnekte, bir kullanıcının bilgilerini doğru şekilde alıp almadığımızı kontrol ediyoruz:

```java
// UserControllerTest.java
@WebMvcTest(UserController.class)
class UserControllerTest {

 @Autowired
 private MockMvc mockMvc;

@MockBean // Burada spring-boot-test içerisinde gelen mockito'yu kullanıyoruz
 private UserService userService;

@Test
 void testGetUser() throws Exception {
 User user = new User("john_doe", "John", "Doe");
 when(userService.getUserByUsername("john_doe")).thenReturn(user);
mockMvc.perform(get("/users/john_doe"))
 .andExpect(status().isOk())
 .andExpect(jsonPath("$.username").value("john_doe"))
 .andExpect(jsonPath("$.firstName").value("John"))
 .andExpect(jsonPath("$.lastName").value("Doe"));
 }

}
```

#### 5. Servis Testleri
Servis testleri, uygulamanın logiclerini doğrulamak için hayati öneme sahiptir. Bu testler, servis katmanındaki işlevlerin doğru çalıştığını kontrol etmek için tasarlanmıştır. Aşağıda, bir user servis testini görebilirsiniz:

```java
// UserServiceTest.java
@SpringBootTest
class UserServiceTest {

 @MockBean
 private UserRepository userRepository;

@Autowired
 private UserService userService;

@Test
 void testGetUserByUsername() {
 User user = new User("john_doe", "John", "Doe");
 when(userRepository.findByUsername("john_doe")).thenReturn(Optional.of(user));
User foundUser = userService.getUserByUsername("john_doe");
 assertEquals("john_doe", foundUser.getUsername(), "Kullanıcı adı doğru olmalı.");
 assertEquals("John", foundUser.getFirstName(), "İsim doğru olmalı.");
 assertEquals("Doe", foundUser.getLastName(), "Soyadı doğru olmalı.");
 }

}
```

##### Testleri Çalıştırma:
Burada kullandığımız build ortamına bağlı olarak iki farklı komut ile testlerimizi koşturabiliriz.

**Gradle** için:
```bash
./gradlew test
```
**Maven** için:
```bash
mvn test
```

#### Sonuç
Bu yazıda Java ve Spring Boot kullanarak uygulamalarınız için nasıl etkili testler yazabileceğimizi detaylı bir şekilde inceledik. Unit testlerden başlayarak, integration, controller ve servis testlerine kadar farklı test türlerini ve bu testlerin nasıl yapıldığına dair örnekler okuduk.

Aslında mock’lar üzerine de yeterince eğilmedik ama yazı çok uzadı part 2 falan bakarız ona. Bir sonraki yazıda görüşmek dileğiyle…
