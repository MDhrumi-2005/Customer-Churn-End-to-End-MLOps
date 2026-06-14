# =============================================================
# Customer Churn MLOps - Dockerfile
#
# Two-stage build:
#   Stage 1 (trainer): runs the full ML pipeline to produce
#                       trained model artifacts
#   Stage 2 (api):     copies only the artifacts + app code
#                       into a lean image and starts FastAPI
#
# Build & run:
#   docker build -t mlops-churn-pipeline .
#   docker run -p 8000:8000 mlops-churn-pipeline
#
# Pull from Docker Hub and run:
#   docker pull MDhrumi2005/mlops-churn-pipeline:latest
#   docker run -p 8000:8000 MDhrumi2005/mlops-churn-pipeline:latest
#
# API available at:  http://localhost:8000
# Swagger UI at:     http://localhost:8000/docs
# =============================================================

# -------------------------------------------------------------
# STAGE 1 — TRAINER
# Installs all dependencies, copies data, runs full pipeline,
# produces trained artifacts in models/ and artifacts/
# -------------------------------------------------------------
FROM python:3.11-slim AS trainer

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Create required directories
RUN mkdir -p data/raw data/validated data/processed \
             artifacts/feature_engineering \
             models mlruns reports

# Set MLflow to use a local SQLite DB
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI=sqlite:///mlflow.db

# Run the full pipeline — produces:
#   models/best_model.pkl
#   models/best_model_metadata.json
#   models/model_scores.csv
#   artifacts/feature_engineering/preprocessor.pkl
#   artifacts/feature_engineering/X_train.csv etc.
RUN python main.py


# -------------------------------------------------------------
# STAGE 2 — API
# Lean image: only what the FastAPI server needs
# No training code, no heavy ML libs for training
# -------------------------------------------------------------
FROM python:3.11-slim AS api

WORKDIR /app

# Install only inference dependencies (smaller image)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app_api.py .
COPY src/ ./src/

# Copy trained artifacts from stage 1
COPY --from=trainer /app/models/ ./models/
COPY --from=trainer /app/artifacts/ ./artifacts/

ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 8000

# Start FastAPI — model is already trained and ready
CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]
