@echo off
title Climate Tracker - Flask Backend (Port 5000)
chcp 65001 >nul 2>&1

:: Get the directory where this script is located
cd /d "%~dp0"

echo ============================================================
echo Starting Flask Backend for CCUS on port 5000
echo ============================================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies if needed
if not exist "venv\Lib\site-packages\flask" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Set environment variables
set PORT=5000
set HOST=0.0.0.0

:: Start Flask app
echo.
echo Starting Flask application...
python app.py

pause
