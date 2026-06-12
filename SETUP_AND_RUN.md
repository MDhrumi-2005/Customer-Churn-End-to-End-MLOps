# 🚀 Setup and Run - Complete Guide

## ⚡ TL;DR (Too Long; Didn't Read)

```bash
# Install dependencies
pip install -r requirements.txt

# Run pipeline (DVC automatic execution)
dvc repro

# View results
mlflow ui
```

Done! 🎉

---

## 📋 Detailed Setup

### Step 1: Environment Setup

**Windows:**
```bash
# Automated setup
setup_environment.bat

# Or manual
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Check Python packages
python -c "import mlflow, lightgbm, xgboost, dvc; print('All packages installed!')"

# Check DVC setup
dvc version
```

---

## 🎯 Running the Pipeline

### Option 1: DVC (Recommended - Automatic)

```bash
# Run entire pipeline (only changed stages execute)
dvc repro

# Check what would run first
dvc status

# Force rerun everything
dvc repro --force

# Run up to specific stage
dvc repro feature_engineering
```

**Benefits:**
- ✅ Only runs changed stages
- ✅ Automatic dependency detection
- ✅ Cached outputs for speed
- ✅ Reproducible results

### Option 2: Python Script (Manual - Full Pipeline)

```bash
# Run all 6 stages sequentially
python main.py
```

**Benefits:**
- ✅ Complete end-to-end execution
- ✅ Detailed progress output
- ✅ No DVC required
- ✅ Good for first-time run

### Option 3: Individual Stages

```bash
# Run one stage at a time
python src/components/ingestion.py
python src/components/validation.py
python src/components/cleaning.py
python src/components/feature_engineering.py
python src/components/model_training.py
python src/components/model_selection.py
```

**Benefits:**
- ✅ Debug specific stage
- ✅ Test individual component
- ✅ Fast iteration during development

### Option 4: Docker

```bash
# Build image
docker build -t churn-mlops .

# Run container
docker run churn-mlops

# Run with volume mounting (preserve outputs)
docker run -v $(pwd)/models:/app/models churn-mlops
```

**Benefits:**
- ✅ Isolated environment
- ✅ Production deployment ready
- ✅ Consistent across machines

---

## 📊 View Results

### 1. Model Leaderboard

```bash
# View model scores
cat models/model_scores.csv
```

**Output:**
```csv
model,accuracy,precision,recall,f1_score,roc_auc
LightGBM,0.8041,0.6538,0.5537,0.5997,0.8445
XGBoost,0.8027,0.6471,0.5518,0.5952,0.8445
RandomForest,0.7963,0.6319,0.5195,0.5702,0.8408
```

### 2. Best Model Metadata

```bash
# View best model info
cat models/best_model_metadata.json
```

**Output:**
```json
{
    "best_model": "LightGBM",
    "accuracy": 0.8041,
    "precision": 0.6538,
    "recall": 0.5537,
    "f1_score": 0.5997,
    "roc_auc": 0.8445
}
```

### 3. MLflow UI

```bash
# Launch web interface
mlflow ui

# Open browser
http://127.0.0.1:5000
```

**Features:**
- 📊 Experiment comparison
- 📈 Metric visualization
- 🏷️ Model registry
- 📦 Artifact browsing

### 4. Pipeline Visualization

```bash
# Show DAG
dvc dag
```

**Output:**
```
  +--------------------+  
  | data/raw/*.csv     |  
  +--------------------+  
           *              
           *              
           *              
  +--------------------+  
  | ingestion          |  
  +--------------------+  
           *              
           *              
           *              
  +--------------------+  
  | validation         |  
  +--------------------+  
  **        **            
 *            **          
*               **        
  +--------------------+  
  | cleaning           |  
  +--------------------+  
           *              
           *              
           *              
  +--------------------+  
  | feature_engineering|  
  +--------------------+  
  **        **            
 *            **          
*               **        
  +--------------------+  
  | model_training     |  
  +--------------------+  
           *              
           *              
           *              
  +--------------------+  
  | model_selection    |  
  +--------------------+  
```

---

## 🔄 DVC Automatic Rerun Scenarios

### Scenario 1: Update Raw Data
```bash
# Replace dataset
cp new_data.csv data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

# DVC reruns: ALL 6 stages
dvc repro
```

### Scenario 2: Change Hyperparameters
```bash
# Edit config
vim config/params.yaml
# Change: n_estimators, max_depth, etc.

# DVC reruns: model_training + model_selection (2 stages)
dvc repro
```

### Scenario 3: Modify Code
```bash
# Edit any component
vim src/components/cleaning.py

# DVC reruns: cleaning + all downstream stages (4 stages)
dvc repro
```

### Scenario 4: No Changes
```bash
# Check status
dvc repro

# Output: "Pipeline is up to date!" (0 stages run)
```

---

## 🧪 Testing DVC Automation

```bash
# Run comprehensive test suite
python test_dvc_automation.py
```

**Tests:**
- ✓ DVC status checking
- ✓ Parameter change detection
- ✓ Code change detection
- ✓ Data validation
- ✓ Stage listing

---

## 📂 Generated Artifacts

After successful run, you'll have:

```
data/
├── validated/
│   └── validated_churn.csv      ✓ Schema-validated data
└── processed/
    └── cleaned_churn.csv         ✓ Clean data ready for ML

artifacts/
└── feature_engineering/
    ├── preprocessor.pkl          ✓ Sklearn pipeline
    ├── X_train.csv               ✓ Training features
    ├── X_test.csv                ✓ Test features
    ├── y_train.csv               ✓ Training labels
    └── y_test.csv                ✓ Test labels

models/
├── RandomForest.pkl              ✓ Trained model
├── XGBoost.pkl                   ✓ Trained model
├── LightGBM.pkl                  ✓ Trained model (best)
├── model_scores.csv              ✓ Leaderboard
├── best_model.pkl                ✓ Production model
└── best_model_metadata.json     ✓ Performance metrics

mlruns/
└── [experiment_id]/
    └── [run_id]/
        └── artifacts/            ✓ MLflow logged models
```

---

## 🆘 Troubleshooting

### Issue: NumPy version errors
**Error:** `AttributeError: _ARRAY_API not found`

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Why:** requirements.txt uses NumPy < 2.0 for compatibility

---

### Issue: kagglehub credentials
**Error:** `kagglehub authentication failed`

**Solution 1 - Skip ingestion (dataset exists):**
```bash
# Dataset already in data/raw/, start from validation
dvc repro validation
```

**Solution 2 - Setup Kaggle credentials:**
```bash
# Create ~/.kaggle/kaggle.json
{
  "username": "your_username",
  "key": "your_api_key"
}

# Or set environment variables
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key
```

**Solution 3 - Manual download:**
Download from https://www.kaggle.com/datasets/blastchar/telco-customer-churn
Place in `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

---

### Issue: MLflow database locked
**Error:** `database is locked`

**Solution:**
```bash
# Stop any running MLflow UI
pkill -f "mlflow ui"

# Remove lock file
rm mlflow.db-journal

# Restart
mlflow ui
```

---

### Issue: DVC stage failed
**Error:** `Stage 'xxx' failed`

**Solution:**
```bash
# Run stage individually for detailed error
python src/components/xxx.py

# Check logs
dvc repro --verbose

# Force clean run
dvc repro --force
```

---

## 🎓 Learn More

### Documentation
- [README.md](README.md) - Complete project docs
- [QUICKSTART.md](QUICKSTART.md) - 3-step quick start
- [DVC_AUTOMATION_GUIDE.md](DVC_AUTOMATION_GUIDE.md) - DVC deep dive
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - What was fixed

### External Resources
- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Kaggle Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 🎯 Next Steps

### 1. Run Initial Pipeline
```bash
dvc repro
```

### 2. Experiment with Hyperparameters
```bash
vim config/params.yaml
dvc repro
```

### 3. View Results in MLflow
```bash
mlflow ui
```

### 4. Compare Experiments
```bash
dvc params diff
dvc metrics diff
```

### 5. Deploy Best Model
```bash
# Serve model locally
mlflow models serve -m "models:/CustomerChurnModel/production-candidate" --port 5001

# Test prediction
curl -X POST http://localhost:5001/invocations \
  -H 'Content-Type: application/json' \
  -d '{"data": [...]}'
```

---

## 🎉 You're All Set!

Your MLOps pipeline is ready with:

✅ Automatic DVC orchestration
✅ MLflow experiment tracking
✅ Model registry integration
✅ Production-ready structure
✅ Comprehensive documentation

**Run `dvc repro` and watch the magic happen!** 🚀
