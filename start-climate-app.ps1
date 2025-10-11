# Climate Tracker Application Startup Script
# This script starts both frontend and backend services

param(
    [switch]$Frontend,
    [switch]$Backend,
    [switch]$Both = $true,
    [switch]$Clean,
    [switch]$Help
)

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "🌍 Climate Tracker Application Startup Script" $Cyan
    Write-ColorOutput "=============================================" $Cyan
    Write-Host ""
    Write-ColorOutput "Usage:" $Yellow
    Write-Host "  .\start-climate-app.ps1 [options]"
    Write-Host ""
    Write-ColorOutput "Options:" $Yellow
    Write-Host "  -Frontend    Start only frontend (React)"
    Write-Host "  -Backend     Start only backend (FastAPI)"
    Write-Host "  -Both        Start both services (default)"
    Write-Host "  -Clean       Clean install (delete node_modules, venv)"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-ColorOutput "Examples:" $Yellow
    Write-Host "  .\start-climate-app.ps1              # Start both services"
    Write-Host "  .\start-climate-app.ps1 -Frontend    # Start only frontend"
    Write-Host "  .\start-climate-app.ps1 -Clean       # Clean install and start"
    exit
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Checking prerequisites..." $Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        Write-ColorOutput "✅ Python: $pythonVersion" $Green
    } catch {
        Write-ColorOutput "❌ Python not found. Please install Python 3.12+" $Red
        exit 1
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        Write-ColorOutput "✅ Node.js: $nodeVersion" $Green
    } catch {
        Write-ColorOutput "❌ Node.js not found. Please install Node.js 18+" $Red
        exit 1
    }
    
    # Check npm
    try {
        $npmVersion = npm --version 2>$null
        Write-ColorOutput "✅ npm: v$npmVersion" $Green
    } catch {
        Write-ColorOutput "❌ npm not found" $Red
        exit 1
    }
}

function Clean-Install {
    Write-ColorOutput "🧹 Performing clean install..." $Yellow
    
    # Clean frontend
    if (Test-Path "frontend/node_modules") {
        Write-ColorOutput "Removing frontend/node_modules..." $Yellow
        Remove-Item -Recurse -Force "frontend/node_modules"
    }
    
    # Clean backend
    if (Test-Path "backend/venv") {
        Write-ColorOutput "Removing backend/venv..." $Yellow
        Remove-Item -Recurse -Force "backend/venv"
    }
    
    Write-ColorOutput "✅ Clean completed" $Green
}

function Start-Backend {
    Write-ColorOutput "🚀 Starting Backend (FastAPI)..." $Cyan
    
    # Navigate to backend
    Set-Location "backend"
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path "venv")) {
        Write-ColorOutput "Creating Python virtual environment..." $Yellow
        python -m venv venv
    }
    
    # Activate virtual environment
    Write-ColorOutput "Activating virtual environment..." $Yellow
    & "venv\Scripts\Activate.ps1"
    
    # Install requirements
    Write-ColorOutput "Installing Python dependencies..." $Yellow
    pip install -r requirements.txt --quiet
    
    Write-ColorOutput "✅ Backend setup complete" $Green
    Write-ColorOutput "🌐 Backend will be available at: http://localhost:8000" $Green
    Write-ColorOutput "📖 API docs will be available at: http://localhost:8000/docs" $Green
    Write-Host ""
    
    # Start the server
    python start_dev.py
}

function Start-Frontend {
    Write-ColorOutput "🚀 Starting Frontend (React)..." $Cyan
    
    # Navigate to frontend
    Set-Location "frontend"
    
    # Install dependencies
    Write-ColorOutput "Installing Node.js dependencies..." $Yellow
    npm install --silent
    
    Write-ColorOutput "✅ Frontend setup complete" $Green
    Write-ColorOutput "🌐 Frontend will be available at: http://localhost:3000" $Green
    Write-Host ""
    
    # Start the server
    npm run dev
}

function Start-Both {
    Write-ColorOutput "🚀 Starting Both Services..." $Cyan
    Write-Host ""
    
    # Start backend in background
    Write-ColorOutput "Starting backend in background..." $Yellow
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location "backend"
        
        if (-not (Test-Path "venv")) {
            python -m venv venv
        }
        
        & "venv\Scripts\Activate.ps1"
        pip install -r requirements.txt --quiet
        python start_dev.py
    }
    
    # Wait a bit for backend to start
    Start-Sleep -Seconds 3
    
    # Start frontend in background
    Write-ColorOutput "Starting frontend in background..." $Yellow
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location "frontend"
        npm install --silent
        npm run dev
    }
    
    # Wait a bit more
    Start-Sleep -Seconds 5
    
    Write-ColorOutput "✅ Both services are starting..." $Green
    Write-ColorOutput "🌐 Frontend: http://localhost:3000" $Green
    Write-ColorOutput "🌐 Backend: http://localhost:8000" $Green
    Write-ColorOutput "📖 API Docs: http://localhost:8000/docs" $Green
    Write-Host ""
    Write-ColorOutput "Press Ctrl+C to stop both services" $Yellow
    
    # Wait for jobs and handle cleanup
    try {
        while ($true) {
            Start-Sleep -Seconds 1
            
            # Check if jobs are still running
            if ($backendJob.State -ne "Running" -and $frontendJob.State -ne "Running") {
                break
            }
        }
    } finally {
        Write-ColorOutput "🛑 Stopping services..." $Yellow
        Stop-Job $backendJob -ErrorAction SilentlyContinue
        Stop-Job $frontendJob -ErrorAction SilentlyContinue
        Remove-Job $backendJob -ErrorAction SilentlyContinue
        Remove-Job $frontendJob -ErrorAction SilentlyContinue
    }
}

# Main script logic
if ($Help) {
    Show-Help
}

Write-ColorOutput "🌍 Climate Tracker Application Startup" $Cyan
Write-ColorOutput "=====================================" $Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "frontend") -or -not (Test-Path "backend")) {
    Write-ColorOutput "❌ Error: Please run this script from the climate-tracker-app directory" $Red
    exit 1
}

Test-Prerequisites

if ($Clean) {
    Clean-Install
}

# Determine what to start
if ($Frontend) {
    Start-Frontend
} elseif ($Backend) {
    Start-Backend
} else {
    Start-Both
}
