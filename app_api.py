"""
FastAPI Inference Service - Customer Churn Prediction
Serves the best trained model for real-time predictions.

Endpoints:
  GET  /          - Health check
  POST /predict   - Predict churn (0 = Stay, 1 = Churn)

Usage:
  uvicorn app_api:app --host 0.0.0.0 --port 8000 --reload

Swagger UI:
  http://127.0.0.1:8000/docs
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# -------------------------------------------------------
# App Setup
# -------------------------------------------------------

app = FastAPI(
    title="Customer Churn Prediction API",
    description="MLOps pipeline inference service. Predicts whether a customer will churn.",
    version="1.0.0"
)

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

MODEL_PATH       = "models/best_model.pkl"
PREPROCESSOR_PATH = "artifacts/feature_engineering/preprocessor.pkl"
METADATA_PATH    = "models/best_model_metadata.json"

# -------------------------------------------------------
# Load model and preprocessor at startup
# -------------------------------------------------------

model        = None
preprocessor = None
metadata     = {}


def load_artifacts():
    """Load model, preprocessor and metadata into memory."""
    global model, preprocessor, metadata

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Best model not found at {MODEL_PATH}. "
            "Run the training pipeline first: python main.py"
        )

    if not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError(
            f"Preprocessor not found at {PREPROCESSOR_PATH}. "
            "Run the training pipeline first: python main.py"
        )

    model        = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

    print(f"[OK] Model loaded        : {MODEL_PATH}")
    print(f"[OK] Preprocessor loaded : {PREPROCESSOR_PATH}")
    print(f"[OK] Best model          : {metadata.get('best_model', 'Unknown')}")
    print(f"[OK] ROC-AUC             : {metadata.get('roc_auc', 'N/A')}")


# Load on startup
try:
    load_artifacts()
except FileNotFoundError as e:
    print(f"[WARN] {e}")
    print("[WARN] API will start but /predict will fail until model is trained.")


# -------------------------------------------------------
# Request / Response Schemas
# -------------------------------------------------------

class CustomerFeatures(BaseModel):
    """Input features matching the Telco Customer Churn dataset."""

    gender:           str   = Field(..., example="Female",         description="Male or Female")
    SeniorCitizen:    int   = Field(..., example=0,                 description="1 = Senior, 0 = Not senior")
    Partner:          str   = Field(..., example="Yes",             description="Yes or No")
    Dependents:       str   = Field(..., example="No",              description="Yes or No")
    tenure:           float = Field(..., example=12,                description="Months with company")
    PhoneService:     str   = Field(..., example="Yes",             description="Yes or No")
    MultipleLines:    str   = Field(..., example="No",              description="Yes / No / No phone service")
    InternetService:  str   = Field(..., example="Fiber optic",     description="DSL / Fiber optic / No")
    OnlineSecurity:   str   = Field(..., example="No",              description="Yes / No / No internet service")
    OnlineBackup:     str   = Field(..., example="Yes",             description="Yes / No / No internet service")
    DeviceProtection: str   = Field(..., example="No",              description="Yes / No / No internet service")
    TechSupport:      str   = Field(..., example="No",              description="Yes / No / No internet service")
    StreamingTV:      str   = Field(..., example="No",              description="Yes / No / No internet service")
    StreamingMovies:  str   = Field(..., example="No",              description="Yes / No / No internet service")
    Contract:         str   = Field(..., example="Month-to-month",  description="Month-to-month / One year / Two year")
    PaperlessBilling: str   = Field(..., example="Yes",             description="Yes or No")
    PaymentMethod:    str   = Field(..., example="Electronic check",description="Payment method")
    MonthlyCharges:   float = Field(..., example=29.85,             description="Monthly bill amount")
    TotalCharges:     float = Field(..., example=358.2,             description="Total amount billed")


class PredictionResponse(BaseModel):
    prediction:       int   = Field(..., description="0 = Will Stay, 1 = Will Churn")
    probability_churn: float = Field(..., description="Probability of churning (0.0 to 1.0)")
    label:            str   = Field(..., description="Human-readable prediction")
    model_used:       str   = Field(..., description="Model that made this prediction")


class HealthResponse(BaseModel):
    message:    str
    model:      Optional[str] = None
    roc_auc:    Optional[float] = None
    status:     str


# -------------------------------------------------------
# Endpoints
# -------------------------------------------------------

@app.get("/", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Health check - confirms the API is running."""
    return {
        "message": "MLOps Customer Churn API is running",
        "model":   metadata.get("best_model"),
        "roc_auc": metadata.get("roc_auc"),
        "status":  "ready" if model is not None else "model_not_loaded"
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(customer: CustomerFeatures):
    """
    Predict whether a customer will churn.

    - **prediction**: 0 = Customer will stay, 1 = Customer will churn
    - **probability_churn**: Confidence score (0.0 to 1.0)
    - **label**: Human-readable result
    """

    if model is None or preprocessor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run the training pipeline first: python main.py"
        )

    # Build a single-row DataFrame matching training feature order
    input_data = pd.DataFrame([{
        "gender":           customer.gender,
        "SeniorCitizen":    customer.SeniorCitizen,
        "Partner":          customer.Partner,
        "Dependents":       customer.Dependents,
        "tenure":           customer.tenure,
        "PhoneService":     customer.PhoneService,
        "MultipleLines":    customer.MultipleLines,
        "InternetService":  customer.InternetService,
        "OnlineSecurity":   customer.OnlineSecurity,
        "OnlineBackup":     customer.OnlineBackup,
        "DeviceProtection": customer.DeviceProtection,
        "TechSupport":      customer.TechSupport,
        "StreamingTV":      customer.StreamingTV,
        "StreamingMovies":  customer.StreamingMovies,
        "Contract":         customer.Contract,
        "PaperlessBilling": customer.PaperlessBilling,
        "PaymentMethod":    customer.PaymentMethod,
        "MonthlyCharges":   customer.MonthlyCharges,
        "TotalCharges":     customer.TotalCharges,
    }])

    # Apply the same preprocessing used during training
    try:
        X_processed = preprocessor.transform(input_data)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Preprocessing failed: {str(e)}"
        )

    # Make prediction
    prediction     = int(model.predict(X_processed)[0])
    probability    = float(model.predict_proba(X_processed)[0][1])
    label          = "Will Churn" if prediction == 1 else "Will Stay"
    model_name     = metadata.get("best_model", "Unknown")

    return {
        "prediction":        prediction,
        "probability_churn": round(probability, 4),
        "label":             label,
        "model_used":        model_name
    }
