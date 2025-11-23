#!/usr/bin/env python3
"""
Medium RSS feed'inden yazıları çekip Jekyll formatına dönüştürür.
"""

import feedparser
import os
import re
import html2text
from datetime import datetime
from pathlib import Path
import frontmatter

# Medium kullanıcı adınızı buraya yazın veya GitHub Secrets'tan alın
MEDIUM_USERNAME = os.environ.get('MEDIUM_USERNAME', 'msrexe')
MEDIUM_RSS_URL = f'https://medium.com/feed/@{MEDIUM_USERNAME}'
POSTS_DIR = Path('_posts')

def clean_filename(title):
    """Başlıktan geçerli bir dosya adı oluşturur."""
    # Türkçe karakterleri değiştir
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'
    }
    for tr_char, en_char in replacements.items():
        title = title.replace(tr_char, en_char)
    
    # Özel karakterleri temizle
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[-\s]+', '-', title)
    return title.strip('-')

def extract_first_image(content):
    """İçerikten ilk resmi çıkarır."""
    img_match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if img_match:
        return img_match.group(1)
    return None

def html_to_markdown(html_content):
    """HTML içeriği Markdown'a dönüştürür."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Satır sarma yapma
    markdown = h.handle(html_content)
    
    # Gereksiz boşlukları temizle
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown.strip()

def extract_description(content, max_length=200):
    """İçerikten kısa bir açıklama çıkarır."""
    # HTML etiketlerini temizle
    text = re.sub(r'<[^>]+>', '', content)
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    # İlk cümleyi veya max_length kadar karakteri al
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    return text

def get_existing_posts():
    """Mevcut post'ların Medium URL'lerini ve başlıklarını döndürür."""
    existing_data = {
        'urls': set(),
        'titles': set(),
        'slugs': set()
    }
    
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True)
        return existing_data
    
    for post_file in POSTS_DIR.glob('*.md'):
        try:
            post = frontmatter.load(post_file)
            # Medium URL'si varsa ekle
            if 'medium_url' in post.metadata:
                existing_data['urls'].add(post.metadata['medium_url'])
            # Başlık kontrolü
            if 'title' in post.metadata:
                existing_data['titles'].add(post.metadata['title'].lower().strip())
            # Slug kontrolü
            if 'slug' in post.metadata:
                existing_data['slugs'].add(post.metadata['slug'].lower().strip())
        except Exception as e:
            print(f"⚠️  {post_file} okunamadı: {e}")
    
    return existing_data

def sync_medium_posts():
    """Medium RSS feed'inden yazıları çeker ve Jekyll formatına dönüştürür."""
    print(f"📡 Medium feed'i kontrol ediliyor: @{MEDIUM_USERNAME}")
    
    feed = feedparser.parse(MEDIUM_RSS_URL)
    
    if feed.bozo:
        print(f"❌ RSS feed okunamadı: {feed.bozo_exception}")
        return
    
    existing_data = get_existing_posts()
    new_posts_count = 0
    
    for entry in feed.entries:
        medium_url = entry.link
        title_lower = entry.title.lower().strip()
        clean_title = clean_filename(entry.title)
        slug = clean_title.lower()
        
        # Çoklu kontrol: URL, başlık veya slug varsa atla
        if medium_url in existing_data['urls']:
            print(f"⏭️  Zaten mevcut (URL): {entry.title}")
            continue
        
        if title_lower in existing_data['titles']:
            print(f"⏭️  Zaten mevcut (Başlık): {entry.title}")
            continue
            
        if slug in existing_data['slugs']:
            print(f"⏭️  Zaten mevcut (Slug): {entry.title}")
            continue
        
        # Tarih bilgisini al
        published = datetime(*entry.published_parsed[:6])
        date_str = published.strftime('%Y-%m-%d')
        
        # Dosya adını oluştur
        clean_title = clean_filename(entry.title)
        filename = f"{date_str}-{clean_title}.md"
        filepath = POSTS_DIR / filename
        
        # İçeriği işle
        content = entry.get('content', [{}])[0].get('value', entry.get('summary', ''))
        markdown_content = html_to_markdown(content)
        
        # İlk resmi bul
        first_image = extract_first_image(content)
        
        # Açıklama oluştur
        description = extract_description(content)
        
        # Kategori çıkar (Medium'da tags varsa)
        categories = [tag.term for tag in entry.get('tags', [])]
        category = categories[0].lower() if categories else 'general'
        
        # Front matter oluştur
        post_data = {
            'layout': 'post',
            'title': entry.title,
            'description': description,
            'category': category,
            'slug': clean_title.lower(),
            'author': 'msrexe',
            'medium_url': medium_url,
            'date': published,
            'lang': 'tr'  # Medium'dan gelen yazılar Türkçe
        }
        
        if first_image:
            post_data['image'] = first_image
        
        # Post'u oluştur
        post = frontmatter.Post(markdown_content, **post_data)
        
        # Dosyaya yaz
        with open(filepath, 'wb') as f:
            frontmatter.dump(post, f)
        
        print(f"✅ Yeni yazı eklendi: {filename}")
        new_posts_count += 1
    
    if new_posts_count == 0:
        print("ℹ️  Yeni yazı bulunamadı.")
    else:
        print(f"🎉 {new_posts_count} yeni yazı eklendi!")

if __name__ == '__main__':
    sync_medium_posts()
