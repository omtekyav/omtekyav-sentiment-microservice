# 🎭 Türkçe Duygu Analizi Mikroservisi

FastAPI backend ve Streamlit frontend ile oluşturulmuş, Docker Compose ile containerize edilmiş Türkçe metin duygu analizi mikroservis mimarisi. Model olarak `savasy/bert-base-turkish-sentiment-cased` kullanılmaktadır.

---

## 🚀 Hızlı Başlangıç

### Kurulum
```bash
# 1. Repository'yi klonlayın
git clone https://github.com/omtekyav/omtekyav-sentiment-microservice.git
cd sentiment-analysis-microservice

# 2. Hugging Face modelini indirin (ilk kurulum)
python download_model.py

# 3. Docker konteynerlerini başlatın
docker-compose up --build
```

### Erişim
- **Web Arayüzü:** [http://localhost:8501](http://localhost:8501)
- **API Dokümantasyonu:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

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
sentiment-analysis-microservice/
├── backend/           # FastAPI mikroservisi
│   ├── app.py         # API endpoint'leri
│   ├── model/         # Fine-tuned BERT modeli
│   └── Dockerfile     # Backend container tanımı
├── frontend/          # Streamlit arayüzü
│   ├── app.py         # Web arayüzü
│   └── Dockerfile     # Frontend container tanımı
├── docker-compose.yml # Multi-container orkestrasyon
└── download_model.py  # Model indirme scripti
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

### Performans Testi
```bash
# Load testing (örn. Apache Bench)
ab -n 100 -c 10 -p test_data.json -T application/json \
  http://localhost:8000/api/v1/analyze
```

---

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

## 📊 Model Performansı

### Doğruluk Metrikleri
| Dataset | Accuracy | Precision | Recall | F1-Score |
|---------|----------|-----------|--------|----------|
| Turkish Movie Reviews | 92.3% | 91.8% | 92.1% | 91.9% |
| Product Reviews | 89.7% | 90.2% | 88.9% | 89.5% |

### Örnek Çıktılar
```json
{
  "positive_example": {
    "text": "Müşteri hizmetleri çok ilgili ve hızlıydı",
    "sentiment": "positive",
    "confidence": 0.97
  },
  "negative_example": {
    "text": "Ürün beklentilerimin çok altında kaldı",
    "sentiment": "negative", 
    "confidence": 0.93
  }
}
```

---

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/improvement`)
3. Değişikliklerinizi commit edin (`git commit -am 'Add new feature'`)
4. Branch'inize push edin (`git push origin feature/improvement`)
5. Pull Request oluşturun

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

## 📞 Destek ve İletişim

- **Issue Tracker:** [GitHub Issues](https://github.com/omtekyav/omtekyav-sentiment-microservice.git)
- **Documentation:** [API Docs](http://localhost:8000/docs)
- **Model Card:** [Hugging Face](https://huggingface.co/savasy/bert-base-turkish-sentiment-cased)

---

*Son Güncelleme: Ocak 2024 | Versiyon: 1.0.0*

