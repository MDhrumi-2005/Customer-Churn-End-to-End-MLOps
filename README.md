# Customer Churn End-to-End MLOps Pipeline

## 🎯 Overview

Complete MLOps pipeline for **Customer Churn Prediction** with automated orchestration, experiment tracking, and model registry.

**Tech Stack:** DVC · MLflow · Scikit-Learn · XGBoost · LightGBM · Docker

---

## 🚀 Quick Start

### Option 1: Run Complete Pipeline (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python main.py
```

### Option 2: DVC Pipeline (Automatic Dependency Management)

```bash
# Run entire pipeline (only executes changed stages)
dvc repro

# Check pipeline status
dvc status

# Visualize pipeline DAG
dvc dag
```

### Option 3: Docker

```bash
# Build image
docker build -t churn-pipeline .

# Run pipeline
docker run churn-pipeline
```

---

## 📊 Pipeline Architecture

```
Raw Data (CSV)
    ↓
[1] Data Ingestion      ← Downloads from Kaggle
    ↓
[2] Data Validation     ← Schema checks, missing values
    ↓
[3] Data Cleaning       ← Handle nulls, duplicates, types
    ↓
[4] Feature Engineering ← Encode, scale, train/test split
    ↓
[5] Model Training      ← GridSearchCV on 3 models
    ↓                     (RandomForest, XGBoost, LightGBM)
[6] Model Selection     ← Pick best by ROC-AUC
    ↓
MLflow Model Registry   ← Register with 'production-candidate' alias
```

---

## 🔄 Automatic DVC Orchestration

**DVC automatically reruns only affected stages when:**

- **Data changes**: Modify raw CSV → reruns from ingestion
- **Code changes**: Edit any component → reruns from that stage
- **Config changes**: Update `params.yaml` → reruns training
- **Dependencies change**: Automatic detection via `deps` tracking

### Examples

```bash
# 1. Change hyperparameters → only reruns training & selection
vim config/params.yaml
dvc repro

# 2. Update cleaning logic → reruns cleaning, engineering, training, selection
vim src/components/cleaning.py
dvc repro

# 3. Replace raw data → reruns entire pipeline
cp new_data.csv data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
dvc repro

# 4. Check what would run (dry-run)
dvc status
```

---

## 📁 Project Structure

```
Customer-Churn-End-to-End-MLOps/
├── config/
│   └── params.yaml              # Hyperparameters (tracked by DVC)
│
├── data/
│   ├── raw/                     # Original dataset
│   ├── validated/               # Schema-validated data
│   └── processed/               # Cleaned data
│
├── artifacts/
│   └── feature_engineering/     # Preprocessor, train/test splits
│
├── models/                      # Trained models & leaderboard
│   ├── RandomForest.pkl
│   ├── XGBoost.pkl
│   ├── LightGBM.pkl
│   ├── model_scores.csv         # Leaderboard
│   ├── best_model.pkl           # Production model
│   └── best_model_metadata.json # Metrics
│
├── src/
│   ├── components/              # Pipeline stages
│   │   ├── ingestion.py
│   │   ├── validation.py
│   │   ├── cleaning.py
│   │   ├── feature_engineering.py
│   │   ├── model_training.py
│   │   └── model_selection.py
│   └── utils/
│       └── config_loader.py
│
├── mlruns/                      # MLflow tracking data
├── mlflow.db                    # MLflow metadata
│
├── dvc.yaml                     # DVC pipeline definition
├── main.py                      # Full pipeline runner
├── requirements.txt             # Python dependencies
└── Dockerfile                   # Container setup
```

---

## 🔬 DVC Pipeline Stages

| Stage | Command | Depends On | Outputs |
|-------|---------|------------|---------|
| `ingestion` | `python src/components/ingestion.py` | - | `data/raw/*.csv` |
| `validation` | `python src/components/validation.py` | ingestion | `data/validated/*.csv` |
| `cleaning` | `python src/components/cleaning.py` | validation | `data/processed/*.csv` |
| `feature_engineering` | `python src/components/feature_engineering.py` | cleaning | `artifacts/feature_engineering/` |
| `model_training` | `python src/components/model_training.py` | feature_engineering, `params.yaml` | `models/*.pkl`, `model_scores.csv` |
| `model_selection` | `python src/components/model_selection.py` | model_training | `best_model.pkl`, `metadata.json` |

### Run Individual Stages

```bash
# Run up to a specific stage
dvc repro feature_engineering

# Run only one stage (skip dependencies)
dvc run -n model_training python src/components/model_training.py

# Force rerun all stages
dvc repro --force
```

---

## 🧪 Model Training

### Hyperparameter Tuning (config/params.yaml)

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

**Tracked by DVC** → Changing these reruns training automatically!

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- **ROC-AUC** (selection criterion)

---

## 📈 MLflow Integration

### Launch UI

```bash
mlflow ui
# Open: http://127.0.0.1:5000
```

### Features

- **Experiment Tracking**: All runs logged with params & metrics
- **Model Registry**: Best model auto-registered
- **Model Versioning**: Automatic version management
- **Aliases**: `production-candidate` tag on best model

### Model Registry

```bash
# View registered models
mlflow models list

# Serve model for predictions
mlflow models serve -m "models:/CustomerChurnModel/production-candidate" --port 5001
```

---

## 🛠️ Development

### Run Individual Components

```bash
python src/components/ingestion.py
python src/components/validation.py
python src/components/cleaning.py
python src/components/feature_engineering.py
python src/components/model_training.py
python src/components/model_selection.py
```

### Check Pipeline Dependencies

```bash
# Visualize DAG
dvc dag

# Show stage info
dvc dag --md > pipeline.md

# Check what needs to run
dvc status
```

### DVC Commands Cheatsheet

```bash
# Pipeline execution
dvc repro                 # Run pipeline (smart execution)
dvc repro --force         # Force rerun all stages
dvc repro <stage>         # Run up to specific stage

# Pipeline inspection
dvc status                # Check modified stages
dvc dag                   # Show pipeline graph
dvc stage list            # List all stages

# Data versioning
dvc add data/raw/*.csv    # Track data file
dvc push                  # Push data to remote storage
dvc pull                  # Pull data from remote storage

# Metrics & params
dvc params diff           # Compare param changes
dvc metrics show          # Show tracked metrics
dvc plots show            # Visualize metrics
```

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build
docker build -t churn-mlops .

# Run pipeline
docker run churn-mlops

# Run with volume (preserve outputs)
docker run -v $(pwd)/models:/app/models churn-mlops

# Interactive mode
docker run -it churn-mlops bash
```

---

## 📊 Model Performance

| Model | Accuracy | ROC-AUC | Status |
|-------|----------|---------|--------|
| **LightGBM** | 80.41% | 0.8445 | ✅ Best |
| XGBoost | 80.27% | 0.8445 | - |
| RandomForest | 79.63% | 0.8408 | - |

*Best model automatically selected and registered to MLflow*

---

## 🔄 When DVC Reruns Stages

### Scenario 1: Data Update
```bash
# Replace raw data
cp new_churn_data.csv data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

# DVC detects change → reruns ALL stages
dvc repro
```

### Scenario 2: Hyperparameter Change
```bash
# Edit config/params.yaml
vim config/params.yaml  # Change n_estimators

# DVC reruns: model_training + model_selection
dvc repro
```

### Scenario 3: Code Update
```bash
# Modify cleaning logic
vim src/components/cleaning.py

# DVC reruns: cleaning → feature_engineering → training → selection
dvc repro
```

### Scenario 4: No Changes
```bash
dvc repro
# Output: "Stage 'xxx' didn't change, skipping"
# Pipeline already up-to-date
```

---

## 🚀 Future Enhancements

- [ ] FastAPI prediction service
- [ ] CI/CD with GitHub Actions
- [ ] Model monitoring dashboard
- [ ] Automated retraining triggers
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] A/B testing framework
- [ ] Feature store integration

---

## 📝 Requirements

- Python 3.11+
- See `requirements.txt` for packages

### Install

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

This is a learning project demonstrating production MLOps practices.

---

## 📧 Author

**Dhrumi**

Built to demonstrate end-to-end MLOps workflows with DVC orchestration and MLflow tracking.
