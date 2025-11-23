# Medium Yazı Senkronizasyonu

Bu GitHub Actions workflow'u, Medium'daki yazılarınızı otomatik olarak Jekyll blog'unuza aktarır.

## Kurulum

### 1. Medium Kullanıcı Adını Ayarlama

GitHub repository'nizde Secret olarak Medium kullanıcı adınızı ekleyin:

1. GitHub repository'nize gidin
2. **Settings** > **Secrets and variables** > **Actions** sekmesine tıklayın
3. **New repository secret** butonuna tıklayın
4. Name: `MEDIUM_USERNAME`
5. Secret: Medium kullanıcı adınızı girin (örn: `msrexe`)
6. **Add secret** butonuna tıklayın

### 2. Workflow'u Çalıştırma

#### Otomatik Çalışma
Workflow her gün otomatik olarak çalışır ve yeni Medium yazılarınızı kontrol eder.

#### Manuel Çalışma
İstediğiniz zaman manuel olarak da çalıştırabilirsiniz:

1. GitHub repository'nizde **Actions** sekmesine gidin
2. Sol menüden **Sync Medium Posts** workflow'unu seçin
3. **Run workflow** butonuna tıklayın
4. **Run workflow** (yeşil buton) ile onaylayın

### 3. İlk Çalıştırma

İlk kez çalıştırdığınızda, Medium'daki tüm yazılarınız `_posts` klasörüne eklenecektir. Sonraki çalıştırmalarda sadece yeni yazılar eklenecektir.

## Nasıl Çalışır?

1. **RSS Feed Okuma**: Medium'un RSS feed'inizi okur (`https://medium.com/feed/@kullaniciadi`)
2. **Yeni Yazıları Tespit**: Henüz blog'unuzda olmayan yazıları bulur
3. **Dönüştürme**: HTML içeriği Markdown formatına dönüştürür
4. **Jekyll Formatı**: Jekyll'in beklediği front matter formatında dosya oluşturur
5. **Commit & Push**: Yeni yazıları otomatik olarak repository'ye ekler

## Oluşturulan Dosya Formatı

Her Medium yazısı için şu formatta bir dosya oluşturulur:

```markdown
---
layout: post
title: "Yazı Başlığı"
description: "Yazının kısa açıklaması..."
category: kategori
slug: yazi-basligi
author: msrexe
medium_url: https://medium.com/@kullaniciadi/yazi-linki
date: 2024-05-13 10:30:00
image: https://miro.medium.com/...
---

Yazı içeriği Markdown formatında...
```

## Özelleştirme

### Çalışma Zamanını Değiştirme

`.github/workflows/sync-medium.yml` dosyasındaki cron ifadesini düzenleyin:

```yaml
schedule:
  - cron: '0 0 * * *'  # Her gün gece yarısı (UTC)
  # - cron: '0 */6 * * *'  # Her 6 saatte bir
  # - cron: '0 12 * * 1'  # Her Pazartesi öğlen
```

### Script'i Özelleştirme

`.github/scripts/sync_medium.py` dosyasını düzenleyerek:
- Kategori mantığını değiştirebilirsiniz
- Markdown dönüşüm kurallarını ayarlayabilirsiniz
- Front matter alanlarını özelleştirebilirsiniz

## Sorun Giderme

### Workflow çalışmıyor
- Actions sekmesinde hata loglarını kontrol edin
- `MEDIUM_USERNAME` secret'ının doğru ayarlandığından emin olun

### Yazılar yanlış formatlanıyor
- Medium'daki yazınızın HTML yapısı farklı olabilir
- `sync_medium.py` dosyasındaki `html_to_markdown` fonksiyonunu düzenleyin

### Türkçe karakterler bozuk
- Script Türkçe karakterleri destekler, ancak sorun yaşarsanız `clean_filename` fonksiyonunu kontrol edin

## Test Etme

Lokal olarak test etmek için:

```bash
# Python bağımlılıklarını yükleyin
pip install feedparser requests python-frontmatter html2text

# Medium kullanıcı adınızı ayarlayın
export MEDIUM_USERNAME=msrexe

# Script'i çalıştırın
python .github/scripts/sync_medium.py
```

## Notlar

- Medium'un RSS feed'i en son 10 yazıyı gösterir
- Mevcut yazılar `medium_url` alanına göre kontrol edilir
- Yazılar bir kez eklendikten sonra güncellenmez (Medium'da düzenleme yaparsanız manuel güncellemeniz gerekir)
