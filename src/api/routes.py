from fastapi import APIRouter,HTTPException
from src.schemas import SentimentRequest, SentimentResponse
# Başka dosyadan (services.py) "SentimentService" tarifini getir dedik.
from src.services import SentimentService

#router garson tanımlanıyor
router = APIRouter()

#müdür başlatılıyor service INSTANTIATION (İşe Alma / Yaratma)
#"Bu tarife göre bana canlı kanlı bir çalışan (nesne) ver
# Artık elimizde "sentiment_service" adında, hafızası olan bir çalışan var.
#"Restoran açıldı (App start), Şefi mutfağa koy, defterini eline ver ve bekle."
sentiment_service = SentimentService()

# kapı 1. analiz kapısı post
@router.post("/analyze", response_model=SentimentResponse)

def analyze_sentiment(request:SentimentRequest):
    try:
        saf_metin = request.text #bu safe
        result = sentiment_service.analyze_text(saf_metin) #burda patlama olabilir yanlış hesaplama model sıkıntısı vsvs
        return result
    
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))


@router.get("/stats")
def get_stats():
    """
    Retrieves real-time sentiment analysis statistics.
    
    Returns:
        dict: A dictionary containing counts for:
        - Positive
        - Negative
        - Neutral
        - Total requests processed
    """
    return sentiment_service.get_statistics()