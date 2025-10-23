# Use a lightweight base image
FROM python:3.10-slim

WORKDIR /app

# Install system deps (important for DVC)
RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pull model during build (optional)
# RUN dvc pull models/model_latest.pkl.dvc || true

EXPOSE 8000
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "7860"]

