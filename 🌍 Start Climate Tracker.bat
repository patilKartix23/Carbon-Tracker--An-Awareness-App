@echo off
title Climate Tracker - One-Click Launcher
color 0A
chcp 65001 >nul 2>&1

:: Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ========================================
echo      🌍 Climate Tracker - Quick Start
echo ========================================
echo.

:: Verify directories exist
if not exist "backend" (
    echo ❌ Error: backend directory not found
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Error: frontend directory not found
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

:: Start both services automatically
echo 🚀 Starting Climate Tracker Application...
echo.
echo This will start both:
echo - Backend API (FastAPI) on port 8000
echo - Frontend Web App (React) on port 3000
echo.

:: Start backend
echo Starting backend...
start "Climate Tracker Backend" cmd /k "cd /d "%~dp0backend" && (if not exist venv python -m venv venv) && venv\Scripts\activate && pip install -r requirements.txt >nul 2>&1 && echo ✅ Backend ready at http://localhost:8000 && echo 📖 API docs at http://localhost:8000/docs && python start_dev.py"

:: Wait a moment for backend
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start frontend
echo Starting frontend...
start "Climate Tracker Frontend" cmd /k "cd /d "%~dp0frontend" && npm install >nul 2>&1 && echo ✅ Frontend starting (will auto-detect port) && npm run dev"

:: Wait a moment
timeout /t 3 /nobreak > nul

echo.
echo ✅ Climate Tracker is starting!
echo.
echo 🌐 Frontend will open on available port:
echo    Check the Frontend terminal window for actual URL
echo    (Usually http://localhost:3000 or http://localhost:3001)
echo.
echo 📖 API Documentation:
echo    http://localhost:8000/docs
echo.
echo 🏥 Backend Health Check:
echo    http://localhost:8000/health
echo.
echo 💡 Tip: Keep the backend and frontend windows open
echo    Close them when you want to stop the application
echo.

:: Try to open browser automatically - start with backend docs
echo Opening API documentation...
timeout /t 2 /nobreak > nul
start http://localhost:8000/docs

echo.
echo 🎉 Climate Tracker is now running!
echo    Check your browser at http://localhost:3000
echo.
pause
