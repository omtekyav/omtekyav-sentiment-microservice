import torch
import torch.nn.functional as F
from typing import List, Dict
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class SentimentModel:
    def __init__(self):
        # Klasör yolu indir.py ile aynı olmalı
        self.model_path = "src/model_files"
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _load_model(self):
        """Lazy loading: Model sadece ilk istek geldiğinde belleğe yüklenir."""
        print(f"🔄 Model yükleniyor (Cihaz: {self.device})...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            print("✅ Model başarıyla yüklendi!")
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            raise e

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """
        Multilingual Batch Prediction
        Model Çıktısı: 1-5 Yıldız (0-4 arası indeks)
        Mapping: 1-2 Yıldız -> Negatif, 3 Yıldız -> Nötr, 4-5 Yıldız -> Pozitif
        """
        if self.model is None or self.tokenizer is None:
            self._load_model()

        # 1. Tokenization (Batch için padding şart)
        encoded = self.tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        # 2. Veriyi GPU/CPU'ya taşı (Güvenli yöntem)
        inputs = {k: v.to(self.device) for k, v in encoded.items()}

        # 3. Inference (Çıkarım)
        with torch.inference_mode():  # no_grad'dan daha hızlıdır
            outputs = self.model(**inputs)

        # 4. Olasılıkları Hesapla
        probs = F.softmax(outputs.logits, dim=1)
        confidence_scores, predicted_classes = torch.max(probs, dim=1)

        results = []
        for i in range(len(texts)):
            # Model çıktısı 0-4 arasıdır (0=1 yıldız, 4=5 yıldız)
            star_rating = predicted_classes[i].item() + 1
            score = round(float(confidence_scores[i].item()), 4)

            # --- YILDIZ MAPPING MANTIĞI ---
            if star_rating <= 2:
                sentiment = "Negatif"
            elif star_rating == 3:
                sentiment = "Nötr"
            else:  # 4 ve 5 yıldız
                sentiment = "Pozitif"

            results.append({
                "sentiment": sentiment,
                "confidence": score,
                # Debug için yıldız bilgisini de loglarda görmek istersen:
                # "stars": star_rating 
            })

        return results

    def predict(self, text: str) -> Dict:
        """Tekli tahmin için wrapper (Eski kodlarla uyumluluk için)."""
        results = self.predict_batch([text])
        return results[0] if results else {"sentiment": "Nötr", "confidence": 0.0}