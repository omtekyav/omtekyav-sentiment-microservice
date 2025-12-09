"""
API endpoint testleri (Mock kullanarak hızlı test).
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.routes import get_sentiment_service
from src.schemas import SentimentResponse

# ✅ DOĞRU MOCK: SentimentResponse döndürür
class MockSentimentService:
    """Gerçek modeli yüklemeden test yapmak için sahte servis."""
    
    def __init__(self):
        self.stats = {
            "Pozitif": 0,
            "Negatif": 0,
            "Nötr": 0,
            "Total": 0
        }
    
    def analyze_text(self, text: str) -> SentimentResponse:
        """
        Sahte analiz: Metinde 'kötü' varsa Negatif, yoksa Pozitif döndürür.
        GERÇEKTEKİ GİBİ SentimentResponse nesnesi döndürür!
        """
        if "kötü" in text.lower() or "berbat" in text.lower():
            sentiment = "Negatif"
            confidence = 1.0
        else:
            sentiment = "Pozitif"
            confidence = 0.95
        
        # İstatistik güncelle (gerçek servis gibi)
        self.stats[sentiment] += 1
        self.stats["Total"] += 1
        
        return SentimentResponse(
            sentiment=sentiment,
            confidence=confidence
        )
    
    def get_statistics(self):
        """Sahte istatistikler döndürür."""
        return self.stats

_mock_instance  = MockSentimentService()
# ✅ DOĞRU OVERRIDE: Lambda ile instance döndürüyoruz
def get_mock_service():
    """Test için mock service döndüren factory."""
    return _mock_instance

# FastAPI'ye: "Test sırasında get_sentiment_service yerine bunu kullan"
app.dependency_overrides[get_sentiment_service] = get_mock_service

# Test client oluştur
client = TestClient(app)


# ============================================
# TEST SENARYOLARI
# ============================================

class TestRootEndpoint:
    """Root endpoint testleri."""
    
    def test_root_accessible(self):
        """✅ Ana sayfa erişilebilir olmalı."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Sentiment Analysis" in response.json()["message"]
        print("\n✅ Root endpoint testi başarılı")


class TestAnalyzeEndpointWithMock:
    """Mock servis ile hızlı testler (model yüklenmez)."""
    
    def test_positive_sentiment_mock(self):
        """✅ Pozitif metin (mock ile) doğru analiz edilmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "Harika bir ürün çok beğendim"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["sentiment"] == "Pozitif"
        assert data["confidence"] == 0.95
        print("\n✅ Pozitif sentiment testi başarılı (Mock)")
    
    def test_negative_sentiment_mock(self):
        """✅ Negatif metin (mock ile) doğru analiz edilmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "Berbat bir deneyim"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["sentiment"] == "Negatif"
        assert data["confidence"] == 1.0
        print("\n✅ Negatif sentiment testi başarılı (Mock)")
    
    def test_empty_text_validation(self):
        """❌ Boş metin validation hatası dönmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": ""}
        )
        
        assert response.status_code == 422  # Validation Error
        print("\n✅ Boş metin validation testi başarılı")
    
    def test_short_text_validation(self):
        """❌ Kısa metin (5 karakterden az) reddedilmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "test"}
        )
        
        assert response.status_code == 422
        print("\n✅ Kısa metin validation testi başarılı")
    
    def test_no_letters_validation(self):
        """❌ Harf içermeyen metin reddedilmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "12345 @#$%"}
        )
        
        assert response.status_code == 422
        print("\n✅ Harf kontrolü testi başarılı")
    
    def test_whitespace_only_validation(self):
        """❌ Sadece boşluk reddedilmeli."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "     "}
        )
        
        assert response.status_code == 422
        print("\n✅ Boşluk kontrolü testi başarılı")


class TestStatsEndpointWithMock:
    """İstatistik endpoint testleri (mock ile)."""
    
    def test_stats_accessible(self):
        """✅ Stats endpoint erişilebilir olmalı."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        print("\n✅ Stats endpoint testi başarılı")
    
    def test_stats_structure(self):
        """✅ Stats doğru yapıda veri döndürmeli."""
        response = client.get("/api/v1/stats")
        data = response.json()
        
        required_keys = ["Pozitif", "Negatif", "Nötr", "Total"]
        assert all(key in data for key in required_keys)
        print("\n✅ Stats yapı testi başarılı")
    
    def test_stats_increment_after_mock_analysis(self):
        """✅ Mock analiz sonrası istatistikler artmalı."""
        # İlk durum
        initial_stats = client.get("/api/v1/stats").json()
        initial_total = initial_stats["Total"]
        
        # Analiz yap
        client.post(
            "/api/v1/analyze",
            json={"text": "Test mesajı güzel"}
        )
        
        # Yeni durum
        new_stats = client.get("/api/v1/stats").json()
        new_total = new_stats["Total"]
        
        assert new_total == initial_total + 1
        print("\n✅ Stats artış testi başarılı")