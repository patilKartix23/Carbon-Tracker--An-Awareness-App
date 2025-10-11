# 🚀 Climate Tracker - Quick Setup Guide

This guide will help you get the Climate Tracker application running quickly on your local machine.

## 📋 Prerequisites

- **Python 3.12+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (to clone the repository)

*Note: You don't need PostgreSQL, MongoDB, or Redis for development - the app uses SQLite and mock services.*

## 🏃‍♂️ Quick Start (2 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python start_dev.py
```

The backend will start at `http://localhost:8000`

### 2. Frontend Setup (in a new terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the frontend server
npm start
# or
npm run dev
```

The frontend will start at `http://localhost:3000`

## 🎉 You're Done!

Open your browser and go to:
- **Frontend**: `http://localhost:3000` - Main application
- **Backend API**: `http://localhost:8000/docs` - Interactive API documentation

## 🌟 What You'll See

### Frontend Features:
- **Beautiful Dashboard**: Real-time climate widgets (using mock data)
- **Modern UI**: Responsive design with Tailwind CSS
- **Navigation**: Professional navbar and routing
- **Authentication**: Login/register pages (mock authentication)
- **Coming Soon Pages**: Carbon tracker, climate map, social feed, profile

### Backend Features:
- **FastAPI Server**: Modern async Python API
- **Interactive Docs**: Full API documentation at `/docs`
- **Mock Data**: Realistic sample data for all endpoints
- **Database**: SQLite database (created automatically)
- **Authentication**: JWT-based auth system

## 🔧 Development Features

### Backend (`http://localhost:8000`)
- Auto-reload when you change Python files
- Comprehensive error handling
- Mock data for external APIs (NASA, OpenWeather, etc.)
- SQLite database (no setup required)

### Frontend (`http://localhost:3000`)
- Hot reload when you change React files
- TypeScript support with strict typing
- Tailwind CSS for styling
- Mock authentication (no backend required)

## 📱 Test the Application

### Try These Features:

1. **Dashboard**: View the main climate dashboard with widgets
2. **Navigation**: Click through different pages (Carbon, Map, Social, Profile)
3. **API Documentation**: Visit `http://localhost:8000/docs` to explore all endpoints
4. **Authentication**: Try the login/register pages (they use mock data)

### Test API Endpoints:

```bash
# Get climate data
curl "http://localhost:8000/api/v1/climate/data?lat=40.7128&lon=-74.0060"

# Get air quality
curl "http://localhost:8000/api/v1/climate/air-quality?lat=40.7128&lon=-74.0060"

# Calculate carbon footprint
curl -X POST "http://localhost:8000/api/v1/carbon/simple" \
  -H "Content-Type: application/json" \
  -d '{"car_miles": 25, "electricity_kwh": 30}'
```

## 🛠️ Troubleshooting

### Common Issues:

**Backend won't start:**
```bash
# Make sure you're in the backend directory and virtual environment is activated
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python start_dev.py
```

**Frontend won't start:**
```bash
# Make sure you're in the frontend directory
cd frontend
npm install
npm start
```

**Port already in use:**
- Backend: Change port in `backend/start_dev.py` (default: 8000)
- Frontend: Change port in `frontend/vite.config.ts` (default: 3000)

### Need Help?

1. Check the terminal output for error messages
2. Make sure you're in the correct directory
3. Ensure Python 3.12+ and Node.js 18+ are installed
4. Try deleting `node_modules` and running `npm install` again

## 🚀 Next Steps

Once you have the basic app running:

1. **Add Real APIs**: Get API keys for NASA, OpenWeatherMap, etc.
2. **Set up Production Database**: Configure PostgreSQL and MongoDB
3. **Deploy**: Use the deployment guides in the main README
4. **Customize**: Modify the code to add your own features

## 📚 Project Structure

```
climate-tracker-app/
├── backend/              # FastAPI backend
│   ├── main.py          # Main FastAPI app
│   ├── start_dev.py     # Development startup script
│   ├── api/             # API routes
│   ├── database/        # Database models
│   └── services/        # Business logic
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── package.json    # Dependencies
│   └── vite.config.ts  # Vite configuration
└── README.md           # Full documentation
```

---

**🎯 Goal**: Get you up and running in under 2 minutes!

If you encounter any issues, check the main README.md for detailed documentation.
