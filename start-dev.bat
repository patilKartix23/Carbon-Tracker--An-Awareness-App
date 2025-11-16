@echo off
title Climate Tracker - Quick Dev Start
color 0A
echo Starting Climate Tracker Development Environment...
echo.

:: Check for required directories
if not exist "backend" (
    echo ❌ Error: backend directory not found
    pause
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Error: frontend directory not found  
    pause
    exit /b 1
)

echo 🚀 Starting Backend (FastAPI on port 8000)...
cd backend
start "Climate Tracker - Backend" cmd /k "python start_dev.py"

echo.
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Starting Frontend (Vite - will auto-detect available port)...
cd ..\frontend
start "Climate Tracker - Frontend" cmd /k "npm run dev"

echo.
echo ✅ Both servers are starting!
echo.
echo 📱 Frontend: Will open on available port (usually 3000, 3001, etc.)
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
echo.
echo 💡 Tip: Vite will automatically find an available port if 3000 is busy
echo      Check the Frontend terminal window for the actual URL
echo.
echo Opening browser to backend docs...
timeout /t 2 /nobreak >nul
start http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
