
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

---

## **Next Steps (Step 3)**

With **Step 2** completed, the next step is **Step 3: Automate Retraining**. In this phase, we will automate the retraining process using **GitHub Actions** and **DVC** (Data Version Control) to trigger retraining whenever drift is detected.

