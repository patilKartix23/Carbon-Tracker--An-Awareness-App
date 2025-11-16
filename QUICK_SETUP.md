# Climate Tracker - Quick Setup Guide

## Port Configuration ✅ FIXED
- **Frontend**: Runs on port 3000 (Vite dev server)
- **Backend**: Runs on port 8000 (FastAPI with Uvicorn)
- **API Proxy**: Vite automatically proxies `/api/*` requests to backend

## Quick Start

### Option 1: Use the Development Script (Recommended)
```bash
# Run both frontend and backend
./start-dev.bat
```

### Option 2: Manual Setup
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## Access Points
- 🌐 **Frontend App**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 🔍 **API Health Check**: http://localhost:8000/health

## Fixed Issues ✅

### 1. **API Endpoint Consistency**
- All frontend APIs now use `/api/v1/` prefix consistently
- Matches backend route structure exactly
- Centralized API client handles authentication and base URL

### 2. **CORS Configuration**
- Backend allows all necessary frontend ports (3000, 5173, etc.)
- Added HTTPS support for future deployment
- Proper development vs production configuration

### 3. **Database Configuration**  
- Uses SQLite by default for easy development
- No PostgreSQL setup required locally
- Configured to auto-create database file

### 4. **Environment Variables**
- Frontend `.env` file created for consistent configuration
- Backend uses sensible defaults for development
- Easy override for production deployment

### 5. **API Client Improvements**
- All APIs now use centralized `apiClient` with:
  - Automatic token management
  - Consistent error handling
  - Proper request/response interceptors
  - Mock data fallbacks for offline development

## API Structure

All API endpoints follow this pattern:
```
Frontend Request → http://localhost:3000/api/v1/[endpoint]
↓ (Vite Proxy)
Backend Handler → http://localhost:8000/api/v1/[endpoint]
```

### Available Endpoints:
- `/api/v1/auth/*` - Authentication
- `/api/v1/climate/*` - Weather & climate data
- `/api/v1/carbon/*` - Carbon footprint tracking
- `/api/v1/social/*` - Social features
- `/api/v1/advocacy/*` - Advocacy features
- `/api/v1/chatbot/*` - AI chatbot
- `/api/ccus/*` - Carbon capture features
- `/api/eco-shopping/*` - Sustainable shopping

## Development Notes

- **Mock Data**: Frontend APIs include fallback mock data for offline development
- **Hot Reload**: Both frontend and backend support live reloading
- **Error Handling**: Graceful fallbacks when backend is unavailable
- **Token Management**: Automatic JWT token refresh handling

## Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 3000 or 8000
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

### Backend Won't Start
- Check Python environment: `python --version` (3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check database: SQLite file will be created automatically

### Frontend Won't Start  
- Check Node.js: `node --version` (16+)
- Install dependencies: `npm install`
- Clear cache: `npm run build` then `npm run dev`

## Next Steps
1. Run `start-dev.bat` to launch both servers
2. Open http://localhost:3000 in your browser
3. Check backend health at http://localhost:8000/health
4. Explore API docs at http://localhost:8000/docs

All major endpoint and port issues have been resolved! 🎉
