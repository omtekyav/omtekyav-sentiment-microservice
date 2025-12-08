# 🎭 Sentiment Analysis Microservice

Bu proje, Türkçe metinlerin duygu analizini (Pozitif/Negatif) yapan, **FastAPI** (Backend) ve **Streamlit** (Frontend) tabanlı, Dockerize edilmiş bir mikroservis mimarisidir.

Model olarak `savasy/bert-base-turkish-sentiment-cased` kullanılmıştır.

---

## 🚀 Çok Hızlı Kurulum (Docker Compose ile)

Tüm sistemi tek komutla ayağa kaldırmak için:

### 1. **Projeyi indirin:**
```bash
git clone <REPO_URL_BURAYA_GELECEK>
cd omtekyav-sentiment-microservice
```

### 2. **Modeli indirin (Sadece ilk kurulumda 1 kez):**
```bash
python indir.py
```
**Not:** Bu adım internet hızına bağlı olarak 400-500MB veri indirecektir.

### 3. **Sistemi başlatın:**
```bash
docker-compose up --build
```

🎉 **Bitti!** Tarayıcıda `http://localhost:8501` adresine gidin.

---

## 📋 Ön Gereksinimler

- **Docker** ve **Docker Compose** (Çalışır durumda olmalı)
- **Python 3.8+** (Sadece modeli indirmek için)
- **Git**
- İnternet bağlantısı (model indirme için)

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

## ⚡ Hızlı Komutlar

```bash
# Sistemi başlat (arka planda)
docker-compose up -d

# Sistem durumunu kontrol et
docker-compose ps

# Logları görüntüle
docker-compose logs -f

# Sistemi durdur
docker-compose down

# Sistemi tamamen temizle
docker-compose down -v

# Yeniden başlat
docker-compose restart
```

---

## ⚠️ Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

| Sorun | Çözüm |
|-------|--------|
| **"Model dosyaları bulunamadı"** | `python indir.py` ile modeli indirin |
| **Port çakışması** | `sudo lsof -i :8000` ve `sudo lsof -i :8501` ile kontrol edin |
| **Docker Compose hataları** | `docker-compose --version` ile sürümü kontrol edin |
| **Yetersiz disk alanı** | `docker system prune -a` ile temizlik yapın |

---

## 🛠️ Geliştirme

### Yerel Geliştirme

Backend'i yerel olarak çalıştırmak için:

```bash
cd src/backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Frontend'i yerel olarak çalıştırın:

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
- **API:** RESTful, JSON-based, CORS enabled
- **Deployment:** Docker Compose, Multi-stage builds

---

## 📝 Lisans

Bu proje açık kaynaklıdır. Model Hugging Face üzerinden sağlanmaktadır.

---

**Not:** `<REPO_URL_BURAYA_GELECEK>` kısmını kendi repository URL'nizle değiştirmeyi unutmayın.
