
## business logic

from src.model.sentiment_model import SentimentModelInteractor
from src.schemas import SentimentResponse


#iş mantıgı katmanı(business logic) veriyi yönet kuralları uygular ve sonucu hazırlar


class SentimentService:
    def __init__(self):
        self.interactor = SentimentModelInteractor()

    def analyze_text(self, text:str) ->SentimentResponse:
        clean_text = text.strip().lower()

        prediction = self.interactor.predict(clean_text) # zor iş tahmin işini interactore devrettik

        return SentimentResponse(

        sentiment = prediction["label"],
        confidence= prediction["score"],

    )





    