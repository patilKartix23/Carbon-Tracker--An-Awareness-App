@echo off
title Climate Tracker - Startup
color 0A
chcp 65001 >nul 2>&1

:: Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ========================================
echo   🌍 Climate Tracker Application
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Error: frontend directory not found
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Error: backend directory not found
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

:: Ask user what to start
echo What would you like to start?
echo.
echo 1. Both Frontend and Backend (Recommended)
echo 2. Frontend only (React)
echo 3. Backend only (FastAPI)
echo 4. Clean install and start both
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto start_both
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_backend
if "%choice%"=="4" goto clean_start
echo Invalid choice. Starting both services...
goto start_both

:clean_start
echo.
echo 🧹 Cleaning previous installations...
if exist "frontend\node_modules" (
    echo Removing frontend\node_modules...
    rmdir /s /q "frontend\node_modules"
)
if exist "backend\venv" (
    echo Removing backend\venv...
    rmdir /s /q "backend\venv"
)
echo ✅ Clean completed
goto start_both

:start_both
echo.
echo 🚀 Starting both Frontend and Backend...
echo.
echo This will open two command windows:
echo - Backend (FastAPI) on http://localhost:8000
echo - Frontend (React) on http://localhost:3000
echo.
echo Starting backend...
start "Climate Tracker - Backend" cmd /k "cd /d "%~dp0backend" && (if not exist venv python -m venv venv) && venv\Scripts\activate && pip install -r requirements.txt && python start_dev.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo Starting frontend...
start "Climate Tracker - Frontend" cmd /k "cd /d "%~dp0frontend" && npm install && npm run dev"

echo.
echo ✅ Both services are starting!
echo 🌐 Frontend: http://localhost:3000
echo 🌐 Backend: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo The applications will open in separate windows.
echo Close those windows to stop the services.
goto end

:start_frontend
echo.
echo 🚀 Starting Frontend only...
cd /d "%~dp0frontend"
echo Installing dependencies...
call npm install
echo Starting development server...
call npm run dev
goto end

:start_backend
echo.
echo 🚀 Starting Backend only...
cd /d "%~dp0backend"
echo Creating virtual environment...
if not exist "venv" python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo Starting development server...
python start_dev.py
goto end

:end
echo.
echo 🎉 Climate Tracker startup complete!
echo.
pause
