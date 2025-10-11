# Development Guide

## Quick Start

### Method 1: Use the Startup Script (Recommended)
```bash
cd climate-tracker-app
./start.sh
```

### Method 2: Manual Setup

#### Backend (Terminal 1)
```bash
cd backend
pip3 install flask flask-cors requests pandas numpy python-dotenv
python3 app.py
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

## Application URLs
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## Key Features to Test

### 1. Dashboard Overview
- Visit http://localhost:3000
- Should automatically get your location (or default to NYC)
- View weather widget, air quality, and map

### 2. Carbon Footprint Calculator
- Enter transportation data (car miles, bus miles, etc.)
- Enter energy usage (electricity, natural gas)
- Enter food consumption (beef, chicken, vegetables)
- Click "Calculate Footprint"
- View results and recommendations

### 3. Interactive Map
- Click anywhere on the map to change location
- Search for cities like "london", "tokyo", "paris"
- Weather and air quality widgets update automatically

### 4. Air Quality Monitoring
- Real-time AQI display with health recommendations
- Detailed pollutant breakdown (PM2.5, PM10, NO2, etc.)

## API Testing

### Test Climate Data
```bash
curl "http://localhost:5000/api/climate-data?lat=40.7128&lon=-74.0060&days=7"
```

### Test Carbon Footprint
```bash
curl -X POST "http://localhost:5000/api/carbon-footprint" \
  -H "Content-Type: application/json" \
  -d '{
    "transportation": {"car_gasoline": 25.5},
    "energy": {"electricity_grid": 30.2},
    "consumption": {"beef": 0.2, "vegetables": 1.5}
  }'
```

### Test Air Quality
```bash
curl "http://localhost:5000/api/air-quality?lat=40.7128&lon=-74.0060"
```

## Development Tips

### Backend Development
- The app uses mock data by default - no API keys required
- Add real API keys to `backend/.env` for live data
- Flask auto-reloads on code changes in debug mode
- Check `backend/services/` for business logic

### Frontend Development
- React auto-reloads on code changes
- Components are in `frontend/src/components/`
- Styles are in `frontend/src/components/Dashboard.css`
- Uses TypeScript for type safety

### Adding New Features

#### Backend (Python/Flask)
1. Add new routes in `backend/api/climate_routes.py`
2. Add business logic in `backend/services/`
3. Update API documentation in README.md

#### Frontend (React/TypeScript)
1. Create new components in `frontend/src/components/`
2. Add to Dashboard.tsx for main integration
3. Update Dashboard.css for styling

## Troubleshooting

### Backend Issues
- **Port 5000 busy**: Change PORT in `backend/.env`
- **Import errors**: Run `pip3 install -r requirements.txt`
- **CORS errors**: Check flask-cors installation

### Frontend Issues
- **Port 3000 busy**: React will suggest port 3001
- **API connection failed**: Ensure backend is running on port 5000
- **Module not found**: Run `npm install`

### Common Issues
- **Geolocation blocked**: Manually enter coordinates or use city search
- **Map not loading**: Check internet connection for tile loading
- **API timeouts**: Using mock data, no external dependencies required

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
FLASK_DEBUG=True
PORT=5000

# Optional - for real data
NASA_API_KEY=your-nasa-key
OPENWEATHER_API_KEY=your-openweather-key
NOAA_API_KEY=your-noaa-key
```

### Frontend
- Automatically proxies to backend via package.json
- No additional configuration needed for development

## Production Deployment

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app:app
```

### Frontend
```bash
cd frontend
npm run build
# Deploy 'build' folder to static hosting
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Architecture Overview

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   React Client  │ ──────────────→ │   Flask API      │
│   (Port 3000)   │ ←────────────── │   (Port 5000)    │
└─────────────────┘                 └──────────────────┘
         │                                   │
         │                                   │
    ┌────▼────┐                         ┌────▼────┐
    │ Leaflet │                         │External │
    │   Map   │                         │   APIs  │
    └─────────┘                         └─────────┘
```

## Next Steps for Development

1. **User Authentication**: Add login/signup functionality
2. **Data Persistence**: Connect to PostgreSQL database  
3. **Advanced Analytics**: Add trend analysis and predictions
4. **Mobile App**: React Native version
5. **Real-time Updates**: WebSocket integration
6. **IoT Integration**: Connect to environmental sensors
