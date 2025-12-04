
## business logic

from src.model.sentiment_model import SentimentModelInteractor
from src.schemas import SentimentResponse


#iş mantıgı katmanı(business logic) veriyi yönet kuralları uygular ve sonucu hazırlar


class SentimentService:
    def __init__(self):
        self.interactor = SentimentModelInteractor()

        self.negative_keywords = {"kötü", "berbat", "çöp", "beğenmedim", "pişman", "problem", "bozuk", "hata", "memnun değilim", "tavsiye etmem"}
        


    def analyze_text(self, text:str) ->SentimentResponse:
        clean_text = text.strip().lower()

        for word in clean_text.split():
            if word in self.negative_keywords:
                print(f"LOG:kural tabanlı yasak kelime bulundu! Yasaklı kelime:'{word}'")

                return SentimentResponse(

                    sentiment = "Negatif",
                    confidence= 1.0 #kesinlik var çünkü kelime sınırına takıldı
                )

        #klasik yapay zeka kontrolü

        #makiniye sorulacak kısım self.interactor'dan predict cleantext'i tahmin edecek ve sonuc döndürecek
        prediction = self.interactor.predict(clean_text) # zor iş tahmin işini interactore devrettik

        return SentimentResponse(

        sentiment = prediction["label"],    
        confidence= prediction["score"],

    )





    