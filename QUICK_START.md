# 🚀 Climate Tracker - Quick Start Guide

## 🎯 One-Click Launch (Recommended)

**Just double-click this file:**
```
🌍 Start Climate Tracker.bat
```

This will:
- ✅ Start both backend and frontend automatically
- ✅ Install all dependencies
- ✅ Open your browser to http://localhost:3000
- ✅ Show you the beautiful Climate Tracker dashboard

## 🛠️ Alternative Launch Methods

### Method 1: Interactive Menu
```bash
start-app.bat
```
Choose what to start (frontend only, backend only, or both)

### Method 2: PowerShell (Advanced)
```powershell
# Start both services
.\start-climate-app.ps1

# Start only frontend
.\start-climate-app.ps1 -Frontend

# Start only backend  
.\start-climate-app.ps1 -Backend

# Clean install and start
.\start-climate-app.ps1 -Clean
```

### Method 3: Manual (For Developers)
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python start_dev.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## 🌐 Access Your Application

Once started, you can access:

- **🌍 Main App**: http://localhost:3000
- **📖 API Docs**: http://localhost:8000/docs
- **⚡ API Endpoint**: http://localhost:8000

## ✨ What You'll See

### Frontend (http://localhost:3000)
- 🌡️ **Weather Dashboard**: Real-time weather widgets
- 🌬️ **Air Quality Monitor**: AQI tracking with recommendations
- 📊 **Carbon Footprint**: Daily emissions tracking
- 🚀 **Quick Actions**: Easy navigation to all features
- 📱 **Activity Feed**: Recent climate activities
- 🎨 **Beautiful UI**: Modern, responsive design

### Backend (http://localhost:8000/docs)
- 🔧 **Interactive API**: Test all endpoints
- 🌍 **Climate Data**: Weather, AQI, forecasting
- 👤 **User Management**: Authentication and profiles
- 📊 **Carbon Calculator**: Emissions calculation
- 🤖 **AI Features**: ML predictions and image analysis
- 📱 **Social Features**: Posts, likes, comments

## 🔧 Troubleshooting

### ❌ "Nothing shows up in browser"

**Solution 1: Wait and refresh**
- Wait 30 seconds for services to start
- Refresh your browser (F5)
- Check if both backend and frontend windows are running

**Solution 2: Check ports**
```bash
# Kill any processes on ports 3000 and 8000
taskkill /f /im node.exe
taskkill /f /im python.exe
```

**Solution 3: Manual restart**
- Close all command windows
- Run `🌍 Start Climate Tracker.bat` again

### ❌ "Module not found" errors

**Solution: Clean install**
```bash
# Delete node_modules and venv, then reinstall
start-app.bat
# Choose option 4 (Clean install)
```

### ❌ "Port already in use"

**Solution: Kill processes**
```bash
netstat -ano | findstr :3000
netstat -ano | findstr :8000
# Note the PID numbers and kill them:
taskkill /f /pid [PID_NUMBER]
```

### ❌ Python/Node.js not found

**Install required software:**
- **Python 3.12+**: https://python.org/downloads
- **Node.js 18+**: https://nodejs.org/download

### ❌ PowerShell execution policy error

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🎯 Quick Test

After starting, test these URLs:

1. **Frontend**: http://localhost:3000 - Should show dashboard
2. **Backend Health**: http://localhost:8000/health - Should return JSON
3. **API Docs**: http://localhost:8000/docs - Should show interactive docs

## 📱 Features to Try

1. **Dashboard**: View climate widgets and data
2. **Navigation**: Click through different pages
3. **API Testing**: Go to `/docs` and try the endpoints
4. **Weather Data**: Test climate endpoints with coordinates
5. **Carbon Calculator**: Try the carbon footprint calculator

## 🆘 Still Having Issues?

1. **Check Prerequisites**:
   - Python 3.12+ installed
   - Node.js 18+ installed
   - Internet connection for dependencies

2. **Restart Everything**:
   - Close all command windows
   - Restart your computer
   - Run `🌍 Start Climate Tracker.bat`

3. **Manual Debugging**:
   ```bash
   # Check Python
   python --version
   
   # Check Node.js
   node --version
   
   # Check npm
   npm --version
   ```

## 🎉 Success!

If you see the Climate Tracker dashboard at http://localhost:3000, you're all set!

The app includes:
- ✅ Beautiful modern UI
- ✅ Real-time climate data (mock data for demo)
- ✅ Interactive API documentation
- ✅ Carbon footprint tracking
- ✅ Weather and air quality monitoring
- ✅ Social features (coming soon pages)

---

**🌍 Welcome to Climate Tracker - Your journey to sustainability starts here!**
