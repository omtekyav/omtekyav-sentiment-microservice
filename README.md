![Test Pipeline](https://github.com/omtekyav/omtekyav-sentiment-microservice/actions/workflows/test.yml/badge.svg)

<div align="center">

# 🎭 Türkçe Duygu Analizi Mikroservisi
### Production-Ready Turkish Sentiment Analysis Architecture

**Analiz Et. Sınıflandır. Ölçekle.**
<br>
FastAPI backend, Streamlit frontend ve BERT mimarisi ile güçlendirilmiş, Dockerize edilmiş duygu analizi servisi.

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Build Status](https://github.com/omtekyav/omtekyav-sentiment-microservice/actions/workflows/test.yml/badge.svg)](https://github.com/omtekyav/omtekyav-sentiment-microservice/actions)
[![License](https://img.shields.io/badge/license-MIT-yellow)](./LICENSE)

[🔴 Canlı Demo (Local)](http://localhost:8501) · [🐞 Hata Bildir](https://github.com/omtekyav/omtekyav-sentiment-microservice/issues) · [✨ Özellik İste](https://github.com/omtekyav/omtekyav-sentiment-microservice/issues)


</div>

---

FastAPI backend ve Streamlit frontend ile oluşturulmuş, Docker Compose ile containerize edilmiş Türkçe metin duygu analizi mikroservis mimarisi. Model olarak `savasy/bert-base-turkish-sentiment-cased` kullanılmaktadır.

---

## 🚀 Hızlı Başlangıç

### Kurulum
```bash
# 1. Önce projeyi indir
git clone https://github.com/omtekyav/omtekyav-sentiment-microservice.git

# 2. İndirdiğin klasörünün içine gir.
cd omtekyav-sentiment-microservice

# 3. Şimdi modeli indir
python indir.py

# Docker'ı başlat(docker desktop app açık olması lazım)
docker-compose up --build
```

### Erişim
- **Web Arayüzü:** [http://localhost:8501](http://localhost:8501)
- **API Dokümantasyonu:** [http://localhost:8000/docs](http://localhost:8000/docs)

 **Uygulamayı açmak için şu adresi kullanın:**
 **http://localhost:8501**
<img width="1888" height="437" alt="image" src="https://github.com/user-attachments/assets/bc2264e7-1c7e-429b-9304-d337eee84e53" />

---

## 📋 Sistem Gereksinimleri

- **Docker Engine:** 20.10+ 
- **Docker Compose:** 2.0+
- **Python:** 3.8+ (model indirme için)
- **RAM:** Minimum 4GB
- **Disk:** 2GB boş alan

---

## 🏗️ Mimarisi

### Servis Yapısı
```
omtekyav-sentiment-microservice/
├── .github/
│   └── workflows/
│       └── test.yml          # CI/CD Otomasyonu (GitHub Actions)
├── images/                   # Dokümantasyon ekran görüntüleri
├── src/                      # Kaynak kodlar
│   ├── api/
│   │   └── routes.py         # API Endpoint'leri ve Router yapısı
│   ├── model/
│   │   └── sentiment_model.py # BERT Modeli ve Tahminleme Sınıfı
│   ├── model_files/          # İndirilen Model Dosyaları (Git'te yok, lokalde oluşur)
│   ├── ui/
│   │   └── app.py            # Streamlit Frontend Arayüzü
│   ├── main.py               # FastAPI Giriş Noktası ve Konfigürasyon
│   ├── schemas.py            # Pydantic Veri Modelleri (Request/Response)
│   └── services.py           # İş Mantığı (Business Logic)
├── tests/                    # Test Klasörü
│   ├── __init__.py
│   └── test_api.py           # API Testleri (Mocking & Dependency Injection)
├── docker-compose.yml        # Konteyner Orkestrasyonu (Tek komutla başlatma)
├── Dockerfile                # Backend İmaj Tarifi (Optimize: Slim + Non-root)
├── Dockerfile.ui             # Frontend İmaj Tarifi
├── indir.py                  # Modeli HuggingFace'den indiren script
├── pytest.ini                # Pytest Konfigürasyon Dosyası
├── requirements.txt          # Backend Bağımlılıklar
└── requirements-ui.txt       # Frontend Bağımlılıklar
```

### Teknoloji Stack'i
| Bileşen | Teknoloji | Versiyon |
|---------|-----------|----------|
| **Backend** | FastAPI, PyTorch, Transformers | 0.95+ |
| **Frontend** | Streamlit | 1.22+ |
| **Model** | BERT-base Turkish | cased |
| **Container** | Docker, Docker Compose | 20.10+ |
| **API Format** | REST, JSON | - |

---

## 🔌 API Endpoints

### 1. Duygu Analizi
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Örnek Türkçe metin"
}
```

**Response:**
```json
{
  "sentiment": "positive|negative",
  "confidence": 0.95,
  "text": "Örnek Türkçe metin",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Sistem Sağlığı
```http
GET /health
```

### 3. Model Bilgileri
```http
GET /api/v1/model-info
```

---

## 🐳 Container Yönetimi

### Temel Komutlar
```bash
# Development modunda başlat
docker-compose up --build

# Detached modda çalıştır
docker-compose up -d

# Servis durumunu kontrol et
docker-compose ps

# Logları izle
docker-compose logs -f [service_name]

# Servisi durdur
docker-compose down

# Volume'lerle birlikte temizle
docker-compose down -v

# Belirli servisi yeniden başlat
docker-compose restart backend
```

### Production Deployment
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# Volume persistency
docker volume create model-storage
```

---

## 🔧 Konfigürasyon

### Environment Variables
```env
# Backend
MODEL_PATH=/app/model
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info

# Frontend
STREAMLIT_SERVER_PORT=8501
API_BASE_URL=http://backend:8000
```

### Port Mapping
| Servis | Container Port | Host Port | Protokol |
|--------|---------------|-----------|----------|
| Backend | 8000 | 8000 | HTTP |
| Frontend | 8501 | 8501 | HTTP |

---

## 🧪 Test ve Validasyon

### API Testleri
```bash
# API endpoint testi
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ürün kalitesinden çok memnun kaldım"}'

# Health check
curl http://localhost:8000/health

# Model bilgisi
curl http://localhost:8000/api/v1/model-info
```


## 🚨 Sorun Giderme

### Sık Karşılaşılan Sorunlar

**1. Model İndirme Hatası**
```bash
# Transformers kütüphanesini kontrol et
pip show transformers

# Model dosyalarını manuel indir
python download_model.py --force
```

**2. Docker Port Çakışması**
```bash
# Kullanılan portları listele
sudo lsof -i :8000
sudo lsof -i :8501

# Alternatif portlarla başlat
docker-compose -f docker-compose.yml \
  --env-file .env.alternative up
```

**3. Yetersiz Bellek**
```bash
# Docker memory limit'ini artır
# docker-compose.yml içinde:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Monitoring Komutları
```bash
# Container kaynak kullanımı
docker stats

# Container log'ları
docker-compose logs --tail=50 backend

# Network connectivity test
docker-compose exec backend ping frontend
```

---

## 📈 Performans Optimizasyonu

### Önerilen Ayarlar
1. **Model Caching:** Transformers cache mekanizması aktif
2. **Batch Processing:** API batch endpoint'i eklenebilir
3. **GPU Support:** CUDA enabled container kullanımı
4. **Load Balancing:** Traefik veya Nginx reverse proxy

### Scaling
```yaml
# docker-compose.scale.yml
services:
  backend:
    image: sentiment-backend:latest
    deploy:
      replicas: 3
    environment:
      - WORKERS_PER_CORE=2
```

---

## 🔐 Güvenlik

### Best Practices
1. **API Rate Limiting:** Implement rate limiting middleware
2. **Input Validation:** Pydantic models for request validation
3. **CORS Configuration:** Restrict origins in production
4. **Environment Variables:** Secrets management via .env files

### Production Hardening
```python
# CORS configuration example
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["POST"],
    max_age=3600
)
```

---


### Development Setup
```bash
# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Geliştirme bağımlılıklarını yükle
pip install -r requirements-dev.txt

# Pre-commit hooks kur
pre-commit install
```

---

##  Destek ve İletişim

- **Issue Tracker:** [GitHub Issues](https://github.com/omtekyav/omtekyav-sentiment-microservice.git)
- **Documentation:** [API Docs](http://localhost:8000/docs)
- **Model Card:** [Hugging Face](https://huggingface.co/savasy/bert-base-turkish-sentiment-cased)

---

*Son Güncelleme: Aralık 2025 | Versiyon: 1.0.0*





