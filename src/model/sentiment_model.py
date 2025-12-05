import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer


#sınıf yapısı ve init kurucu method
class SentimentModel():
    def __init__(self):
        
        self.model_name = "savasy/bert-base-turkish-sentiment-cased"
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#lazy loading yapılacak kısım
    def _load_model(self):

        print("Model Loading...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            print("Model Loaded Successfully!")
        except Exception as e:
            print(f"error:{e}")
            raise e
    
    #tahmin aşaması predict aşaması
    def predict(self,text:str) -> dict:
        if self.model is None or self.tokenizer is None:
            self._load_model()
        

        #tokenizer = metni sayılara tokenlere ceviriyoruz
        inputs = self.tokenizer(
            text,
            return_tensors = "pt",
            truncation=True,
            padding= True,
            max_length = 512
        ).to(self.device)

        #inference çıkarım yapma işlemi

        with torch.no_grad():
            outputs = self.model(**inputs)
        
        #logits to probs
        probs = F.softmax(outputs.logits , dim=1)

        #en yüksek olasılık
        confidence, predicted_class = torch.max(probs, dim=1)

        labels = {0: "Negatif", 1: "Pozitif"}
        sentiment = labels.get(predicted_class.item(), "Nötr")

        return {
            "sentiment": sentiment,
            "confidence": round(confidence.item(), 4)
        }




                
    


