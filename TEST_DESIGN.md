# Tasarımı Test Etme

## Local Jekyll Server Başlatma

Blog tasarımını local olarak test etmek için:

```bash
# Jekyll ve bağımlılıkları yükleyin (ilk kez)
bundle install

# Jekyll server'ı başlatın
bundle exec jekyll serve

# Tarayıcınızda açın
# http://localhost:4000
```

## Medium Sync'i Test Etme

```bash
# Python bağımlılıklarını yükleyin
pip install feedparser requests python-frontmatter html2text

# Medium kullanıcı adınızı ayarlayın
export MEDIUM_USERNAME=msrexe

# Script'i çalıştırın
python .github/scripts/sync_medium.py

# Yeni eklenen postları kontrol edin
ls -la _posts/
```

## Değişiklikler

### ✅ Duplicate Kontrolü Güçlendirildi

Script artık üç farklı yöntemle duplicate kontrolü yapıyor:
1. **Medium URL** - Aynı Medium linki varsa atlar
2. **Başlık** - Aynı başlık varsa atlar  
3. **Slug** - Aynı slug varsa atlar

Bu sayede aynı yazı farklı şekillerde bile eklenmeye çalışılsa tespit edilir.

### 🎨 Neumorphism Dark Theme Uygulandı

#### Renk Şeması
- Siyah arka plan (#1a1a1a)
- Yükseltilmiş yüzeyler (#242424)
- Cyan vurgu rengi (#00d4ff)
- Yumuşak gölge efektleri

#### Bileşenler
- **Header**: Gradient başlık, neumorphism kart
- **Post Kartları**: 3D efekt, hover animasyonları
- **Navigasyon**: Her öğe ayrı kart
- **Code Blocks**: Basılı efekt, syntax highlighting
- **Görseller**: Çerçeveli, hover efekti
- **Blockquotes**: Flat efekt, accent border

#### Animasyonlar
- Smooth geçişler (0.3s)
- Hover efektleri
- Glow animasyonları
- Transform efektleri

#### Responsive
- Mobil optimize
- Esnek grid sistem
- Adaptive font boyutları

## Dosya Yapısı

```
├── _sass/
│   ├── no-style-please.scss          # Ana stil dosyası
│   └── neumorphism-components.scss   # Neumorphism bileşenleri
├── _layouts/
│   ├── post.html                     # Güncellenmiş post layout
│   └── ...
├── _includes/
│   ├── post_list.html                # Güncellenmiş post listesi
│   ├── menu_item.html                # Güncellenmiş menü
│   └── ...
├── .github/
│   ├── workflows/
│   │   └── sync-medium.yml           # GitHub Actions workflow
│   └── scripts/
│       └── sync_medium.py            # Medium sync script
└── assets/
    └── css/
        └── main.scss                 # CSS import dosyası
```

## Özelleştirme

### Renkleri Değiştirme

`_sass/no-style-please.scss` dosyasını düzenleyin:

```scss
$bg-dark: #1a1a1a;        // Arka plan
$bg-elevated: #242424;     // Kartlar
$accent: #00d4ff;          // Vurgu rengi
```

### Neumorphism Efektlerini Ayarlama

`_sass/no-style-please.scss` içindeki mixin'leri düzenleyin:

```scss
@mixin neu-flat {
  box-shadow: 
    8px 8px 16px $shadow-dark,
    -8px -8px 16px $shadow-light;
}
```

### Post Layout'u Özelleştirme

`_layouts/post.html` dosyasını düzenleyin.

## Sorun Giderme

### Jekyll build hatası
```bash
bundle update
bundle exec jekyll clean
bundle exec jekyll serve
```

### CSS değişiklikleri görünmüyor
- Tarayıcı cache'ini temizleyin (Ctrl+Shift+R)
- Jekyll server'ı yeniden başlatın

### Medium sync çalışmıyor
- `MEDIUM_USERNAME` secret'ının doğru olduğundan emin olun
- RSS feed'i manuel kontrol edin: `https://medium.com/feed/@kullaniciadi`

## GitHub'a Push Etme

```bash
git add .
git commit -m "🎨 Neumorphism dark theme ve geliştirilmiş Medium sync"
git push origin main
```

GitHub Actions otomatik olarak çalışacak ve site deploy edilecektir.
