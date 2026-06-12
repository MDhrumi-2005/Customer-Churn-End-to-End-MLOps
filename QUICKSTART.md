# ⚡ Quick Start Guide

## 🎯 Goal

Run the complete Customer Churn MLOps pipeline in **3 simple steps**.

---

## 📋 Prerequisites

- Python 3.11+
- pip installed

---

## 🚀 3-Step Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Pipeline

**Option A: Using main.py (Full Pipeline)**
```bash
python main.py
```

**Option B: Using DVC (Smart Execution)**
```bash
dvc repro
```

### Step 3: View Results

```bash
# View model leaderboard
cat models/model_scores.csv

# View best model metadata
cat models/best_model_metadata.json

# Launch MLflow UI
mlflow ui
# Open: http://127.0.0.1:5000
```

---

## ✅ What Happens

The pipeline automatically:

1. ✓ Downloads Telco Customer Churn dataset
2. ✓ Validates data schema
3. ✓ Cleans missing values & duplicates
4. ✓ Engineers features (encoding, scaling)
5. ✓ Trains 3 models with GridSearchCV:
   - RandomForest
   - XGBoost
   - LightGBM
6. ✓ Selects best model by ROC-AUC
7. ✓ Registers best model to MLflow

---

## 📊 Expected Output

```
models/
├── RandomForest.pkl       ← Trained model
├── XGBoost.pkl            ← Trained model
├── LightGBM.pkl           ← Trained model (best)
├── model_scores.csv       ← Leaderboard
├── best_model.pkl         ← Production-ready model
└── best_model_metadata.json  ← Metrics & info
```

**Best Model Metrics:**
- Model: LightGBM
- Accuracy: ~80.4%
- ROC-AUC: ~0.844

---

## 🔄 DVC Automatic Rerun

DVC **only reruns changed stages**:

```bash
# Scenario 1: Change hyperparameters
vim config/params.yaml      # Edit n_estimators
dvc repro                   # Only reruns: training + selection

# Scenario 2: Update data
cp new.csv data/raw/...     # Replace dataset
dvc repro                   # Reruns: ALL stages

# Scenario 3: No changes
dvc repro                   # Output: "Pipeline is up to date"
```

---

## 🆘 Troubleshooting

### Issue: `kagglehub` fails (no Kaggle credentials)

**Solution:** Dataset already included in `data/raw/`
```bash
# Skip ingestion, start from validation
python src/components/validation.py
python src/components/cleaning.py
python src/components/feature_engineering.py
python src/components/model_training.py
python src/components/model_selection.py
```

### Issue: NumPy compatibility errors

**Solution:** Use clean requirements.txt
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: MLflow not found

**Solution:**
```bash
pip install mlflow==2.14.3
```

---

## 📖 Next Steps

- [Full README](README.md) - Complete documentation
- [DVC Commands](README.md#dvc-commands-cheatsheet) - Pipeline management
- [MLflow UI](http://127.0.0.1:5000) - Experiment tracking

---

## 🎓 Learn More

- **DVC Docs**: https://dvc.org/doc
- **MLflow Docs**: https://mlflow.org/docs/latest/index.html
- **Kaggle Dataset**: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

---

**Total Pipeline Runtime:** ~3-5 minutes (depends on hardware)

🎉 You're now running production-grade MLOps!
