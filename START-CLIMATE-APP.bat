@echo off
title Climate Tracker - Starting Servers...
echo.
echo ========================================
echo   Climate Tracker Application
echo ========================================
echo.
echo Starting Backend Server (Port 8000)...
echo.

:: Start Backend in a new window
start "Climate Tracker - Backend (Port 8000)" cmd /k "cd /d C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app\backend && set PORT=8000 && python app.py"

:: Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

echo Backend started!
echo.
echo Starting Frontend Server (Port 3000)...
echo.

:: Start Frontend in a new window
start "Climate Tracker - Frontend (Port 3000)" cmd /k "cd /d C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app\frontend && npm run dev"

:: Wait 5 seconds for frontend to start
timeout /t 5 /nobreak >nul

echo Frontend started!
echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul

:: Open the application in default browser
start http://localhost:3000

echo.
echo ========================================
echo   Climate Tracker is now running!
echo ========================================
echo.
echo To stop the servers:
echo - Close the Backend window (Port 8000)
echo - Close the Frontend window (Port 3000)
echo.
echo Press any key to close this window...
pause >nul
