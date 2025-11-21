from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
import os
import requests
import time

app = FastAPI(
    title="Okul Haritası API",
    description="Okul verilerini harita üzerinde göstermek için API",
    version="1.0.0"
)

# CORS ayarları - Frontend'den erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da belirli domainlere izin verin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Pydantic Modelleri
# -------------------------------
class Okul(BaseModel):
    adi: str
    il: str
    ilce: str
    zorunlu_hizmet: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CoordinateRequest(BaseModel):
    address: str


class CoordinateResponse(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    address: str


class MapRequest(BaseModel):
    json_file: str


# -------------------------------
# Yardımcı Fonksiyonlar
# -------------------------------
def get_coordinates(address: str):
    """Nominatim üzerinden geocoding yapan fonksiyon"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }

    try:
        response = requests.get(url, params=params, headers={'User-Agent': 'SchoolMapper/1.0'})
        data = response.json()

        if len(data) == 0:
            return None, None

        return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding hatası: {e}")
        return None, None


def load_json_file(filename: str) -> Dict:
    """JSON dosyasını yükler"""
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail=f"Dosya bulunamadı: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON okuma hatası: {str(e)}")


def save_json_file(filename: str, data: Dict):
    """JSON dosyasını kaydeder"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON yazma hatası: {str(e)}")


# -------------------------------
# API Endpoints
# -------------------------------

@app.get("/")
async def root():
    """API ana sayfası"""
    return {
        "message": "Okul Haritası API'ye hoş geldiniz!",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API bilgileri",
            "GET /okullar": "Tüm JSON dosyalarını listele",
            "GET /okullar/{filename}": "Belirli bir JSON dosyasını getir",
            "POST /geocode": "Adres için koordinat bul",
            "POST /okullar/{filename}/process": "Okul verilerini işle ve koordinat ekle",
            "GET /harita/{filename}": "HTML harita oluştur",
            "GET /docs": "API dokümantasyonu (Swagger UI)"
        }
    }


@app.get("/okullar")
async def list_school_files():
    """Mevcut okul JSON dosyalarını listeler"""
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'okullar' in f]
    return {
        "files": json_files,
        "count": len(json_files)
    }


@app.get("/okullar/{filename}")
async def get_schools(filename: str):
    """Belirli bir JSON dosyasındaki okul verilerini getirir"""
    if not filename.endswith('.json'):
        filename += '.json'
    
    data = load_json_file(filename)
    
    # İstatistikler
    total = len(data)
    with_coords = sum(1 for okul in data.values() if okul.get('latitude') and okul.get('longitude'))
    
    return {
        "filename": filename,
        "total_schools": total,
        "schools_with_coordinates": with_coords,
        "schools_without_coordinates": total - with_coords,
        "data": data
    }


@app.post("/geocode", response_model=CoordinateResponse)
async def geocode_address(request: CoordinateRequest):
    """Verilen adres için koordinat bulur"""
    lat, lon = get_coordinates(request.address)
    
    return CoordinateResponse(
        latitude=lat,
        longitude=lon,
        address=request.address
    )


@app.post("/okullar/{filename}/process")
async def process_schools(filename: str, delay: float = 1.0):
    """
    Okul verilerini işler ve eksik koordinatları ekler
    
    - **filename**: İşlenecek JSON dosyası
    - **delay**: Her geocoding isteği arasındaki bekleme süresi (saniye)
    """
    if not filename.endswith('.json'):
        filename += '.json'
    
    okullar = load_json_file(filename)
    
    processed = 0
    skipped = 0
    failed = 0
    
    for key, okul in okullar.items():
        # Zaten koordinatı varsa atla
        if okul.get('latitude') and okul.get('longitude'):
            skipped += 1
            continue
        
        full_address = f"{okul['adi']}, {okul['ilce']}, {okul['il']}, Türkiye"
        print(f"İşleniyor: {full_address}")
        
        lat, lon = get_coordinates(full_address)
        
        if lat and lon:
            okul['latitude'] = lat
            okul['longitude'] = lon
            processed += 1
        else:
            failed += 1
        
        # Rate limiting için bekleme
        time.sleep(delay)
    
    # Güncellenmiş veriyi kaydet
    output_filename = filename.replace('.json', '_koordinatli.json')
    save_json_file(output_filename, okullar)
    
    return {
        "message": "İşlem tamamlandı",
        "input_file": filename,
        "output_file": output_filename,
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
        "total": len(okullar)
    }


@app.get("/harita/{filename}", response_class=HTMLResponse)
async def create_map(filename: str):
    """
    Belirli bir JSON dosyası için HTML harita oluşturur
    
    - **filename**: JSON dosya adı (örn: okullar-sehitkamil)
    """
    if not filename.endswith('.json'):
        filename += '.json'
    
    okullar = load_json_file(filename)
    
    # Harita merkezini hesapla
    valid_coords = []
    for okul in okullar.values():
        if okul.get('latitude') and okul.get('longitude'):
            try:
                lat = float(okul['latitude'])
                lon = float(okul['longitude'])
                valid_coords.append((lat, lon))
            except (ValueError, TypeError):
                continue
    
    if not valid_coords:
        center_lat, center_lon = 37.06, 37.38
        zoom = 11
    else:
        center_lat = sum(c[0] for c in valid_coords) / len(valid_coords)
        center_lon = sum(c[1] for c in valid_coords) / len(valid_coords)
        zoom = 12
    
    json_filename = os.path.basename(filename)
    ilce_adi = json_filename.replace('.json', '').replace('okullar-', '').upper()
    
    # Okulları JavaScript array'e dönüştür
    schools_json = json.dumps(okullar, ensure_ascii=False)
    
    html_content = f'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Okul Haritası - {ilce_adi}</title>

  <!-- Leaflet CSS -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  />

  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
    }}
    #map {{
      height: 100vh;
      width: 100%;
    }}
    .info-box {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: white;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      z-index: 1000;
      max-width: 250px;
    }}
    .info-box h3 {{
      margin: 0 0 10px 0;
      font-size: 16px;
      color: #333;
    }}
    .info-box p {{
      margin: 5px 0;
      font-size: 14px;
      color: #666;
    }}
  </style>
</head>
<body>
  <div id="map"></div>
  <div class="info-box">
    <h3 id="title">{ilce_adi}</h3>
    <p id="school-count">Toplam {len(valid_coords)} okul</p>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <script>
    // JSON verisi direkt olarak embed edildi
    const data = {schools_json};

    // Harita başlangıç konumu
    const map = L.map("map").setView([{center_lat}, {center_lon}], {zoom});

    // OpenStreetMap layer
    L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }}).addTo(map);

    let schoolCount = 0;

    // Okulları marker olarak ekle
    for (const key in data) {{
      const okul = data[key];

      if (!okul.latitude || !okul.longitude) continue;

      const lat = parseFloat(okul.latitude);
      const lon = parseFloat(okul.longitude);

      if (isNaN(lat) || isNaN(lon)) continue;

      const marker = L.marker([lat, lon]).addTo(map);

      marker.bindPopup(
        `<b>${{okul.adi}}</b><br>
         ${{okul.il}} / ${{okul.ilce}}<br>
         Hizmet Süresi: ${{okul.zorunlu_hizmet}}`
      );

      schoolCount++;
    }}

    console.log(`Toplam ${{schoolCount}} okul haritaya eklendi`);
  </script>
</body>
</html>
'''
    
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {
        "status": "healthy",
        "message": "API çalışıyor"
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

