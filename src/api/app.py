from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# 👇 Add this import
from src.api.utils import pull_latest_model

app = FastAPI(title="Retail Demand Forecast API", version="1.0")

# ---- Fetch the latest model from DagsHub DVC before loading ----
try:
    pull_latest_model()
except Exception as e:
    print(f"⚠️ Warning: Could not pull model from DVC. Using local copy. Error: {e}")

# ---- Load model ----
MODEL_PATH = os.getenv("MODEL_PATH", "models/model_latest.pkl")
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully from", MODEL_PATH)

# ---- Request Schema ----
class ForecastRequest(BaseModel):
    store: int
    item: int
    date: str
    day_of_week: int
    month: int
    year: int

# ---- Routes ----
@app.get("/")
def root():
    return {"message": "Retail Demand Forecast API is running 🚀"}

@app.post("/predict")
def predict(request: ForecastRequest):
    data = pd.DataFrame([request.dict()])
    preds = model.predict(data)
    return {"predicted_sales": float(preds[0])}
