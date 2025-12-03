from fastapi import APIRouter,HTTPException
from src.schemas import SentimentRequest, SentimentResponse

from src.services import SentimentService

router = APIRouter()

sentiment_service = SentimentService()

@router.post("/analyze", response_model=SentimentResponse)

def analyze_sentiment(request:SentimentRequest):
    try:
        saf_metin = request.text #bu safe
        result = sentiment_service.analyze_text(saf_metin) #burda patlama olabilir yanlış hesaplama model sıkıntısı vsvs
        return result
    
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))


