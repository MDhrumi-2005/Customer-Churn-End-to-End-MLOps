# 🔄 DVC Automatic Pipeline Execution Guide

## 🎯 What is DVC Automation?

**DVC (Data Version Control)** automatically detects changes in:
- 📊 **Data files** (raw CSVs, processed data)
- 🐍 **Code files** (Python scripts)
- ⚙️ **Config files** (params.yaml)

When you run `dvc repro`, it **only executes stages that changed** or have changed dependencies.

---

## 📊 Your Pipeline Dependency Graph

```
data/raw/*.csv  ───────┐
                       ↓
               [1] ingestion
                       ↓
           data/raw/WA_Fn-UseC...csv  ─────┐
           validation.py ──────────────────┤
                                           ↓
                                   [2] validation
                                           ↓
                      data/validated/*.csv ─────┐
                      cleaning.py ──────────────┤
                                                ↓
                                        [3] cleaning
                                                ↓
                     data/processed/*.csv ──────┐
                     feature_engineering.py ────┤
                                                ↓
                                  [4] feature_engineering
                                                ↓
                       artifacts/feature_eng/ ──┐
                       model_training.py ────────┤
                       params.yaml ───────────────┤
                                                  ↓
                                         [5] model_training
                                                  ↓
                            models/*.pkl ─────────┐
                            model_scores.csv ─────┤
                            model_selection.py ───┤
                                                  ↓
                                         [6] model_selection
                                                  ↓
                                    best_model.pkl + metadata.json
```

---

## 🧪 Automatic Rerun Examples

### Example 1: Change Raw Data
**Scenario:** You get a new dataset with more customers

```bash
# Replace raw data
cp new_churn_data.csv data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

# Check what will run
dvc status
```

**Output:**
```
Data and pipelines are up to date.
Run 'dvc repro' to reproduce.
```

```bash
# Execute pipeline
dvc repro
```

**What Runs:**
```
✓ Running stage 'ingestion'         [SKIP - data already updated]
✓ Running stage 'validation'        [EXECUTE - data changed]
✓ Running stage 'cleaning'          [EXECUTE - upstream changed]
✓ Running stage 'feature_engineering' [EXECUTE - upstream changed]
✓ Running stage 'model_training'    [EXECUTE - upstream changed]
✓ Running stage 'model_selection'   [EXECUTE - upstream changed]
```

**Result:** 🔥 **5 stages rerun** (validation through selection)

---

### Example 2: Change Hyperparameters
**Scenario:** You want to try more trees in RandomForest

```bash
# Edit config
vim config/params.yaml

# Change:
# random_forest:
#   n_estimators: [100, 200]  ← OLD
#   n_estimators: [100, 200, 300]  ← NEW

# Check status
dvc status
```

**Output:**
```
model_training:
    changed deps:
        modified:           config/params.yaml
model_selection:
    changed deps:
        modified:           models/model_scores.csv (dependency)
```

```bash
# Execute
dvc repro
```

**What Runs:**
```
✓ Stage 'ingestion' didn't change, skipping
✓ Stage 'validation' didn't change, skipping  
✓ Stage 'cleaning' didn't change, skipping
✓ Stage 'feature_engineering' didn't change, skipping
✓ Running stage 'model_training'    [EXECUTE - params changed]
✓ Running stage 'model_selection'   [EXECUTE - upstream changed]
```

**Result:** 🎯 **Only 2 stages rerun** (training + selection)

---

### Example 3: Change Cleaning Logic
**Scenario:** You improve how missing values are handled

```bash
# Edit cleaning code
vim src/components/cleaning.py

# Add better imputation logic
# ...

# Check status
dvc status
```

**Output:**
```
cleaning:
    changed deps:
        modified:           src/components/cleaning.py
feature_engineering:
    changed deps:
        modified:           data/processed/cleaned_churn.csv
model_training:
    changed deps:
        modified:           artifacts/feature_engineering
...
```

```bash
# Execute
dvc repro
```

**What Runs:**
```
✓ Stage 'ingestion' didn't change, skipping
✓ Stage 'validation' didn't change, skipping
✓ Running stage 'cleaning'          [EXECUTE - code changed]
✓ Running stage 'feature_engineering' [EXECUTE - upstream changed]
✓ Running stage 'model_training'    [EXECUTE - upstream changed]
✓ Running stage 'model_selection'   [EXECUTE - upstream changed]
```

**Result:** 🔄 **4 stages rerun** (cleaning through selection)

---

### Example 4: No Changes
**Scenario:** You just want to check if pipeline is up-to-date

```bash
dvc repro
```

**Output:**
```
✓ Stage 'ingestion' didn't change, skipping
✓ Stage 'validation' didn't change, skipping
✓ Stage 'cleaning' didn't change, skipping
✓ Stage 'feature_engineering' didn't change, skipping
✓ Stage 'model_training' didn't change, skipping
✓ Stage 'model_selection' didn't change, skipping

Pipeline is up to date!
```

**Result:** ⚡ **0 stages run** (nothing changed)

---

## 🎓 Advanced DVC Commands

### Force Rerun Everything
```bash
# Ignore cache, run all stages
dvc repro --force
```

### Run Up To Specific Stage
```bash
# Only run validation + cleaning
dvc repro cleaning

# Only run ingestion + validation + cleaning + feature_engineering
dvc repro feature_engineering
```

### Dry Run (Check What Would Execute)
```bash
# See what would run WITHOUT executing
dvc status

# More detailed output
dvc status --verbose
```

### Visualize Pipeline
```bash
# ASCII graph
dvc dag

# Markdown format
dvc dag --md

# Mermaid diagram
dvc dag --mermaid
```

### Compare Parameter Versions
```bash
# Show param changes between commits
dvc params diff

# Compare specific commits
dvc params diff HEAD~1 HEAD
```

### Track Metrics Over Time
```bash
# Show current metrics
dvc metrics show

# Compare metrics across commits
dvc metrics diff
```

---

## 🔍 How DVC Detects Changes

### 1. **File Hash Comparison**
DVC computes MD5 hash of each tracked file:
```bash
# dvc.lock stores hashes
cat dvc.lock
```

### 2. **Dependency Tracking**
Each stage declares its `deps`:
```yaml
model_training:
  deps:
    - artifacts/feature_engineering  ← If this changes...
    - src/components/model_training.py  ← ...or this changes...
    - config/params.yaml  ← ...or this changes...
  outs:
    - models/  ← ...then rerun this stage
```

### 3. **Output Tracking**
Each stage declares its `outs`:
```yaml
cleaning:
  outs:
    - data/processed/cleaned_churn.csv  ← Tracked output

feature_engineering:
  deps:
    - data/processed/cleaned_churn.csv  ← Depends on cleaning output
```

### 4. **Parameter Tracking**
Specific config keys are tracked:
```yaml
model_training:
  params:
    - random_forest  ← Only these params
    - xgboost        ← trigger rerun
    - lightgbm
    - cv_folds
    - selection_metric
```

---

## 🎯 Best Practices

### 1. Always Check Status First
```bash
dvc status  # What would run?
dvc repro   # Execute it
```

### 2. Use Descriptive Commit Messages
```bash
git commit -m "feat: improve missing value imputation in cleaning"
dvc repro
git add dvc.lock  # Track pipeline state
git commit -m "chore: update dvc.lock after cleaning improvements"
```

### 3. Track Experiments
```bash
# Before major change
git tag v1.0-baseline

# Make changes
vim config/params.yaml
dvc repro

# Save experiment
git tag v1.1-experiment

# Compare
dvc params diff v1.0-baseline v1.1-experiment
dvc metrics diff v1.0-baseline v1.1-experiment
```

### 4. Use DVC Remote for Data
```bash
# Add remote storage (S3, GCS, Azure, etc.)
dvc remote add -d myremote s3://mybucket/dvcstore

# Push data
dvc push

# Team members can pull
dvc pull
```

---

## 🚀 Quick Reference

| Command | Purpose |
|---------|---------|
| `dvc repro` | Run changed stages only |
| `dvc repro --force` | Force rerun all stages |
| `dvc repro <stage>` | Run up to specific stage |
| `dvc status` | Check what would run |
| `dvc dag` | Show pipeline graph |
| `dvc stage list` | List all stages |
| `dvc params diff` | Compare parameters |
| `dvc metrics show` | Show tracked metrics |
| `dvc push` | Upload data to remote |
| `dvc pull` | Download data from remote |

---

## 💡 Tips

1. **DVC is Git-aware**: It integrates with Git for versioning
2. **Cached outputs**: DVC caches outputs - rerun is FAST if code unchanged
3. **Reproducibility**: Anyone can clone repo + `dvc repro` → same results
4. **Scalability**: Works with datasets too large for Git
5. **Cloud-ready**: Supports S3, GCS, Azure, SSH, HTTP remotes

---

## 🎉 Summary

**Your pipeline NOW has:**

✅ **Automatic change detection** (data, code, config)
✅ **Smart execution** (only changed stages run)
✅ **Dependency tracking** (upstream changes propagate)
✅ **Parameter versioning** (track hyperparameter experiments)
✅ **Metric tracking** (compare model performance)
✅ **Reproducibility** (anyone can reproduce results)
✅ **Caching** (fast reruns when possible)

**Run:** `dvc repro` and let DVC handle the rest! 🚀
