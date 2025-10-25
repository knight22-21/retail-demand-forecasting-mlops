
# **Store Item Demand Forecasting Challenge**

## **Overview**

This project aims to predict the **daily sales** of store items through machine learning models. The project is split into multiple steps, each tackling different stages of model development, monitoring, and maintenance. **Step 1** focused on data preparation and model training, while **Step 2** deals with detecting data drift and concept drift to ensure the model stays up-to-date and performs reliably.

---

## **Step 1: Data Preparation & Model Development**

### **Objective:**

In **Step 1**, the goal was to prepare the dataset, engineer relevant features, train a baseline regression model, and evaluate its performance. The process involved cleaning the dataset, splitting it into training and test sets, and then developing a regression model to predict the daily sales of store items.

### **Steps Completed in Step 1:**

#### **1. Project Setup**

* Set up the local development environment using either a **virtual environment** (`venv` or `conda`).
* Installed the required dependencies listed in the `requirements.txt`.
* Created the initial Jupyter notebook (`01_data_preparation.ipynb`) to handle data loading and preprocessing.

#### **2. Dataset Loading**

* Loaded the Kaggle dataset (`train.csv`) into a pandas DataFrame.
* Inspected the data to understand its structure and basic information.

#### **3. Data Cleaning & Preprocessing**

* Handled missing values and outliers in the dataset.
* Sorted the data chronologically by store and item to prepare it for feature engineering.
* Saved the cleaned dataset to `data/processed/cleaned_data.csv`.

#### **4. Feature Engineering**

* Added **time-based features** (e.g., `year`, `month`, `day`, `dayofweek`, `is_weekend`).
* Created **lag features** (`lag_1`, `lag_7`, `lag_30`) and **rolling means** (`rolling_mean_7`, `rolling_mean_30`).
* Saved the feature-engineered dataset for model training as `data/processed/feature_data.csv`.

#### **5. Train/Test Split**

* Split the dataset chronologically into **training** and **test sets**.
* Prepared the training and test features (`X_train`, `X_test`) and target labels (`y_train`, `y_test`).

#### **6. Model Training (Baseline)**

* Trained a baseline model using **XGBoostRegressor** or **RandomForestRegressor** on the training data.
* Evaluated the model performance using metrics such as **MAE**, **RMSE**, and **MAPE**.

#### **7. Model Evaluation & Visualization**

* Visualized the model’s performance by plotting **actual vs. predicted sales**.

#### **8. Save Model & Metrics**

* Saved the trained model to `models/model.pkl`.
* Stored the evaluation metrics (`MAE`, `RMSE`, `MAPE`) in a `models/metrics.json` file.

---

### **Deliverables (Step 1)**

After completing **Step 1**, the following deliverables are available:

| Deliverable                | Path                                  |
| -------------------------- | ------------------------------------- |
| Cleaned Dataset            | `data/processed/cleaned_data.csv`     |
| Feature-Engineered Dataset | `data/processed/feature_data.csv`     |
| Trained Model              | `models/model.pkl`                    |
| Model Evaluation Metrics   | `models/metrics.json`                 |
| Jupyter Notebook           | `notebooks/01_data_preparation.ipynb` |

---

## **Step 2: Drift Detection Setup**

### **Objective:**

In **Step 2**, the focus shifted to monitoring the model's performance and data distribution over time. This is essential to detect **data drift** (when the distribution of input data changes) and **concept drift** (when the model’s performance degrades). By detecting these drifts early, we can trigger retraining to keep the model’s predictions accurate.

### **Steps Completed in Step 2:**

#### **1. Drift Detection Notebook**

A dedicated notebook `notebooks/02_drift_detection.ipynb` was created to:

* Load both the **reference dataset** (training data) and **current dataset** (new data).
* Compare the current data with the reference data to detect **data drift** using the **Evidently AI** library.
* Use **Evidently's DataDriftPreset** to perform statistical tests for detecting feature distribution shifts.
* Generate a **drift report** in HTML format and save it as `reports/data_drift_report.html`.

#### **2. Concept Drift Detection**

* The trained model (`models/model.pkl`) was used to make predictions on the current dataset.
* **Performance metrics** such as **MAE**, **RMSE**, and **MAPE** were calculated on the current data.
* The current model's performance was compared with the baseline stored in `models/metrics.json`. If the performance degraded (e.g., MAPE > baseline MAPE by 20%), **concept drift** was flagged.
* **Concept drift detection results** were logged in `logs/drift_logs.log` and saved in a summary file (`reports/drift_summary.json`).

#### **3. Results Logging and Storage**

* **Drift Results** were saved in the following files:

  * **Data Drift Report**: `reports/data_drift_report.html`
  * **Drift Summary**: `reports/drift_summary.json`
  * **Drift Log File**: `logs/drift_logs.log`

---

### **Deliverables (Step 2)**

After completing **Step 2**, the following deliverables are available:

| Deliverable              | Path                                 |
| ------------------------ | ------------------------------------ |
| Drift Detection Notebook | `notebooks/02_drift_detection.ipynb` |
| Evidently Report (HTML)  | `reports/data_drift_report.html`     |
| Drift Summary (JSON)     | `reports/drift_summary.json`         |
| Drift Log File           | `logs/drift_logs.log`                |

---

## **Success Criteria (Step 2)**

The following goals were achieved in **Step 2**:

* **Data Drift** detection using the **Evidently AI** library was implemented and successfully generated a report.
* **Concept Drift** detection logic was applied and validated, comparing current model performance to baseline metrics.
* Drift results were logged and stored for future automation of model retraining.
* The outputs were organized and stored in appropriate directories (`reports/`, `logs/`).



## **Step 3: Automate Retraining**

### **Objective:**

Building on the drift detection capability from Step 2, Step 3 focused on fully automating the model retraining workflow. This ensures that whenever data or concept drift is detected, the model retrains itself, updates versioned artifacts, and commits changes to the repository — all without manual intervention.

---

### **What Was Achieved in Step 3:**

#### 1. **Data & Model Versioning with DVC and DagsHub Integration**

* Initialized DVC in the project to efficiently track datasets and model files, ensuring reproducibility.
* Added key processed data files and trained models to DVC tracking, enabling seamless version control.
* Configured DVC to use **DagsHub as the remote storage backend**, providing scalable and reliable cloud storage for large data and model artifacts.
* Leveraged DagsHub’s integration with GitHub to synchronize data and model versions transparently, keeping the repository lightweight while maintaining full history and collaboration capabilities.
* Ensured that all CI/CD pipeline steps pull the latest artifacts from DagsHub, guaranteeing consistent and up-to-date inputs for drift detection and retraining.

#### 2. **Retraining Pipeline Script**

* Developed a robust retraining script that:

  * Loads the latest processed data directly managed by DVC and stored remotely on DagsHub.
  * Performs feature preparation consistent with earlier steps.
  * Retrains the model using the selected regression algorithm.
  * Evaluates retraining performance using standard metrics (MAE, RMSE, MAPE).
  * Saves the updated model and metrics with timestamped filenames for version tracking.
  * Logs retraining events for transparency and auditability.

#### 3. **Drift-to-Retrain Trigger Integration**

* Enhanced the drift detection process to generate a lightweight flag file signaling when data or concept drift is detected.
* This flag serves as a reliable trigger for the automated retraining pipeline.

#### 4. **GitHub Actions Workflow for End-to-End Automation**

* Created a GitHub Actions pipeline that:

  * Runs on a scheduled basis (weekly) or when new drift reports are pushed.
  * Checks for the presence of the retrain trigger flag.
  * Executes the retraining script only if drift has been detected.
  * Commits updated model artifacts and metrics to the repository.
  * Pushes DVC-tracked changes to **DagsHub remote storage**, ensuring remote artifacts remain synchronized.
* This workflow fully automates the retraining cycle — from drift detection to retraining, version control, and remote artifact management — using free-tier tools.

#### 5. **Logging and Monitoring**

* Implemented logging of retraining events into a dedicated log file, capturing timestamps and key performance metrics.
* Established a foundation for future alerting mechanisms or notifications upon retraining.
* Logs and versioned metrics enable ongoing analysis of model performance and retraining history.

---

### **Deliverables in Step 3:**

| Deliverable                  | Location                                   |
| ---------------------------- | ------------------------------------------ |
| DVC tracked data and models  | `.dvc/` directory and corresponding files  |
| DagsHub remote configuration | `.dvc/config` (pointing to DagsHub remote) |
| Retraining script            | `src/retraining/retrain_pipeline.py`       |
| Drift retrain trigger        | `drift_result.txt` (auto-generated)        |
| GitHub Actions workflow      | `.github/workflows/retrain.yml`            |
| Retraining logs              | `logs/retrain_logs.log`                    |

---

### **Summary:**

Step 3 established a fully automated MLOps retraining pipeline that tightly couples data and concept drift detection with retraining, artifact versioning, and repository updates. The integration of **DagsHub as a remote DVC storage backend** enhances scalability, collaboration, and artifact management, ensuring that large data and model files are efficiently handled outside of the GitHub repo.

This architecture ensures the model continuously adapts to evolving data with minimal manual intervention, providing a reliable, maintainable, and scalable foundation for production-ready machine learning workflows.



## **Step 4: Model Deployment via API**

### **Objective:**

In **Step 4**, the goal was to expose the trained forecasting model as a **REST API** that can be queried for real-time predictions. By using **FastAPI** for the backend and **Docker** for containerization, we can easily deploy this API locally or to a cloud platform such as **Hugging Face Spaces** for serving predictions.

### **Steps Completed in Step 4:**

#### **1. Folder Structure Setup**

The project structure was updated to accommodate the FastAPI app and Docker setup. The key components include:

* **API code** (`src/api/`) for handling the prediction logic.
* **Model** (`models/model_latest.pkl`) to store the latest trained model.
* **Configuration files** for dependencies (`requirements.txt`) and environment setup (`.env`).
* **Dockerfile** for containerizing the API app.

#### **2. FastAPI App Creation**

A FastAPI application was created to serve the model through a REST API. The app includes the following endpoints:

* **`/`**: A simple endpoint confirming that the API is running.
* **`/predict`**: A POST endpoint that accepts input features (store, item, date, etc.) and returns the predicted sales for the specified input.

The FastAPI app also automatically loads the latest model and serves predictions in real time.

#### **3. Utility for Fetching Latest Model (from DagsHub)**

To always serve the latest version of the model, a utility function was created that pulls the latest model from **DagsHub** using **DVC**. This ensures that the model served by the API is always the most up-to-date version.

#### **4. Local Testing**

Before containerizing the application, the FastAPI app was tested locally using **Uvicorn**. This allowed us to ensure the API is running correctly and can respond to prediction requests.

#### **5. Dockerize the API**

A **Dockerfile** was created to containerize the FastAPI app. This makes it portable and easy to deploy to any cloud service, such as **Hugging Face Spaces**, or run locally in any environment that supports Docker.

#### **6. Deployment to Hugging Face Spaces**

Instead of using Render or Heroku, the FastAPI app was deployed to **Hugging Face Spaces**, which provides a free-tier hosting solution. The deployment was configured with the necessary build and start commands to ensure the API runs smoothly in the cloud environment.

---

### **Deliverables (Step 4)**

After completing **Step 4**, the following deliverables are available:

| Deliverable                | Path               |
| -------------------------- | ------------------ |
| FastAPI app                | `src/api/app.py`   |
| Model fetching utility     | `src/api/utils.py` |
| Dockerfile                 | `Dockerfile`       |
| Hugging Face Spaces config | —                  |
| Test endpoint              | `/predict`         |

---

### **Success Criteria (Step 4)**

The following goals were achieved in **Step 4**:

* The **FastAPI API** was successfully created and runs both locally and containerized.
* The **`/predict`** endpoint accurately returns sales forecasts based on input features.
* The model is **automatically pulled from DVC** (DagsHub) to ensure the latest version is always used.
* The API was successfully deployed on **Hugging Face Spaces**, making it accessible online for real-time predictions.



## 🧭 **Step 5: Monitoring & Alerting (Prometheus + Grafana)**

### **Objective**

The goal of **Step 5** is to set up an open-source monitoring and alerting system for the deployed FastAPI forecasting API.
This ensures complete visibility into API health, performance, and usage over time — all running within a **free-tier Dockerized stack**.

We aim to monitor:

* **Model performance metrics** — latency, request rate, prediction volume
* **API uptime and error rates**
* **Drift detection triggers** (from Step 2)
* **Retraining frequency** (from Step 3 workflow)

We’ll use:

* **Prometheus** → metrics collection
* **Grafana** → visual dashboards
* **Prometheus Client (Python)** → instrumentation inside the FastAPI app

All components are orchestrated with **Docker Compose** for simple deployment.

---

### ⚙️ **Step 5.1 — Add Prometheus Metrics to FastAPI**

The FastAPI service (`src/api/app.py`) was extended with **Prometheus instrumentation** to expose real-time metrics such as:

* Total number of requests
* Prediction count
* Request latency distribution

A dedicated `/metrics` endpoint was added, compatible with Prometheus scraping.

---

### 🐳 **Step 5.2 — Docker Compose Setup**

A `docker-compose.yml` file was added at the project root to spin up **API + Prometheus + Grafana** simultaneously.
This allows quick local orchestration of the complete monitoring stack with one command.

---

### 🧾 **Step 5.3 — Prometheus Configuration**

A `prometheus.yml` configuration file defines the scrape job for the FastAPI container.
Prometheus scrapes metrics periodically (every 5 seconds by default) to maintain up-to-date API performance data.

---

### 🧪 **Step 5.4 — Run the Full Stack**

Launch all services together:

```bash
docker-compose up --build
```

Access the running stack via:

| Service        | URL                                                                        |
| -------------- | -------------------------------------------------------------------------- |
| **FastAPI**    | [http://localhost:8000/docs](http://localhost:8000/docs)                   |
| **Prometheus** | [http://localhost:9090](http://localhost:9090)                             |
| **Grafana**    | [http://localhost:3000](http://localhost:3000) (user/pass = `admin/admin`) |

This unified setup provides both API serving and live metric visualization.

---

### 📊 **Step 5.5 — Configure Grafana Dashboard**

Inside Grafana:

1. Navigate to **[http://localhost:3000](http://localhost:3000)**
2. Add a **Prometheus Data Source** → `http://prometheus:9090`
3. Create a new dashboard and add **query panels** using PromQL queries such as:

| Metric                   | Example Query                                                                     | Description             |
| ------------------------ | --------------------------------------------------------------------------------- | ----------------------- |
| Request Rate             | `rate(request_count[1m])`                                                         | Requests per minute     |
| Prediction Count         | `rate(prediction_count[1m])`                                                      | Predictions per minute  |
| Request Latency (95th %) | `histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[1m])) by (le))` | 95th-percentile latency |

These panels visualize API load, latency trends, and model usage patterns over time.

---

### **Deliverables (Step 5 – Monitoring & Alerting)**

| Deliverable              | Path / Purpose                                         |
| ------------------------ | ------------------------------------------------------ |
| FastAPI App with Metrics | `src/api/app.py` – includes `/metrics` endpoint        |
| Docker Compose Setup     | `docker-compose.yml` – runs API + Prometheus + Grafana |
| Prometheus Configuration | `prometheus.yml` – defines scrape job                  |
| Grafana Dashboard        | Custom panels for requests, latency, and usage         |

---

### **Success Criteria (Step 5)**

* ✅ `/metrics` endpoint successfully exposes runtime metrics
* ✅ Prometheus collects metrics from FastAPI container
* ✅ Grafana visualizes request rate, latency, and prediction volume
* ✅ Entire monitoring stack runs locally via Docker Compose


## 🛠 **Step 6: CI/CD Pipeline for Model Updates**

### **Objective**

The goal of **Step 6** is to fully automate the **retraining, testing, and deployment** of the forecasting model whenever a **data drift** or **concept drift** event occurs. This ensures the model stays accurate and the latest version is always served via the FastAPI API.

Key objectives include:

* Automatically detect drift triggers and initiate retraining workflows.
* Rebuild and deploy the FastAPI container with the updated model.
* Push updated model artifacts to **DVC/DagsHub**.
* Maintain a fully automated, reproducible MLOps pipeline using **GitHub Actions**.

---

### **Steps Completed in Step 6**

#### **1. GitHub Actions Workflow for Retraining & Deployment**

* Created a workflow file: `.github/workflows/retrain.yml`.
* The workflow is triggered by:

  * **Push events** on the main branch (manual retraining)
  * **Scheduled cron jobs** (e.g., weekly model evaluation)
  * **Drift flags** generated by Step 2 & Step 3 pipelines
* The workflow consists of the following jobs:

  1. **Setup Environment**

     * Install Python dependencies from `requirements.txt`.
     * Configure DVC to pull latest datasets and models from DagsHub.
  2. **Drift Check**

     * Pull the latest drift detection results (`reports/drift_summary.json`).
     * Evaluate if retraining is necessary.
  3. **Model Retraining**

     * Execute `src/retraining/retrain_pipeline.py`.
     * Train model on latest data and generate new evaluation metrics.
  4. **Artifact Versioning**

     * Save retrained model (`models/model.pkl`) and metrics (`models/metrics.json`).
     * Track artifacts with DVC and push to DagsHub.
  5. **Docker Build & Deploy**

     * Rebuild FastAPI container with updated model.
     * Deploy container to Hugging Face Spaces using the configured build commands.
  6. **Notification & Logging**

     * Update logs in `logs/retrain_logs.log`.
     * Optionally send Slack/email notifications for retraining events.

---

#### **2. Drift-to-CI/CD Integration**

* Drift detection from Step 2 generates a lightweight trigger flag.
* The GitHub Actions workflow reads this flag and conditionally triggers the retraining pipeline.
* This ensures **automatic, event-driven retraining** without manual intervention.

---

#### **3. Automated Testing**

* Added a **basic test suite** to validate the FastAPI API after redeployment:

  * `/predict` endpoint returns expected response.
  * Model metrics are within acceptable ranges compared to previous version.

---

### **Deliverables (Step 6 – CI/CD)**

| Deliverable                           | Path / Purpose                                   |
| ------------------------------------- | ------------------------------------------------ |
| CI/CD Workflow File                   | `.github/workflows/retrain.yml`                  |
| Retraining & Deployment Logs          | `logs/retrain_logs.log`                          |
| Updated Model & Metrics (DVC/DagsHub) | `models/model.pkl`, `models/metrics.json`        |
| FastAPI Container with Latest Model   | Hugging Face Spaces deployment                   |

---

### **Success Criteria**

* ✅ GitHub Actions workflow triggers retraining automatically on drift detection.
* ✅ Retrained model artifacts are versioned in **DVC/DagsHub**.
* ✅ FastAPI container is rebuilt and redeployed automatically.
* ✅ Logs track retraining events, model performance, and deployment success.
* ✅ Optional automated tests validate the `/predict` endpoint and model integrity.

---

### **Outcome**

Step 6 completes the **full MLOps lifecycle** for the Store Item Demand Forecasting project:

1. Data ingestion & preprocessing → Step 1
2. Drift detection → Step 2
3. Automated retraining → Step 3
4. Model deployment via FastAPI → Step 4
5. Monitoring & alerting → Step 5
6. **CI/CD automation for retraining & redeployment** → Step 6

The pipeline ensures **continuous adaptation, reproducibility, and reliability** of the forecasting model in production.

