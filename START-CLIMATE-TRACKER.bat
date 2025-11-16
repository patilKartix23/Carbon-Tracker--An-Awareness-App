@echo off
title Climate Tracker - Smart Launcher
color 0A
chcp 65001 >nul 2>&1

:: Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ========================================
echo   🌍 Climate Tracker - Smart Launcher
echo ========================================
echo.

:: Check for required directories
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

:: Check if concurrently is installed
cd frontend
npm list concurrently >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing missing dependencies...
    call npm install concurrently --save-dev >nul 2>&1
    echo ✅ Dependencies installed
)
cd ..

echo 🚀 Starting Climate Tracker Application...
echo.
echo This will launch:
echo - Backend API (FastAPI) on port 8000
echo - Frontend Web App (Vite) on auto-detected port
echo.

:: Start backend first
echo [1/2] Starting backend server...
start "Climate Tracker - Backend API" cmd /k "cd /d "%~dp0backend" && echo 🚀 Starting Climate Tracker Backend... && python start_dev.py"

:: Wait for backend to initialize
echo [2/2] Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start frontend
echo [2/2] Starting frontend application...
start "Climate Tracker - Frontend" cmd /k "cd /d "%~dp0frontend" && echo 🌐 Starting Climate Tracker Frontend... && npm run dev"

:: Give both services time to start
timeout /t 3 /nobreak > nul

echo.
echo ✅ Climate Tracker is starting up!
echo.
echo 📊 Services Status:
echo   Backend API:  http://localhost:8000
echo   Frontend App: Check Frontend terminal for actual port
echo                (usually http://localhost:3000 or 3001)
echo.
echo 📚 Useful Links:
echo   API Documentation: http://localhost:8000/docs
echo   Health Check:      http://localhost:8000/health
echo   OpenAPI Spec:      http://localhost:8000/openapi.json
echo.
echo 💡 Pro Tips:
echo   - Vite automatically finds available ports if 3000 is busy
echo   - Both apps support hot-reload during development  
echo   - Close the terminal windows to stop the services
echo   - Backend includes mock data for offline development
echo.

:: Open helpful pages
echo 🌐 Opening useful pages...
timeout /t 2 /nobreak > nul
start http://localhost:8000/docs
timeout /t 1 /nobreak > nul
start http://localhost:8000/health

echo.
echo 🎉 Launch complete! Check the opened terminal windows.
echo.
echo Frontend will be available shortly at:
echo → Check the "Climate Tracker - Frontend" window for the exact URL
echo.
pause
