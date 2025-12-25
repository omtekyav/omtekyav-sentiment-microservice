from fastapi import APIRouter, HTTPException, Depends
# Yeni eklenen Batch şemalarını import etmeyi unutmuyoruz
from src.schemas import SentimentRequest, SentimentResponse, BatchSentimentRequest, BatchSentimentResponse
from src.services import SentimentService

# Router tanımlaması
router = APIRouter()

# --- TEDARİKÇİ (Dependency Provider) ---
# Gerçek servisi hafızada tutan Singleton değişken
_real_service = SentimentService()

def get_sentiment_service():
    """
    Endpoint'lere SentimentService sağlar.
    Testlerde bu fonksiyon override edilerek mock servis verilebilir.
    """
    return _real_service

# --- 1. ESKİ ENDPOINT (Geriye Dönük Uyumluluk İçin) ---
@router.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(
    request: SentimentRequest,
    service: SentimentService = Depends(get_sentiment_service)
):
    try:
        # Tekli işlem de artık arka planda yeni mantığı kullanıyor
        return service.analyze_text(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 2. YENİ BATCH ENDPOINT (Ingestion İçin) ---
@router.post("/analyze-batch", response_model=BatchSentimentResponse)
def analyze_batch(
    request: BatchSentimentRequest,
    service: SentimentService = Depends(get_sentiment_service)
):
    """
    🚀 HIZLI ŞERİT: Birden fazla metni aynı anda analiz eder.
    - Kural tabanlı ön eleme yapar.
    - Sadece gerekenleri AI modeline gönderir.
    - 10x daha hızlıdır.
    """
    try:
        return service.analyze_batch(request.texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. İSTATİSTİK ENDPOINT ---
@router.get("/stats")
def get_stats(service: SentimentService = Depends(get_sentiment_service)):
    """
    Gerçek zamanlı analiz istatistiklerini döndürür.
    """
    return service.get_statistics()