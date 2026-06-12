@echo off
REM Setup script for Windows

echo ======================================
echo  MLOps Pipeline Environment Setup
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    exit /b 1
)

echo [1/4] Python found
python --version

REM Create virtual environment
if not exist "venv\" (
    echo.
    echo [2/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo.
    echo [2/4] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --quiet --upgrade pip

REM Install dependencies
echo.
echo [4/4] Installing dependencies...
pip install --quiet -r requirements.txt

echo.
echo ======================================
echo  Setup Complete!
echo ======================================
echo.
echo Next steps:
echo   1. Run pipeline: python main.py
echo   2. Or use DVC: dvc repro
echo   3. View MLflow UI: mlflow ui
echo.
echo To activate the environment manually:
echo   venv\Scripts\activate.bat
echo.

pause
