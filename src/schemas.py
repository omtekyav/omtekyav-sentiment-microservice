from pydantic import BaseModel, Field , field_validator
import re

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
    #validasyon olduğu için classmethod olarak kullanıyoruz
    @classmethod # daha ortada üretilmiş bir response olmadığı için classmethod'dan cagırıyoruz yani instance yok ortada ürün yok

    def check_valid_text(cls,v:str): #ilk parametre sınıfın kendisi olacak v : value > bunlar
        if not v.strip():
            raise ValueError('Metin boşluklardan oluşamaz anlamlı bir metin giriniz.')
        



        if not re.search(r'[a-zA-Z]', v): #kücük harf veya büyük harf
            raise ValueError('Metin en az bir harf içermelidir(sadece sayı ve semboller kabul edilmez)')   
        

        return v
    







class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Duygu sonucu(Pozitif/Negatif/Nötr)")
    confidence: float  =Field(..., description="Güven skoru : (0.0-1.0)")