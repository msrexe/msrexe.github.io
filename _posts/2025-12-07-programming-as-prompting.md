---
layout: post
title: "Prompt Engineering’in Evrimi: “Yazdım Oldu”dan Programlama Diline"
description: "Chain-of-thought, ReAct, tool use ve modern prompt şablonlarının nasıl yeni bir programlama paradigmasına dönüşümü."
image: /assets/images/meme-prompt.jpg
category: ai
slug: prompt-engineering
author: msrexe
lang: tr
---

![Image](/assets/images/meme-prompt.jpg)

LLM dünyasına ilk girdiğimiz zaman hepimizin yaşadığı bir dönem vardı:  
**“Bir şey yazıyorum, model de bir şey söylüyor.”**

Ama işler orada kalmadı. Bugün geldiğimiz nokta, prompt’ların neredeyse **kendi kuralları, kontrol akışları ve veri modelleri olan küçük birer program** gibi davrandığı bir dönem. Bu yazıda, dilim döndüğünce bu konuyu ele almaya çalışacağım.

---

## 1. Prompt Engineering’in Dönüşümü

LLM’lerin ilk dönemlerinde sistem oldukça basitti:

> Kullanıcı bir şey yazar → Model cevap verir

Zaman içinde hem modeller büyüdü hem de onlardan beklentimiz. Bir noktada fark ettik ki:

- Prompt dediğimiz mevzu, günün sonunda **bir kontrat**.
- Model, bu kontrata uymaya çalışıyor.
- Kontrat ne kadar netse, sonuç o kadar stabil oluyor.

Bu farkındalık bizi bugünkü LLM dünyasının temel kavramlarına taşıdı: **chain-of-thought**, **ReAct**, **tool use**, **system prompt mimarileri** ve **prompt şablonları**.

---

## 2. Chain-of-Thought: Modelin Düşünmesine İzin Vermek

Chain-of-thought (CoT), aslında çok basit bir ilkeye dayanıyor:

**Modelin cevabı değil, o cevaba giden yolu üretmesini sağlamak.**

Bir matematik sorusu düşünelim. Çözümü direkt istemekle, çözüm adımlarını istemek arasında ciddi fark var. CoT, modelin *içsel kararsızlıklarını daha stabil bir forma sokuyor* çünkü model adım adım ilerleyerek hatayı minimize ediyor.

### Basit bir CoT akışı

```

Soru → Ara adımlar (Reasoning Steps (Chain-of-Thought)) → Sonuç

````

CoT, özellikle teknik konularda, algoritma açıklamalarında, hata analizlerinde ve uzun planlama gerektiren işlerde öne çıkıyor.

> Not: CoT her zaman açık şekilde verilmez. LLM’lerin çoğu içsel olarak zaten bir tür gizli chain-of-thought çalıştırır.

---

## 3. ReAct: Düşünme + Hareket Etme

ReAct, adından da anlaşılacağı üzere **Reasoning + Acting** birleşimidir.

Bu yöntem, modele sadece düşünmeyi değil, dış sistemlerle iletişim kurmayı da öğretiyor.
Yani:

1. Düşün →
2. Bir eylem seç →
3. Tool çağır (MCP muhabbetlerinin devreye girdiği yer) →
4. Sonucu değerlendir →
5. Yeniden düşün →
6. Final cevabı ver

### ReAct döngüsü

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant M as Model
    participant T as Tool

    U->>M: Soru
    M->>M: Reasoning Step
    M->>T: Tool Action
    T->>M: Tool Output
    M->>M: New Reasoning Step
    M->>U: Final Answer
</div>


Bu yaklaşım özellikle **kod oluşturma**, **veri çekme**, **hesaplama yapma**, **RAG tabanlı sorgular** ve **ajan sistemleri** için temel yapı taşı haline geldi.

---

## 4. Tool Use: LLM’in Alamet-i Farikası

Tek başına bir model çok şey yapabilir; ama **dış araçlara erişimi olan** tabiri caizse uzuvları olan bir model, bambaşka bir seviyedir.

Tool use, LLM’lere:

* Web search
* Kod çalıştırma
* Veri tabanı sorgulama
* Dönüşümler (image → text vb.)
* Hesaplama

gibi yetenekler kazandırıyor.

Böylece model artık sadece "konuşan" bir varlık değil;
**iş yapan ajan** oluyor.

---

## 5. System Prompt: Görünmeyen Kod

System prompt, çoğu kullanıcı için görünmeyen ama işin en kritik kısmı.

Eğer prompt’ı bir program olarak düşünürsek, system prompt da **main() fonksiyonuna** benzer.
Modelin kimliği, sınırları ve davranış şekli burada belirlenir.

### System prompt neleri belirler?

* Ton
* Rol
* Sorumluluklar
* Format
* Güvenlik kuralları
* Kısıtlamalar

Kısacası system prompt, modelin *doğal ortamıdır*.

Bazen tek bir satır:

> "You are a helpful assistant."

Bazen de sayfalarca kurallar:

```
You MUST always respond in JSON.
Never break schema.
Use short sentences.
```

Bu yapı sayesinde, LLM’ler “çıktıda tutarlılık” sağlamaya çok daha yatkın hale gelir. 

Geçenlerde Twitter'ın Grok'unda yaşanan sağa sola sataşma, küfürler savurma olayı da burada yapılan değişiklikler sonucu meydana gelmiş ve yine uygun system promptları ile çözülmüştü. 
![alt text](/assets/images/grok-fix-commit.png)

---

## 6. Prompt Şablonları ve Best Practice’ler

Bir noktadan sonra prompt yazmak, *her seferinde sıfırdan metin üretmekten* çok daha fazlası oldu.
Kendimizi şablonlar oluştururken ve bunun küçük bir DSL’e dönüştüğünü fark ederken bulduk.

İyi bir prompt şablonu:

* **Girdi formatını açıklar**
* **Çıkışı tanımlar**
* **Örnek input-output sağlar**
* **Köşeli durumları belirtir**
* **Modelin sınırlarını çizer**

### Örnek bir şablon

```
# Task
Sen bir kod inceleme aracı olarak davranacaksın.

# Input Format
<code></code> etiketleri arasında yalnızca Go kodu verilecek.

# Output Format
Aşağıdaki alanları içeren JSON üret:
- issues: []
- suggestions: []
- complexity_score: number

# Rules
- Kod çalışabilir olmasa bile analiz et.
- Tahmin etme; sadece kodda gördüğünü yorumla.
```

Bu yapı, modele aslında *küçük bir API kontratı* sunar.

---

## 7. Prompt Artık Bir Dil: Peki Sonrası?

Bugün geldiğimiz seviyede, prompt artık “metin girişi” değil,
**kontrollü bir programlama modeli**.

Üstelik:

* Kontrol akışı var (ReAct)
* Fonksiyon çağrıları var (tool use)
* Derin düşünme var (CoT)
* Runtime davranışını belirleyen bir config var (system prompt)
* Şablonlar var (bir nevi DSL mantığı)

Kısacası, prompt engineering artık kendi ekosistemini oluşturmuş durumda.

---

## Sonuç

Bu yazıda, prompt engineering’in basit bir “yazdım oldu” anlayışından çıkıp, kendi kurallarına sahip bir **programlama modeline** dönüşümünü ele aldık. CoT, ReAct, tool use ve system prompt gibi kavramların her biri bu dönüşümde kritik rol oynuyor.

Artık bir LLM’e soru sorduğumuzda sadece cevap almıyoruz;
**modelle birlikte bir çalışma akışı tasarlıyoruz.**

Bir sonraki yazıda buluşana dek
esenlikle kalın..