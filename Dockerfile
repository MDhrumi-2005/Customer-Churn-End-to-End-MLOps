# =============================================================
# Customer Churn MLOps - Dockerfile
#
# Lightweight single-stage build.
# Trained model artifacts are already in the repo (models/ and
# artifacts/) so no training happens at build time.
# The container starts FastAPI immediately on port 8000.
#
# Build & run locally:
#   docker build -t mlops-churn-pipeline .
#   docker run -p 8000:8000 mlops-churn-pipeline
#
# Pull from Docker Hub and run:
#   docker pull dhrumi2910/mlops-churn-pipeline:latest
#   docker run -p 8000:8000 dhrumi2910/mlops-churn-pipeline:latest
#
# API:        http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# =============================================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app_api.py .
COPY src/ ./src/
COPY config/ ./config/

# Copy pre-trained artifacts (already committed to repo)
COPY models/ ./models/
COPY artifacts/ ./artifacts/

# Set environment
ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 8000

# Start FastAPI — model already trained, starts instantly
CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]
