import pandas as pd
import joblib, json
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os
from datetime import datetime

# 1️⃣ Load new data
data_path = "data/processed/cleaned_data.csv"
df = pd.read_csv(data_path, parse_dates=['date'])

# 2️⃣ Feature prep (reuse logic)
X = df.drop(['sales', 'date'], axis=1)
y = df['sales']

# 3️⃣ Train new model
model = XGBRegressor(
    n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42
)
model.fit(X, y)

# 4️⃣ Evaluate (train performance only, for simplicity)
y_pred = model.predict(X)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
mape = np.mean(np.abs((y - y_pred) / y)) * 100

metrics = {"mae": mae, "rmse": rmse, "mape": mape}

# 5️⃣ Save new artifacts
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
model_path = f"models/model_{timestamp}.pkl"
joblib.dump(model, model_path)
json.dump(metrics, open("models/metrics.json", "w"), indent=2)

print("✅ Model retrained and saved:", model_path) 
print("📊 Metrics:", metrics)
