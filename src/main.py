from fastapi import FastAPI
from src.api.routes import router as api_router

#dükkanı inşaa et

app = FastAPI(

    title="Sentiment Analysis Microservice",
    description="Faz 1: Duygu Analizi API'si",
    version="1.0.0"

)

#api 
app.include_router(api_router, prefix="/api/v1", tags=["Analysis"])

@app.get("/")
def root():
    return{"message":"Sentiment Analysis Service is Running"}