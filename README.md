# Customer Churn End-to-End MLOps Pipeline

## Overview

This project is an end-to-end MLOps pipeline for Customer Churn Prediction using Machine Learning and modern MLOps tools.

The pipeline automates the complete machine learning workflow, starting from raw data ingestion and validation to model training, model selection, experiment tracking, and model registration.

The project demonstrates industry-standard MLOps practices including:

* Data Version Control (DVC)
* MLflow Experiment Tracking
* MLflow Model Registry
* Automated Model Selection
* Hyperparameter Tuning
* Reproducible ML Pipelines
* Git-based Version Control

---

## Problem Statement

Customer churn is one of the biggest challenges faced by subscription-based businesses.

The goal of this project is to predict whether a customer is likely to leave the company based on customer demographics, services used, billing information, and account history.

By identifying customers at risk of churn, businesses can take proactive actions to improve customer retention.

---

## Dataset

Dataset Used:

**Telco Customer Churn Dataset**

Features include:

* Gender
* Senior Citizen Status
* Partner
* Dependents
* Tenure
* Phone Service
* Internet Service
* Online Security
* Online Backup
* Device Protection
* Tech Support
* Streaming TV
* Streaming Movies
* Contract Type
* Payment Method
* Monthly Charges
* Total Charges

Target Variable:

```text
Churn
```

---

## Project Architecture

```text
Raw Data
    │
    ▼
Data Validation
    │
    ▼
Data Cleaning
    │
    ▼
Feature Engineering
    │
    ▼
Model Training
    │
    ▼
Model Selection
    │
    ▼
MLflow Model Registry
```

---

## Project Structure

```text
Customer-Churn-End-to-End-MLOps
│
├── .dvc/
├── artifacts/
├── config/
│   └── params.yaml
│
├── data/
│   ├── raw/
│   ├── validated/
│   └── processed/
│
├── mlruns/
│
├── models/
│
├── src/
│   ├── components/
│   │   ├── validation.py
│   │   ├── cleaning.py
│   │   ├── feature_engineering.py
│   │   ├── model_training.py
│   │   └── model_selection.py
│   │
│   ├── pipeline/
│   │
│   └── utils/
│       └── config_loader.py
│
├── dvc.yaml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

### Machine Learning

* Scikit-Learn
* XGBoost
* LightGBM

### Data Processing

* Pandas
* NumPy

### MLOps

* DVC
* MLflow

### Version Control

* Git
* GitHub

### Configuration Management

* YAML

---

## Pipeline Stages

### 1. Data Validation

Validates:

* Dataset existence
* Required columns
* Dataset structure
* Missing critical information

Output:

```text
data/validated/validated_churn.csv
```

---

### 2. Data Cleaning

Performs:

* Missing value handling
* Data type correction
* Duplicate removal
* Data consistency checks

Output:

```text
data/processed/cleaned_churn.csv
```

---

### 3. Feature Engineering

Performs:

* Train-Test Split
* Categorical Encoding
* Numerical Feature Scaling
* Preprocessing Pipeline Creation

Outputs:

```text
X_train.csv
X_test.csv
y_train.csv
y_test.csv
preprocessor.pkl
```

---

### 4. Model Training

Trains multiple machine learning models:

#### Random Forest

Grid Search Parameters:

* n_estimators
* max_depth

#### XGBoost

Grid Search Parameters:

* learning_rate
* max_depth
* n_estimators

#### LightGBM

Grid Search Parameters:

* learning_rate
* max_depth
* n_estimators

Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score

---

### 5. Automated Model Selection

The pipeline automatically:

* Compares all trained models
* Selects the best model using ROC-AUC
* Saves best model metadata
* Creates production-ready model artifacts

Outputs:

```text
best_model.pkl
best_model_metadata.json
```

---

### 6. MLflow Integration

Tracks:

* Experiments
* Runs
* Parameters
* Metrics
* Artifacts

Stored Information:

```text
Model Parameters
Training Metrics
Model Artifacts
Leaderboard Results
```

---

### 7. MLflow Model Registry

The best-performing model is automatically registered into the MLflow Model Registry.

Benefits:

* Model Versioning
* Centralized Model Management
* Deployment Readiness
* Production Tracking

---

## DVC Pipeline

Pipeline Definition:

```text
validation
    ↓
cleaning
    ↓
feature_engineering
    ↓
model_training
    ↓
model_selection
```

Run entire pipeline:

```bash
dvc repro
```

Visualize pipeline:

```bash
dvc dag
```

Check pipeline status:

```bash
dvc status
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/Customer-Churn-End-to-End-MLOps.git
```

Move into project directory:

```bash
cd Customer-Churn-End-to-End-MLOps
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run complete pipeline:

```bash
dvc repro
```

Run individual stages:

```bash
python src/components/validation.py

python src/components/cleaning.py

python src/components/feature_engineering.py

python src/components/model_training.py

python src/components/model_selection.py
```

---

## Launch MLflow UI

```bash
mlflow ui
```

Open:

```text
http://127.0.0.1:5000
```

Features:

* Experiment Tracking
* Metrics Visualization
* Model Comparison
* Model Registry

---

## Model Performance

| Model         | Accuracy | ROC-AUC |
| ------------- | -------- | ------- |
| Random Forest | 79.63%   | 0.8408  |
| XGBoost       | 80.27%   | 0.8445  |
| LightGBM      | 80.41%   | 0.8445  |

Best Model:

```text
LightGBM
```

---

## Future Improvements

* Docker Containerization
* FastAPI Prediction Service
* CI/CD with GitHub Actions
* Cloud Deployment
* Monitoring and Logging
* Automated Retraining Pipeline

---

## Author

Dhrumi

Customer Churn End-to-End MLOps Project built for learning and implementing production-grade Machine Learning Operations practices.
