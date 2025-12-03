import random

class SentimentModelInteractor:
    
    # 1. Init Metodu (Başlatıcı)
    def __init__(self):
        # ml model ile etkileşim kuran aşama bu
        # interactor kahve makinesi oluyor 
        print("Log: Yapay zeka modeli(mock)eklendi.")
    
    # 2. Predict Metodu (Tahminci)
    # DİKKAT: Bu fonksiyon __init__'in içinde değil, onunla AYNI HİZADA (Kardeş)
    # DİKKAT: Adı __predict__ değil, sadece 'predict'
    def predict(self, text: str) -> dict:
        
        # gelen metni modele verir ve ham (raw) sonucu döndürür
        mock_score = random.uniform(0.0, 1.0)
        mock_label = "Pozitif" if mock_score > 0.5 else "Negatif"

        return {"label": mock_label, "score": mock_score}