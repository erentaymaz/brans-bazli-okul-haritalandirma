# Render.com'da Deployment Rehberi

Bu rehber, Okul Haritası API'sini Render.com'da nasıl deploy edeceğinizi adım adım açıklar.

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler
- GitHub hesabı
- Render.com hesabı (ücretsiz)
- Projeniz GitHub'da bir repository'de olmalı

## 📝 Adım Adım Deployment

### 1. GitHub'a Projeyi Yükleyin

```bash
# Git repository oluşturun (henüz yoksa)
git init

# Dosyaları ekleyin
git add .

# Commit yapın
git commit -m "Initial commit - Okul Haritası API"

# GitHub'a push edin
git remote add origin https://github.com/KULLANICI_ADINIZ/okul-haritasi-api.git
git branch -M main
git push -u origin main
```

### 2. Render.com'da Web Service Oluşturun

1. **Render.com'a gidin**: https://render.com
2. **Sign Up / Log In** yapın (GitHub ile giriş yapabilirsiniz)
3. **Dashboard**'da **"New +"** butonuna tıklayın
4. **"Web Service"** seçeneğini seçin

### 3. Repository'yi Bağlayın

1. GitHub repository'nizi seçin veya bağlayın
2. Render.com'un repository'nize erişim izni verin

### 4. Yapılandırma Ayarları

Aşağıdaki ayarları yapın:

#### Temel Ayarlar
- **Name**: `okul-haritasi-api` (veya istediğiniz bir isim)
- **Region**: `Frankfurt (EU Central)` (size en yakın bölgeyi seçin)
- **Branch**: `main`
- **Root Directory**: (boş bırakın)
- **Runtime**: `Python 3`

#### Build & Deploy Ayarları
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command**: 
  ```bash
  uvicorn api:app --host 0.0.0.0 --port $PORT
  ```

#### Environment Variables (Ortam Değişkenleri)
- **PYTHON_VERSION**: `3.11.0`

#### Plan
- **Free** planı seçin (0$/ay)

### 5. Deploy Edin

1. **"Create Web Service"** butonuna tıklayın
2. Render.com otomatik olarak:
   - Kodu çekecek
   - Bağımlılıkları yükleyecek
   - Uygulamayı başlatacak

### 6. Deployment Tamamlandı! 🎉

Deploy tamamlandığında, size şuna benzer bir URL verilecek:
```
https://okul-haritasi-api.onrender.com
```

## 🔍 API'yi Test Edin

### Ana Sayfa
```
https://okul-haritasi-api.onrender.com/
```

### Swagger Dokümantasyonu
```
https://okul-haritasi-api.onrender.com/docs
```

### Harita Görüntüleme
```
https://okul-haritasi-api.onrender.com/harita/okullar-sehitkamil
```

### Okulları Listele
```
https://okul-haritasi-api.onrender.com/okullar/okullar-sehitkamil
```

## 📊 Önemli Notlar

### Free Plan Özellikleri
- ✅ 750 saat/ay ücretsiz çalışma süresi
- ✅ Otomatik HTTPS
- ✅ Otomatik deploy (her push'ta)
- ⚠️ 15 dakika inaktivite sonrası uyku moduna geçer
- ⚠️ İlk istek sonrası uyanması 30-60 saniye sürebilir

### Uyku Modunu Önlemek İçin
Ücretsiz planda uyku modunu tamamen önleyemezsiniz, ancak:
- Paid plana geçerek 7$/ay ödeyebilirsiniz
- Veya bir cron job ile her 10 dakikada bir ping atabilirsiniz

## 🔄 Otomatik Deployment

Her GitHub push'unda Render.com otomatik olarak yeniden deploy eder:

```bash
# Değişiklik yapın
git add .
git commit -m "API güncellendi"
git push

# Render.com otomatik olarak yeniden deploy edecek
```

## 🛠️ Alternatif: render.yaml ile Deploy

Proje dizininde `render.yaml` dosyası var. Bu dosya ile:

1. Render Dashboard'da **"New +"** → **"Blueprint"** seçin
2. Repository'nizi seçin
3. `render.yaml` otomatik algılanacak
4. **"Apply"** butonuna tıklayın

## 📝 JSON Dosyalarını Yükleme

Okul JSON dosyalarınızı da projeye ekleyin:

```bash
# JSON dosyalarını projeye ekleyin
git add okullar-sehitkamil.json
git add okullar-sahinbey.json
git commit -m "Okul verileri eklendi"
git push
```

## 🔧 Sorun Giderme

### Build Hatası
- **Logs** sekmesinden hata mesajlarını kontrol edin
- `requirements.txt` dosyasının doğru olduğundan emin olun

### Start Hatası
- Start Command'in doğru olduğundan emin olun
- Environment Variables'ın doğru ayarlandığından emin olun

### 502 Bad Gateway
- Uygulamanın başlaması biraz zaman alabilir
- Logs'u kontrol edin

## 📞 Destek

Render.com dokümantasyonu: https://render.com/docs

## 🎯 Sonraki Adımlar

1. ✅ API'yi test edin
2. ✅ Custom domain ekleyin (opsiyonel)
3. ✅ Environment variables ekleyin (gerekirse)
4. ✅ Monitoring ve logs'u takip edin

Başarılar! 🚀

