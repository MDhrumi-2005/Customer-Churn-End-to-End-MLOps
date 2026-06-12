@echo off
REM Run End-to-End MLOps Pipeline (Windows)

echo ==============================================
echo   Customer Churn MLOps Pipeline
echo ==============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo Dependencies installed
echo.

REM Run pipeline
echo Starting MLOps pipeline...
echo.
python main.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat 2>nul

echo.
echo ==============================================
echo   Pipeline execution completed
echo ==============================================
pause
