# Customer Churn End-to-End MLOps Pipeline

[![MLOps Pipeline CI](https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps/actions/workflows/pipeline.yml/badge.svg)](https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps/actions/workflows/pipeline.yml)
[![Docker Build and Push](https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps/actions/workflows/docker.yml/badge.svg)](https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps/actions/workflows/docker.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/dhrumi2910/mlops-churn-pipeline)](https://hub.docker.com/r/dhrumi2910/mlops-churn-pipeline)

---

## Overview

A complete **end-to-end MLOps pipeline** for predicting customer churn in a telecom company.

The system automates the entire ML workflow — from raw data ingestion to a deployed REST API — using industry-standard MLOps tools.

**Tech Stack:** Python · Scikit-Learn · XGBoost · LightGBM · DVC · MLflow · FastAPI · Docker · GitHub Actions

---

## Problem Statement

Customer churn is a major challenge for subscription-based businesses. This project predicts whether a customer is likely to leave so the business can take proactive retention steps.

**Dataset:** Telco Customer Churn (7,043 customers, 21 features)  
**Target:** `Churn` — Yes or No  
**Source:** [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Architecture

```
Raw Data (CSV)
     │
     ▼
[1] Data Ingestion        ← Downloads dataset from Kaggle
     │
     ▼
[2] Data Validation       ← Schema checks, column validation
     │
     ▼
[3] Data Cleaning         ← Missing values, duplicates, type fixes
     │
     ▼
[4] Feature Engineering   ← OneHotEncoder + StandardScaler + Train/Test split
     │
     ▼
[5] Model Training        ← GridSearchCV on RandomForest, XGBoost, LightGBM
     │
     ▼
[6] Model Selection       ← Best model by ROC-AUC → MLflow Model Registry
     │
     ▼
FastAPI REST API          ← Serve predictions via POST /predict
     │
     ▼
Docker Container          ← Portable deployment
     │
     ▼
GitHub Actions CI/CD      ← Auto build + push to Docker Hub on every push
```

---

## Project Structure

```
Customer-Churn-End-to-End-MLOps/
│
├── .github/
│   └── workflows/
│       ├── pipeline.yml          ← CI: runs ML pipeline on every push
│       └── docker.yml            ← CD: builds & pushes Docker image
│
├── config/
│   └── params.yaml               ← Hyperparameters for all models
│
├── data/
│   ├── raw/                      ← Original dataset
│   ├── validated/                ← Schema-validated data
│   └── processed/                ← Cleaned data
│
├── artifacts/
│   └── feature_engineering/
│       ├── preprocessor.pkl      ← Fitted sklearn pipeline
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── models/
│   ├── RandomForest.pkl
│   ├── XGBoost.pkl
│   ├── LightGBM.pkl
│   ├── model_scores.csv          ← Leaderboard
│   ├── best_model.pkl            ← Production model
│   └── best_model_metadata.json  ← Metrics
│
├── reports/
│   └── metrics.json              ← Final model metrics
│
├── src/
│   ├── components/
│   │   ├── ingestion.py
│   │   ├── validation.py
│   │   ├── cleaning.py
│   │   ├── feature_engineering.py
│   │   ├── model_training.py
│   │   └── model_selection.py
│   └── utils/
│       └── config_loader.py
│
├── app_api.py                    ← FastAPI inference service
├── main.py                       ← Full pipeline runner
├── dvc.yaml                      ← DVC pipeline definition
├── Dockerfile                    ← Container build
├── requirements.txt              ← Python dependencies
└── README.md
```

---

## Quick Start

### Option 1 — Run Locally

```bash
# Clone repo
git clone https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps.git
cd Customer-Churn-End-to-End-MLOps

# Create virtual environment
python -m venv venv_mlops
venv_mlops\Scripts\activate        # Windows
# source venv_mlops/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python main.py
```

### Option 2 — Docker (No setup needed)

```bash
# Pull from Docker Hub
docker pull dhrumi2910/mlops-churn-pipeline:latest

# Run the API
docker run -p 8000:8000 dhrumi2910/mlops-churn-pipeline:latest
```

Open: **http://localhost:8000/docs**

### Option 3 — DVC (Smart pipeline)

```bash
# Runs only changed stages automatically
dvc repro
```

---

## Pipeline Stages

### 1. Data Ingestion
Downloads the Telco Customer Churn dataset from Kaggle. Skips download if file already exists locally.

### 2. Data Validation
Checks all 21 required columns are present, dataset is not empty, and reports missing values and duplicates.

### 3. Data Cleaning
- Converts `TotalCharges` from string to numeric
- Fills missing values (median for numeric, mode for categorical)
- Removes duplicate rows
- Saves a cleaning report

### 4. Feature Engineering
- Drops `customerID`
- Encodes target: `Churn` → 0/1
- `OneHotEncoder` for 15 categorical columns
- `StandardScaler` for 4 numerical columns
- 80/20 stratified train/test split
- Saves `preprocessor.pkl` and split CSVs

### 5. Model Training
Trains 3 models with `GridSearchCV` (5-fold CV, ROC-AUC scoring):
- **RandomForest**: n_estimators, max_depth
- **XGBoost**: n_estimators, max_depth, learning_rate
- **LightGBM**: n_estimators, max_depth, learning_rate

All runs logged to **MLflow** (params, metrics, artifacts).

### 6. Model Selection
- Reads leaderboard CSV
- Selects best model by ROC-AUC
- Saves `best_model.pkl` and `best_model_metadata.json`
- Registers to **MLflow Model Registry** with alias `production-candidate`

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| **LightGBM** | 80.41% | 70.59% | 44.92% | 54.90% | **0.8445** |
| XGBoost | 80.27% | 70.00% | 44.92% | 54.72% | 0.8445 |
| RandomForest | 79.63% | 68.51% | 43.05% | 52.87% | 0.8408 |

**Best Model: LightGBM** (ROC-AUC: 0.8445)

---

## FastAPI Inference Service

### Start locally

```bash
uvicorn app_api:app --reload --port 8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/predict` | Predict churn |

### Sample Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 85.5,
    "TotalCharges": 171.0
  }'
```

### Sample Response

```json
{
  "prediction": 1,
  "probability_churn": 0.82,
  "label": "Will Churn",
  "model_used": "LightGBM"
}
```

### Swagger UI

Open **http://localhost:8000/docs** for the interactive API documentation.

---

## DVC Pipeline

```yaml
# dvc.yaml — 6 automated stages
ingestion → validation → cleaning → feature_engineering → model_training → model_selection
```

### DVC Commands

```bash
dvc repro              # Run only changed stages
dvc repro --force      # Force rerun all stages
dvc status             # Check what would run
dvc dag                # Visualize pipeline graph
dvc params diff        # Compare parameter changes
dvc metrics show       # Show tracked metrics
```

### Auto-rerun behaviour

| Change | Stages that rerun |
|--------|------------------|
| Raw data changed | All 6 stages |
| `params.yaml` changed | model_training + model_selection |
| `cleaning.py` changed | cleaning → selection (4 stages) |
| Nothing changed | 0 stages ("Pipeline up to date") |

---

## MLflow

```bash
# Launch UI
mlflow ui
# Open: http://127.0.0.1:5000
```

Features:
- All training runs logged with params and metrics
- Model comparison across RandomForest, XGBoost, LightGBM
- Best model registered in Model Registry
- Alias: `production-candidate`

---

## Docker

### Docker Hub

```
dhrumi2910/mlops-churn-pipeline:latest
```

### Build locally

```bash
docker build -t mlops-churn-pipeline .
docker run -p 8000:8000 mlops-churn-pipeline
```

### Pull and run from Docker Hub

```bash
docker pull dhrumi2910/mlops-churn-pipeline:latest
docker run -p 8000:8000 dhrumi2910/mlops-churn-pipeline:latest
```

---

## GitHub Actions CI/CD

### MLOps Pipeline CI (`pipeline.yml`)
Triggers on every push to `main`:
- Installs dependencies
- Runs `python main.py` (full 6-stage pipeline)
- Uploads model scores and metadata as artifacts

### Docker Build and Push (`docker.yml`)
Triggers on every push to `main`:
- Logs in to Docker Hub
- Builds Docker image
- Pushes `dhrumi2910/mlops-churn-pipeline:latest` to Docker Hub

---

## Hyperparameters (`config/params.yaml`)

```yaml
random_forest:
  n_estimators: [100, 200]
  max_depth: [5, 10, 15]

xgboost:
  n_estimators: [100, 200]
  max_depth: [4, 6]
  learning_rate: [0.01, 0.1]

lightgbm:
  n_estimators: [100, 200]
  max_depth: [4, 6]
  learning_rate: [0.01, 0.1]

cv_folds: 5
selection_metric: roc_auc
```

Change any value → run `dvc repro` → pipeline reruns automatically from training stage.

---

## Technologies Used

| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| ML | Scikit-Learn, XGBoost, LightGBM |
| Data | Pandas, NumPy, SciPy |
| MLOps | DVC, MLflow |
| API | FastAPI, Uvicorn, Pydantic |
| Container | Docker, Docker Hub |
| CI/CD | GitHub Actions |
| Config | YAML |
| Version Control | Git, GitHub |

---

## Future Enhancements

- [ ] Cloud deployment (AWS / GCP / Azure)
- [ ] Kubernetes for API scaling
- [ ] Model monitoring and drift detection
- [ ] Automated retraining on data drift
- [ ] Cross-validation and advanced hyperparameter tuning
- [ ] Feature store integration
- [ ] A/B testing framework

---

## Author

**Dhrumi Deepak Modi**

End-to-End MLOps Customer Churn Pipeline — built to demonstrate production-grade Machine Learning Operations practices.

GitHub: [MDhrumi-2005](https://github.com/MDhrumi-2005)  
Docker Hub: [dhrumi2910](https://hub.docker.com/r/dhrumi2910/mlops-churn-pipeline)
