from pydantic import BaseModel, Field

#giriş modeli (REQUEST)

class SentimentRequest(BaseModel):
    text: str= Field(
         ... , 
         min_length =5,
         max_length = 1000,
         description="Analiz edilecek metin",
         example = "bu ürün harikaydı, çok beğendim"

    )
    
#çıkış model(Response)
class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Duygu sonucu(Pozitif/Negatif/Nötr)")
    confidence: float  =Field(..., description="Güven skoru : (0.0-1.0)")