FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create necessary directories
RUN mkdir -p data/raw data/validated data/processed \
             artifacts/feature_engineering \
             models mlruns

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI=sqlite:///mlflow.db

# Expose API port
EXPOSE 8000

# Default: run full pipeline then start API
# Override with: docker run ... python main.py  (pipeline only)
CMD ["sh", "-c", "python main.py && uvicorn app_api:app --host 0.0.0.0 --port 8000"]