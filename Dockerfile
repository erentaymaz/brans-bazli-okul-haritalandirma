FROM python:3.11-slim

WORKDIR /app

# Gerekli paketleri kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port
EXPOSE 8000

# Uygulamayı çalıştır
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

