# Okul Haritası API

Bu proje, okul verilerini harita üzerinde göstermek için geliştirilmiş bir REST API'dir.

## Özellikler

- ✅ Okul verilerini JSON formatında saklama
- ✅ Adres bilgilerinden otomatik koordinat bulma (Geocoding)
- ✅ İnteraktif harita oluşturma
- ✅ RESTful API endpoints
- ✅ Swagger UI dokümantasyonu
- ✅ CORS desteği

## Kurulum

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Çalıştırma

```bash
python api.py
```

veya

```bash
uvicorn api:app --reload
```

API şu adreste çalışacak: `http://localhost:8000`

## API Endpoints

### 📍 Ana Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/` | API bilgileri |
| GET | `/docs` | Swagger UI dokümantasyonu |
| GET | `/health` | Sağlık kontrolü |

### 🏫 Okul Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/okullar` | Tüm JSON dosyalarını listele |
| GET | `/okullar/{filename}` | Belirli bir dosyadaki okulları getir |
| POST | `/okullar/{filename}/process` | Okul verilerini işle ve koordinat ekle |

### 🗺️ Harita Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/harita/{filename}` | HTML harita oluştur |

### 📍 Geocoding Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/geocode` | Adres için koordinat bul |

## Kullanım Örnekleri

### 1. Tüm Okul Dosyalarını Listele

```bash
curl http://localhost:8000/okullar
```

### 2. Belirli Bir Dosyadaki Okulları Getir

```bash
curl http://localhost:8000/okullar/okullar-sehitkamil
```

### 3. Okul Verilerini İşle (Koordinat Ekle)

```bash
curl -X POST http://localhost:8000/okullar/okullar-sehitkamil/process
```

### 4. Harita Oluştur

Tarayıcıda aç:
```
http://localhost:8000/harita/okullar-sehitkamil
```

### 5. Adres için Koordinat Bul

```bash
curl -X POST http://localhost:8000/geocode \
  -H "Content-Type: application/json" \
  -d '{"address": "Gaziantep Üniversitesi, Şehitkamil, Gaziantep"}'
```

## Swagger UI

API dokümantasyonuna ve test arayüzüne erişmek için:

```
http://localhost:8000/docs
```

## Deployment

### Render.com (Önerilen - Ücretsiz)

#### Hızlı Deployment

1. **GitHub'a push edin**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADINIZ/okul-haritasi-api.git
git push -u origin main
```

2. **Render.com'da Web Service oluşturun**:
   - https://render.com adresine gidin
   - "New +" → "Web Service" seçin
   - GitHub repository'nizi bağlayın

3. **Ayarları yapın**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: `3.11.0`

4. **Deploy edin** ve URL'nizi alın!

📖 **Detaylı rehber için**: `RENDER_DEPLOYMENT.md` dosyasına bakın

### Railway.app

1. GitHub'a push edin
2. Railway.app'e giriş yapın
3. "New Project" → "Deploy from GitHub repo"
4. Repository'nizi seçin
5. Otomatik deploy edilecek

### Heroku

1. `Procfile` oluşturun:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

2. Deploy edin:
```bash
heroku create okul-haritasi-api
git push heroku main
```

### Docker

1. `Dockerfile` oluşturun:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build ve çalıştır:
```bash
docker build -t okul-haritasi-api .
docker run -p 8000:8000 okul-haritasi-api
```

## Ortam Değişkenleri

Gerekirse `.env` dosyası oluşturun:

```env
PORT=8000
HOST=0.0.0.0
ALLOWED_ORIGINS=*
```

## Lisans

MIT

## Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

