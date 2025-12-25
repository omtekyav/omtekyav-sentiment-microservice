from pydantic import BaseModel, Field, field_validator
from typing import List
import re

# --- TEKLİ İŞLEM MODELLERİ (MEVCUT) ---

# Giriş Modeli (Request)
class SentimentRequest(BaseModel):
    text: str = Field(
         ..., 
         min_length=5,
         max_length=1000,
         description="Analiz edilecek metin",
         example="bu ürün harikaydı, çok beğendim"
    )
    
    @field_validator('text')
    @classmethod
    def check_valid_text(cls, v: str):
        if not v.strip():
            raise ValueError('Metin boşluklardan oluşamaz anlamlı bir metin giriniz.')

        if not re.search(r'[a-zA-Z]', v): # En az bir harf olmalı
            raise ValueError('Metin en az bir harf içermelidir (sadece sayı ve semboller kabul edilmez)')   

        return v

# Çıkış Modeli (Response)
class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Duygu sonucu (Pozitif/Negatif/Nötr)")
    confidence: float = Field(..., description="Güven skoru: (0.0-1.0)")


# --- BATCH (TOPLU) İŞLEM MODELLERİ (YENİ) ---

class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(
        ..., 
        description="Analiz edilecek metinlerin listesi",
        example=["Film harikaydı", "Berbat bir deneyim", "Fena değildi"]
    )

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]