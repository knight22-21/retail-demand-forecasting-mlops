from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from datetime import datetime

# 👇 Optional: Pull latest model from DVC if you have that setup
try:
    from src.api.utils import pull_latest_model
    pull_latest_model()
except Exception as e:
    print(f"⚠️ Warning: Could not pull model from DVC. Using local copy. Error: {e}")

app = FastAPI(title="Retail Demand Forecast API", version="1.0")

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully from", MODEL_PATH)

class ForecastRequest(BaseModel):
    store: int
    item: int
    date: str  # Date is accepted but not used in prediction

@app.get("/")
def root():
    return {"message": "Retail Demand Forecast API is running 🚀"}

@app.post("/predict")
def predict(request: ForecastRequest):
    # Only the features used during training: store and item
    data_dict = {
        "store": request.store,
        "item": request.item,
    }

    input_df = pd.DataFrame([data_dict])
    prediction = model.predict(input_df)[0]

    return {"predicted_sales": float(prediction)}
