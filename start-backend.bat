@echo off
title Climate Tracker - Backend Server
chcp 65001 >nul 2>&1

:: Get the directory where this script is located and navigate to backend
cd /d "%~dp0backend"

:: Check if backend directory exists
if not exist "start_dev.py" (
    echo Error: Cannot find backend files
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

echo ========================================
echo   Starting Climate Tracker Backend
echo ========================================
echo.

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Start the backend server
echo.
echo Starting backend server...
python start_dev.py

pause