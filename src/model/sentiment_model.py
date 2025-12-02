import random

class SentimentModelInteractor:
    
    def __init__(self):

        # ml model ile etkileşim kuran aşama bu
        # interactor kahve makinesi oluyor 

        #iş mantıgı ve api kuralları burda yer almaz

        def __init__(self):
            print("Log: Yapay zeka modeli(mock)eklendi.")
        
        def __predict__(self,text : str) -> dict:

            #gelen metni modele verir ve ham (raw) sonucu döndürür

            mock_score = random.uniform(0.0,1.0)
            mock_label = "Pozitif" if mock_score > 0.5 else "Negatif"

            return {"label": mock_label, "score": mock_score}
            


       