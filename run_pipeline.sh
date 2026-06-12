#!/bin/bash
# Run End-to-End MLOps Pipeline

set -e  # Exit on error

echo "=============================================="
echo "  Customer Churn MLOps Pipeline"
echo "=============================================="
echo ""

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found"
    exit 1
fi

echo "✓ Python: $(python --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run pipeline
echo "Starting MLOps pipeline..."
echo ""
python main.py

# Deactivate virtual environment
deactivate 2>/dev/null || true

echo ""
echo "=============================================="
echo "  Pipeline execution completed"
echo "=============================================="
