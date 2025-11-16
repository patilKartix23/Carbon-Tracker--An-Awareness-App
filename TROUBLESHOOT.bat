@echo off
title Climate Tracker - Troubleshooting
color 0E

echo.
echo ========================================
echo   🔧 Climate Tracker - Troubleshooting
echo ========================================
echo.

echo Checking system and application status...
echo.

:: Check current directory
echo 📁 Current Directory: %CD%
if not exist "backend" (
    echo ❌ Backend directory not found
) else (
    echo ✅ Backend directory found
)

if not exist "frontend" (
    echo ❌ Frontend directory not found  
) else (
    echo ✅ Frontend directory found
)
echo.

:: Check ports
echo 🌐 Checking port usage...
netstat -ano | findstr :3000 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 3000 is available
) else (
    echo ⚠️  Port 3000 is in use
    echo    PIDs using port 3000:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do echo    %%a
)

netstat -ano | findstr :3001 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 3001 is available
) else (
    echo ⚠️  Port 3001 is in use
)

netstat -ano | findstr :8000 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 8000 is available
) else (
    echo ⚠️  Port 8000 is in use
    echo    PIDs using port 8000:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do echo    %%a
)
echo.

:: Check Python
echo 🐍 Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found or not in PATH
    echo    Please install Python 3.8+ from https://python.org
) else (
    echo ✅ Python found:
    python --version
)
echo.

:: Check Node.js
echo 📦 Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found or not in PATH
    echo    Please install Node.js 16+ from https://nodejs.org
) else (
    echo ✅ Node.js found:
    node --version
    echo ✅ NPM version:
    npm --version
)
echo.

:: Check dependencies
if exist "frontend\package.json" (
    echo 📦 Checking frontend dependencies...
    cd frontend
    if exist "node_modules" (
        echo ✅ Frontend node_modules exists
        npm list concurrently >nul 2>&1
        if errorlevel 1 (
            echo ⚠️  Concurrently not installed - this may cause issues
            echo    Run: npm install concurrently --save-dev
        ) else (
            echo ✅ Concurrently is installed
        )
    ) else (
        echo ⚠️  Frontend node_modules missing
        echo    Run: npm install
    )
    cd ..
)

if exist "backend\requirements.txt" (
    echo 🐍 Checking backend dependencies...
    if exist "backend\venv" (
        echo ✅ Backend virtual environment exists
    ) else (
        echo ⚠️  Backend virtual environment missing
        echo    It will be created automatically when you start the backend
    )
)
echo.

:: Quick fixes
echo 🔧 Quick Fix Options:
echo.
echo 1. Kill processes on ports 3000/8000
echo 2. Clean install frontend dependencies
echo 3. Clean install backend dependencies
echo 4. Show detailed port information
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto kill_ports
if "%choice%"=="2" goto clean_frontend
if "%choice%"=="3" goto clean_backend
if "%choice%"=="4" goto show_ports
goto end

:kill_ports
echo.
echo 🔪 Killing processes on ports 3000 and 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1
echo ✅ Processes killed (if any were running)
goto end

:clean_frontend
echo.
echo 🧹 Cleaning frontend...
if exist "frontend\node_modules" rmdir /s /q "frontend\node_modules"
cd frontend
call npm install
echo ✅ Frontend dependencies reinstalled
cd ..
goto end

:clean_backend
echo.
echo 🧹 Cleaning backend...
if exist "backend\venv" rmdir /s /q "backend\venv"
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Backend dependencies reinstalled
cd ..
goto end

:show_ports
echo.
echo 🌐 Detailed port information:
echo.
echo Processes using port 3000:
netstat -ano | findstr :3000
echo.
echo Processes using port 8000:
netstat -ano | findstr :8000
echo.
goto end

:end
echo.
echo 🎉 Troubleshooting complete!
echo.
pause
