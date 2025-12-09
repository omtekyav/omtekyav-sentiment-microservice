from fastapi import APIRouter,HTTPException, Depends
from src.schemas import SentimentRequest, SentimentResponse
# Başka dosyadan (services.py) "SentimentService" tarifini getir dedik.
from src.services import SentimentService

#router garson tanımlanıyor
router = APIRouter()

# --- 1. TEDARİKÇİ (Dependency Provider) ---
# Gerçek servisi hafızada tutan değişken (Singleton)
# Global instance (gerçek servis)'i hhafızada tutan değişken
_real_service = SentimentService()

#--ESKİ VERSİYON--
#müdür başlatılıyor service INSTANTIATION (İşe Alma / Yaratma)
#"Bu tarife göre bana canlı kanlı bir çalışan (nesne) ver
# Artık elimizde "sentiment_service" adında, hafızası olan bir çalışan var.
#"Restoran açıldı (App start), Şefi mutfağa koy, defterini eline ver ve bekle."
#sentiment_service = SentimentService() 




def get_sentiment_service():
    """
    Bu fonksiyon, endpoint'lere SentimentService sağlar.
    Test yaparken bu fonksiyonu 'Override' edip SAHTE servis vereceğiz.
    """
    return _real_service

# --- 2. ENDPOINT (Dependency Injection Uygulanmış) ---
# kapı 1. analiz kapısı post > endpoint DEPENDENCY INJECTİON uygunalnmıs kısım
@router.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(
    request:SentimentRequest,
    #SERVİS artık dışarıdan injeckte edilecek
    service: SentimentService = Depends(get_sentiment_service)     
           
):

    
    try:
        saf_metin = request.text #bu safe
        result = service.analyze_text(saf_metin) #burda patlama olabilir yanlış hesaplama model sıkıntısı vsvs
        return result
    
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))

# KAPI 2: İSTATİSTİK KAPISI
@router.get("/stats")
def get_stats(service:SentimentService = Depends(get_sentiment_service)):
    """
    Retrieves real-time sentiment analysis statistics.
    
    Returns:
        dict: A dictionary containing counts for:
        - Positive
        - Negative
        - Neutral
        - Total requests processed
    """
    return service.get_statistics()