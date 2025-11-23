# Blog Tasarım Notları

## Neumorphism Dark Theme

Blog, modern neumorphism (soft UI) tasarım prensiplerine göre siyah tema ile yeniden tasarlandı.

### Renk Paleti

- **Arka Plan (Dark)**: `#1a1a1a`
- **Yükseltilmiş Arka Plan**: `#242424`
- **Birincil Metin**: `#e0e0e0`
- **İkincil Metin**: `#a0a0a0`
- **Vurgu Rengi**: `#00d4ff` (Cyan)
- **Vurgu Hover**: `#00b8e6`

### Neumorphism Efektleri

#### Flat (Düz Yüzey)
```scss
box-shadow: 
  8px 8px 16px rgba(0, 0, 0, 0.7),
  -8px -8px 16px rgba(255, 255, 255, 0.05);
```

#### Pressed (Basılı)
```scss
box-shadow: 
  inset 4px 4px 8px rgba(0, 0, 0, 0.7),
  inset -4px -4px 8px rgba(255, 255, 255, 0.05);
```

#### Hover (Üzerine Gelindiğinde)
```scss
box-shadow: 
  12px 12px 24px rgba(0, 0, 0, 0.7),
  -12px -12px 24px rgba(255, 255, 255, 0.05);
transform: translateY(-2px);
```

### Bileşenler

#### Header
- Neumorphism kart içinde
- Gradient başlık efekti
- Merkezi hizalama

#### Post Kartları
- Neumorphism efekti
- Hover animasyonları
- Kategori etiketleri
- Post açıklamaları

#### Navigasyon
- Her menü öğesi ayrı neumorphism kartı
- Hover efektleri
- Smooth geçişler

#### Code Blocks
- Pressed (basılı) efekt
- Syntax highlighting desteği
- Rounded köşeler

#### Blockquotes
- Flat neumorphism
- Sol kenarda accent rengi
- İtalik metin

#### Görseller
- Neumorphism çerçeve
- Hover efekti
- Otomatik merkezi hizalama

### Responsive Tasarım

Mobil cihazlar için optimize edilmiş:
- Küçük ekranlarda font boyutları ayarlanır
- Padding değerleri azaltılır
- Kartlar tam genişlik kullanır

### Animasyonlar

- Smooth geçişler (0.3s ease)
- Hover efektleri
- Glow animasyonları
- Pulse loading animasyonu

### Özelleştirme

Renkleri değiştirmek için `_sass/no-style-please.scss` dosyasındaki değişkenleri düzenleyin:

```scss
$bg-dark: #1a1a1a;
$bg-elevated: #242424;
$text-primary: #e0e0e0;
$text-secondary: #a0a0a0;
$accent: #00d4ff;
```

### Tarayıcı Desteği

- Chrome/Edge: ✅ Tam destek
- Firefox: ✅ Tam destek
- Safari: ✅ Tam destek
- Mobile: ✅ Responsive

### Performans

- Minimal CSS (< 10kb)
- Hardware-accelerated animasyonlar
- Optimize gölge efektleri
- Lazy loading görseller

## Medium Entegrasyonu

Medium'dan gelen yazılar otomatik olarak:
- Neumorphism tasarımına uyarlanır
- Kategori etiketleri eklenir
- Medium linki footer'da gösterilir
- Açıklama alanı doldurulur
