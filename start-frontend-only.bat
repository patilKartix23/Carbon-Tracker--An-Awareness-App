@echo off
title Climate Tracker - Frontend Only
chcp 65001 >nul 2>&1

:: Get the directory where this script is located and navigate to frontend
cd /d "%~dp0frontend"

:: Check if frontend directory exists
if not exist "package.json" (
    echo ❌ Error: Cannot find frontend files
    echo Please run this script from the climate-tracker-app directory
    pause
    exit /b 1
)

echo ========================================
echo   Starting Climate Tracker Frontend
echo ========================================
echo.

:: Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ❌ Error: Failed to install dependencies
        echo Make sure Node.js and npm are installed
        pause
        exit /b 1
    )
)

echo Starting development server...
echo Frontend will be available at: http://localhost:3000
echo.

call npm run dev

pause
