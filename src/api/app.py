from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Retail Demand Forecast API", version="1.0")

# Load model (ensure path matches your retrain pipeline output)
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
model = joblib.load(MODEL_PATH)

class ForecastRequest(BaseModel):
    store: int
    item: int
    date: str  # ISO date string
    day_of_week: int
    month: int
    year: int

@app.get("/")
def root():
    return {"message": "Retail Demand Forecast API is running 🚀"}

@app.post("/predict")
def predict(request: ForecastRequest):
    data = pd.DataFrame([request.dict()])
    preds = model.predict(data)
    return {"predicted_sales": float(preds[0])}
