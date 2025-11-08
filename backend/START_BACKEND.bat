@echo off
title Climate Tracker - Advocacy API (SQLite)
chcp 65001 >nul 2>&1

:: Get the directory where this script is located
cd /d "%~dp0"

echo ============================================================
echo Starting Climate Tracker Advocacy API (SQLite)
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
if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo Killing any existing backend processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend on port 8000...
echo API Documentation will be available at: http://localhost:8000/docs
echo.

python -m uvicorn app_advocacy_sqlite:app --host 0.0.0.0 --port 8000 --reload

pause
