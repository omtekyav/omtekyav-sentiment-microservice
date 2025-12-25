#business logic aşaması / çoklu dil destekli 
from typing import List, Dict
from src.model.sentiment_model import SentimentModel
from src.schemas import SentimentResponse

class SentimentService:
    def __init__(self):
        self.model = SentimentModel()
        
        # 🌍 BILINGUAL KEYWORDS (TR + EN)
        # Hem Türkçe hem İngilizce negatif kelimeleri buraya ekliyoruz.
        # Bu kelimeler geçiyorsa modele sormaya gerek yok, direkt NEGATİF basacağız.
        self.negative_keywords = {
            # Turkish
            "kötü", "berbat", "çöp", "beğenmedim", "pişman", 
            "problem", "bozuk", "hata", "iğrenç", "vasat",
            "dandik", "rezalet", "felaket", "saçma", "zaman kaybı",
            # English
            "bad", "terrible", "awful", "trash", "worst", 
            "boring", "waste", "disaster", "poor", "hate",
            "sucks", "horrible", "garbage", "crap", "stupid"
        }
        
        # Basit bir bellek-içi istatistik tutucu
        self.stats = {
            "Total": 0,
            "Pozitif": 0,
            "Negatif": 0,
            "Nötr": 0
        }

    def analyze_text(self, text: str) -> SentimentResponse:
        """
        Tekli metin analizi (Eski endpointler için uyumluluk).
        """
        # Batch mantığını çağırıp ilk sonucu alıyoruz, kod tekrarı yok.
        result = self.analyze_batch([text])["results"][0]
        
        # Response modeline çevir (Pydantic)
        return SentimentResponse(
            sentiment=result["sentiment"],
            confidence=result["confidence"]
        )

    def analyze_batch(self, texts: List[str]) -> Dict[str, List[Dict]]:
        """
        Hibrit Batch Analizi:
        1. Kural Tabanlı Ön Eleme (Hız Kazandırır)
        2. Sadece gerekenleri Yapay Zekaya sorma
        3. Sonuçları birleştirme
        """
        final_results = [None] * len(texts) # Sonuçlar için yer tut
        indices_for_ai = [] # AI'ya gideceklerin orijinal sıra numarası
        texts_for_ai = []   # AI'ya gidecek metinler

        # --- FAZ 1: Kural Tabanlı Tarama ---
        for i, text in enumerate(texts):
            original = (text or "").strip()
            clean = original.lower() # Sadece kural kontrolü için küçült

            found_keyword = False
            
            # Yasaklı kelime kontrolü
            for word in clean.split():
                if word in self.negative_keywords:
                    # Yakaladık! Modele gitmeye gerek yok.
                    final_results[i] = {
                        "sentiment": "Negatif",
                        "confidence": 1.0
                    }
                    found_keyword = True
                    
                    # İstatistik güncelle
                    self.stats["Negatif"] += 1
                    self.stats["Total"] += 1
                    break

            # Eğer kurala takılmadıysa AI listesine ekle
            if not found_keyword:
                indices_for_ai.append(i)
                texts_for_ai.append(original) # Modele ORİJİNAL metni gönder (Cased model hassasiyeti için)

        # --- FAZ 2: Yapay Zeka (Sadece gerekenler için) ---
        if texts_for_ai:
            ai_results = self.model.predict_batch(texts_for_ai)

            # Sonuçları doğru yerlerine (indekslerine) yerleştir
            for original_index, result in zip(indices_for_ai, ai_results):
                final_results[original_index] = result
                
                # İstatistik güncelle
                sentiment = result.get("sentiment")
                if sentiment in self.stats:
                    self.stats[sentiment] += 1
                self.stats["Total"] += 1

        return {"results": final_results}

    def get_statistics(self):
        return self.stats