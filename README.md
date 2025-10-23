
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

---

### **Next Steps:**

With automated retraining and robust version control via DVC and DagsHub in place, the project is ready to advance to **Step 4: Model Deployment**, focusing on packaging the model with FastAPI and Docker, and deploying it to cloud infrastructure for serving real-time predictions.
