# 🎭 Sentiment Analysis Microservice

Bu proje, Türkçe metinlerin duygu analizini (Pozitif/Negatif) yapan, **FastAPI** (Backend) ve **Streamlit** (Frontend) tabanlı, Dockerize edilmiş bir mikroservis mimarisidir.

Model olarak `savasy/bert-base-turkish-sentiment-cased` kullanılmıştır.

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Projeyi klonlayın
git clone <REPO_URL_BURAYA_GELECEK>
cd omtekyav-sentiment-microservice

# 2. Modeli indirin
python indir.py

# 3. Docker ağı oluşturun
docker network create sentiment-net

# 4. Backend'i build edin ve çalıştırın
docker build -t sentiment-backend .
docker run -d -p 8000:8000 --network sentiment-net --name sentiment-backend sentiment-backend

# 5. Frontend'i build edin ve çalıştırın
docker build -t sentiment-frontend -f Dockerfile.ui .
docker run -d -p 8501:8501 --network sentiment-net --name sentiment-frontend -e API_URL="http://sentiment-backend:8000/api/v1/analyze" sentiment-frontend
```

**Uygulamayı kullanmak için:** 👉 [http://localhost:8501](http://localhost:8501)

---

## 📋 Ön Gereksinimler

- **Docker Desktop** (Çalışır durumda olmalı)
- **Python 3.8+** (Sadece modeli indirmek için gerekli)
- **Git**
- İnternet bağlantısı (model indirme için)

---

## 📂 Proje Yapısı

```
omtekyav-sentiment-microservice/
├── src/
│   ├── backend/
│   │   ├── app.py          # FastAPI uygulaması
│   │   ├── model_files/    # İndirilen model dosyaları
│   │   └── requirements.txt
│   └── frontend/
│       └── app.py          # Streamlit arayüzü
├── indir.py                # Model indirme scripti
├── Dockerfile             # Backend Dockerfile
├── Dockerfile.ui          # Frontend Dockerfile
└── README.md
```

---

## 🔧 Detaylı Kurulum Adımları

### 1. Projeyi İndirin

```bash
git clone <REPO_URL_BURAYA_GELECEK>
cd omtekyav-sentiment-microservice
```

### 2. Modeli Yerel Ortama İndirin (Kritik Adım!)

Docker imajını inşa etmeden önce, büyük model dosyalarını yerel klasöre indirmemiz gerekiyor. Bu işlem internet hızına bağlı olarak 400-500MB veri indirecektir.

*(Eğer `transformers` yüklü değilse önce: `pip install transformers torch`)*

```bash
python indir.py
```

✅ **Başarılı:** `src/model_files` klasörü oluşmalı ve içi dolu olmalıdır.

### 3. Docker Ağını Oluşturun

Backend ve Frontend konteynerlerinin haberleşebilmesi için özel bir bridge network oluşturuyoruz.

```bash
docker network create sentiment-net
```

### 4. Backend (API) Kurulumu

Model dosyalarıyla birlikte Backend imajını oluşturun ve çalıştırın.

**Build:**
```bash
docker build -t sentiment-backend .
```

**Run:**
```bash
docker run -d -p 8000:8000 --network sentiment-net --name sentiment-backend sentiment-backend
```

🔍 **Test:** Tarayıcıda `http://localhost:8000/docs` adresine giderek Swagger UI'ı görebilirsiniz.

### 5. Frontend (UI) Kurulumu

Arayüz için optimize edilmiş (Slim) imajı oluşturun ve Backend'e bağlayın.

**Build:**
```bash
docker build -t sentiment-frontend -f Dockerfile.ui .
```

**Run:**
```bash
docker run -d -p 8501:8501 --network sentiment-net --name sentiment-frontend -e API_URL="http://sentiment-backend:8000/api/v1/analyze" sentiment-frontend
```

---

## 🎮 Kullanım

1. Tarayıcınızda [http://localhost:8501](http://localhost:8501) adresine gidin
2. Metin kutusuna Türkçe bir metin girin
3. "Analiz Et" butonuna tıklayın
4. Sonuçları görün:
   - **Duygu Durumu:** Pozitif / Negatif
   - **Güven Skoru:** % olarak

### API Kullanımı

Backend API'yi doğrudan kullanmak için:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bu film gerçekten harikaydı!"}'
```

Yanıt:
```json
{
  "sentiment": "positive",
  "confidence": 0.98,
  "text": "Bu film gerçekten harikaydı!"
}
```

---

## ⚠️ Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

| Sorun | Çözüm |
|-------|--------|
| **"Container name already in use" hatası** | `docker rm -f sentiment-backend sentiment-frontend` |
| **Docker Build Hatası** | `src/model_files` klasörünün boş olmadığından emin olun (Adım 2) |
| **Model dosyaları indirilemedi** | `pip install transformers torch` yükleyip tekrar deneyin |
| **API bağlantı hatası** | `docker network ls` ile `sentiment-net` ağının oluştuğunu kontrol edin |
| **Port çakışması** | 8000 veya 8501 portlarını kullanan uygulamaları kapatın |

### Konteynerleri Yönetme

```bash
# Tüm konteynerleri durdur
docker stop sentiment-backend sentiment-frontend

# Tüm konteynerleri sil
docker rm sentiment-backend sentiment-frontend

# Logları görüntüle
docker logs sentiment-backend
docker logs sentiment-frontend

# Tüm konteynerleri yeniden başlat
docker start sentiment-backend sentiment-frontend
```

### Docker Ağını Temizleme

```bash
# Ağı sil
docker network rm sentiment-net

# Kullanılmayan kaynakları temizle
docker system prune -a
```

---

## 🛠️ Geliştirme

### Modeli Değiştirme

Farklı bir model kullanmak isterseniz:

1. `src/backend/app.py` dosyasındaki model adını değiştirin
2. Yeni modeli indirmek için `indir.py` scriptini güncelleyin
3. Docker konteynerlerini yeniden build edin

### Yerel Geliştirme

Backend'i yerel olarak çalıştırmak için:

```bash
cd src/backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Frontend'i yerel olarak çalıştırmak için:

```bash
cd src/frontend
pip install streamlit
streamlit run app.py
```

---

## 📊 Teknik Özellikler

- **Backend:** FastAPI, Python 3.9, Transformers
- **Frontend:** Streamlit, Python 3.9
- **Model:** bert-base-turkish-sentiment-cased
- **Docker:** Multi-stage builds, lightweight containers
- **API:** RESTful, JSON-based, CORS enabled

---

## 📝 Lisans

Bu proje açık kaynaklıdır. Model Hugging Face üzerinden sağlanmaktadır.

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

**Not:** `<REPO_URL_BURAYA_GELECEK>` kısmını kendi repository URL'nizle değiştirmeyi unutmayın.
