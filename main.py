#!/usr/bin/env python3
"""
End-to-End MLOps Pipeline Runner
Executes complete Customer Churn prediction workflow:
  ingestion -> validation -> cleaning -> feature_engineering -> training -> selection
"""

import sys
import time
import traceback
from pathlib import Path

# --------------------------------------------------------
# Import pipeline components
# --------------------------------------------------------
from src.components.ingestion import ingest_data
from src.components.validation import validate_data
from src.components.cleaning import DataCleaner
from src.components.feature_engineering import FeatureEngineering
from src.components.model_training import ModelTrainer
from src.components.model_selection import ModelSelector


def separator(title=""):
    line = "=" * 70
    if title:
        print("\n" + line)
        print(f"  {title}")
        print(line + "\n")
    else:
        print("\n" + line + "\n")


def run_pipeline():
    """
    Execute complete end-to-end MLOps pipeline.

    Stages:
      1. Data Ingestion      - Download dataset (KaggleHub / local fallback)
      2. Data Validation     - Schema and integrity checks
      3. Data Cleaning       - Missing values, duplicates, type fixes
      4. Feature Engineering - Encoding, scaling, train/test split
      5. Model Training      - RF + XGBoost + LightGBM with GridSearchCV
      6. Model Selection     - Pick best by ROC-AUC, register to MLflow
    """

    pipeline_start = time.time()

    try:

        # ============================================================
        # STAGE 1: DATA INGESTION
        # ============================================================
        separator("STAGE 1/6 : DATA INGESTION")

        raw_data_path = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

        if raw_data_path.exists():
            print(f"Dataset already present at: {raw_data_path}")
            print("Skipping download.")
        else:
            print("Downloading dataset from KaggleHub...")
            ingest_data()

        print("\n[OK] Stage 1 complete")

        # ============================================================
        # STAGE 2: DATA VALIDATION
        # ============================================================
        separator("STAGE 2/6 : DATA VALIDATION")
        validate_data()
        print("\n[OK] Stage 2 complete")

        # ============================================================
        # STAGE 3: DATA CLEANING
        # ============================================================
        separator("STAGE 3/6 : DATA CLEANING")
        cleaner = DataCleaner()
        cleaner.clean_data()
        print("\n[OK] Stage 3 complete")

        # ============================================================
        # STAGE 4: FEATURE ENGINEERING
        # ============================================================
        separator("STAGE 4/6 : FEATURE ENGINEERING")
        engineer = FeatureEngineering()
        engineer.process()
        print("\n[OK] Stage 4 complete")

        # ============================================================
        # STAGE 5: MODEL TRAINING
        # ============================================================
        separator("STAGE 5/6 : MODEL TRAINING")
        trainer = ModelTrainer()
        trainer.train()
        print("\n[OK] Stage 5 complete")

        # ============================================================
        # STAGE 6: MODEL SELECTION & MLFLOW REGISTRY
        # ============================================================
        separator("STAGE 6/6 : MODEL SELECTION & REGISTRY")
        selector = ModelSelector()
        selector.select_best_model()
        print("\n[OK] Stage 6 complete")

        # ============================================================
        # PIPELINE COMPLETION SUMMARY
        # ============================================================
        elapsed = time.time() - pipeline_start
        separator("PIPELINE COMPLETE")

        print(f"Total runtime : {elapsed:.1f}s  ({elapsed/60:.1f} min)")

        print("\nGenerated artifacts:")
        print("  data/validated/validated_churn.csv")
        print("  data/processed/cleaned_churn.csv")
        print("  artifacts/feature_engineering/")
        print("    - preprocessor.pkl")
        print("    - X_train.csv  X_test.csv")
        print("    - y_train.csv  y_test.csv")
        print("  models/")
        print("    - RandomForest.pkl")
        print("    - XGBoost.pkl")
        print("    - LightGBM.pkl")
        print("    - model_scores.csv")
        print("    - best_model.pkl")
        print("    - best_model_metadata.json")

        print("\nMLflow:")
        print("  Experiment  : Customer_Churn")
        print("  Registry    : CustomerChurnModel")
        print("  Alias       : production-candidate")

        print("\nNext steps:")
        print("  View MLflow UI  :  mlflow ui")
        print("  Open browser    :  http://127.0.0.1:5000")
        print("  Rerun pipeline  :  dvc repro")

        return 0

    except Exception as exc:
        separator("PIPELINE FAILED")
        print(f"Error : {exc}")
        print(f"Type  : {type(exc).__name__}")
        print("\nTraceback:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
