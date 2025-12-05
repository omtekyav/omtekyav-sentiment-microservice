
## business logic

from src.model.sentiment_model import SentimentModel
from src.schemas import SentimentResponse


#iş mantıgı katmanı(business logic) veriyi yönet kuralları uygular ve sonucu hazırlar

#mutfak şefi ana kumandan sentiment service
class SentimentService:
    def __init__(self):
        self.model = SentimentModel()
        

        self.negative_keywords = {"kötü", "berbat", "çöp", "beğenmedim", "pişman", "problem", "bozuk", "hata", "memnun değilim", "tavsiye etmem"}
        #hafıza sayaç kısmı burada olacak
        self.stats = {
            "Pozitif": 0,
            "Negatif": 0,
            "Nötr": 0,
            "Total": 0
        }


    def analyze_text(self, text:str) ->SentimentResponse:
        clean_text = text.strip().lower()

        #sonucları tutan gecici degiskenler
        sentiment = None
        confidence = 0.0

        #kural tabanlı kontrol direkt yasak kelime var mı yok mu kontrol ediyoruz
        for word in clean_text.split():
            if word in self.negative_keywords:
                print(f"LOG:kural tabanlı yasak kelime bulundu! Yasaklı kelime:'{word}'")
                sentiment = "Negatif"
                confidence = 1.0
                break
        
        #yapay zeka kontrolü kelime kuralı yoksa
        if sentiment is None:
            #makiniye sorulacak kısım self.interactor'dan predict cleantext'i tahmin edecek ve sonuc döndürecek
            prediction = self.model.predict(clean_text) # zor iş tahmin işini interactore(model oldu) devrettik
            sentiment = prediction["sentiment"]
            confidence = prediction["confidence"]

        #istatistik güncelleme kısmı burası
        if sentiment in self.stats:
            self.stats[sentiment] +=1
        self.stats["Total"] +=1

        return SentimentResponse(
            sentiment=sentiment,
            confidence=confidence
        )
    
    def get_statistics(self):
        return self.stats


                





    