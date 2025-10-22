# Step 1 - Data Preparation & Model Development

## Overview

This project walks through the **Data Preparation & Model Development** phase of the **Store Item Demand Forecasting Challenge**. In this step, you will load, clean, and preprocess the dataset, engineer useful features, and train a baseline regression model to predict daily sales. By the end of this step, you should have a trained model along with evaluation metrics.

## Steps Completed in Step 1

### 1. Project Setup

* Set up your local environment using a virtual environment (`venv` or `conda`).
* Installed the required dependencies listed in `requirements.txt`.
* Created the first Jupyter notebook for data preparation.

### 2. Dataset Loading

* Loaded the Kaggle dataset (`train.csv`) into a pandas DataFrame.
* Inspected the data to understand its structure and basic information.

### 3. Data Cleaning & Preprocessing

* Handled missing values and outliers in the dataset.
* Sorted the data chronologically by store and item to prepare it for feature engineering.
* Saved the cleaned dataset to `data/processed/cleaned_data.csv`.

### 4. Feature Engineering

* Added time-based features (e.g., `year`, `month`, `day`, `dayofweek`, `is_weekend`).
* Created lag features (`lag_1`, `lag_7`, `lag_30`) and rolling means (`rolling_mean_7`, `rolling_mean_30`).
* Saved the feature-engineered dataset for model training.

### 5. Train/Test Split

* Split the dataset chronologically into training and testing sets.
* Prepared the training and test features (`X_train`, `X_test`) and target labels (`y_train`, `y_test`).

### 6. Model Training (Baseline)

* Trained a baseline model (using **XGBoostRegressor** or **RandomForestRegressor**) on the training data.
* Evaluated the model performance using metrics such as **MAE**, **RMSE**, and **MAPE**.

### 7. Model Evaluation & Visualization

* Visualized the model’s performance by plotting **actual vs. predicted sales**.

### 8. Save Model & Metrics

* Saved the trained model to `models/model.pkl`.
* Stored the evaluation metrics (`MAE`, `RMSE`, `MAPE`) in a `metrics.json` file.

---

## Deliverables

After completing Step 1, the following deliverables should be available in your project:

* **Cleaned Dataset**: `data/processed/cleaned_data.csv`
* **Feature-Engineered Dataset**: `data/processed/feature_data.csv`
* **Trained Model**: `models/model.pkl`
* **Model Evaluation Metrics**: `models/metrics.json`
* **Jupyter Notebook**: `notebooks/01_data_preparation.ipynb`

---

## Next Steps

With **Step 1** completed, you are now ready to move on to **Step 2: Drift Detection Setup**. In this step, we will integrate **Evidently AI** and set up a **Streamlit drift monitoring dashboard**.


