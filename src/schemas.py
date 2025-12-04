from pydantic import BaseModel, Field , field_validator

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
    @field_validator('text')
    @classmethod

    def check_not_empty(cls,v:str): #ilk parametre sınıfın kendisi olacak v : value > bunlar
        if not v.strip():
            raise ValueError('Metin boşluklardan oluşamaz anlamlı bir metin giriniz.')
        return v




class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Duygu sonucu(Pozitif/Negatif/Nötr)")
    confidence: float  =Field(..., description="Güven skoru : (0.0-1.0)")