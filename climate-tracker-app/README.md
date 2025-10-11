# 🌍 Climate Tracker Application v2.0

A comprehensive climate monitoring and carbon footprint tracking application that provides real-time climate data, AI-powered insights, and social features for environmental awareness and action.

## 🌟 Features

### Core Features
- **🌡️ Real-time Climate Data**: Integration with NASA, NOAA, OpenWeatherMap APIs
- **📊 Carbon Footprint Tracking**: Advanced calculator with personalized recommendations  
- **🗺️ Interactive Climate Map**: Global climate visualization with multiple data layers
- **📱 Social Features**: Photo sharing with AI analysis and community feed
- **🤖 AI/ML Integration**: Climate forecasting and image recognition
- **👥 User Profiles**: Authentication, progress tracking, and achievements

### Technical Architecture
- **Backend**: FastAPI with API Gateway pattern
- **Frontend**: React + TypeScript + Tailwind CSS
- **Databases**: PostgreSQL (relational) + MongoDB (documents)
- **Authentication**: JWT-based with refresh tokens
- **File Storage**: Cloudinary/AWS S3 integration
- **ML/AI**: scikit-learn models with SHAP interpretability
- **Real-time**: Background tasks with Celery + Redis

## 🏗️ Architecture Overview

```
┌───────────────────────────┐
│         Frontend           │
│  (React / React Native)    │
│ ─────────────────────────  │
│ - Weather & AQI Dashboard  │
│ - Carbon Footprint Tracker │
│ - Photo Upload (Instagram) │
│ - User Feed & Profiles     │
└───────────┬────────────────┘
            │
            ▼
 ┌───────────────────────────────┐
 │            Backend             │
 │ (FastAPI / Node.js + Express)  │
 │ ─────────────────────────────  │
 │ - API Gateway                  │
 │ - Weather API Fetcher          │
 │ - Carbon Footprint Calculator  │
 │ - ML Forecasts (scikit-learn)  │
 │ - Image Upload API             │
 │ - Authentication (JWT/Auth0)   │
 └───────────┬────────────────────┘
             │
┌───────────────────┼───────────────────────────┐
│                   │                           │
▼                   ▼                           ▼
┌──────────┐   ┌─────────────┐            ┌─────────────────┐
│ Database │   │   File/Img  │            │ External APIs    │
│ (Postgres│   │   Storage   │            │ (NASA, NOAA,     │
│  + Mongo)│   │(Cloudinary/ │            │  OpenWeather,    │
│──────────│   │ Firebase/S3)│            │  AirVisual)      │
│ - Users  │   │ - User Photos│            │ - Weather        │
│ - Carbon │   │ - Climate Img│            │ - AQI            │
│ - Posts  │   │ - Thumbnails │            │ - Satellite Data │
│ - Logs   │   │              │            │                  │
└──────────┘   └─────────────┘            └─────────────────┘
                     │
                     ▼
          ┌────────────────────────────┐
          │   AI/ML Layer (Optional)   │
          │ ─────────────────────────  │
          │ - Time Series Forecasting  │
          │ - Image Recognition (YOLO) │
          │   (detect trees, pollution │
          │    in photos)              │
          │ - Personalized Tips Engine │
          └────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+** (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL** (main database)
- **MongoDB** (document storage)
- **Redis** (caching & background tasks)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize databases**:
   ```bash
   # Make sure PostgreSQL and MongoDB are running
   # Tables will be created automatically on first run
   ```

6. **Start the FastAPI server**:
   ```bash
   python main.py
   # Or use uvicorn: uvicorn main:app --reload --port 8000
   ```

   Backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## 🔑 Environment Configuration

### Backend (.env)
```env
# Application
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=climate_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=climate_tracker_docs

REDIS_URL=redis://localhost:6379/0

# External APIs
OPENWEATHER_API_KEY=your_openweather_key
NASA_API_KEY=optional
NOAA_API_KEY=optional

# File Storage
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ML Features
ENABLE_ML_FEATURES=True
```

## 📱 API Documentation

Once the backend is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Climate Data
```http
GET /api/v1/climate/data?lat=40.7128&lon=-74.0060&days=7
GET /api/v1/climate/air-quality?lat=40.7128&lon=-74.0060
GET /api/v1/climate/weather-forecast?lat=40.7128&lon=-74.0060
GET /api/v1/climate/alerts?lat=40.7128&lon=-74.0060
```

#### Carbon Footprint
```http
POST /api/v1/carbon/calculate
POST /api/v1/carbon/simple
GET /api/v1/carbon/history
GET /api/v1/carbon/stats
```

#### Social Features
```http
GET /api/v1/social/posts
POST /api/v1/social/posts
POST /api/v1/social/posts/{id}/like
POST /api/v1/social/posts/{id}/comments
```

#### Authentication
```http
POST /api/v1/auth/register
POST /api/v1/auth/token
GET /api/v1/auth/me
```

#### ML & AI
```http
POST /api/v1/ml/forecast
POST /api/v1/ml/analyze-image
GET /api/v1/ml/recommendations
```

## 🛠️ Development

### Project Structure
```
climate-tracker-app/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   │   ├── auth.py        # Authentication
│   │   ├── carbon.py      # Carbon footprint
│   │   ├── climate.py     # Climate data
│   │   ├── ml.py          # Machine learning
│   │   ├── social.py      # Social features
│   │   └── upload.py      # File uploads
│   ├── core/              # Core configuration
│   ├── database/          # Database models & connection
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── main.py           # FastAPI app
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── contexts/     # React contexts
│   │   ├── hooks/        # Custom hooks
│   │   ├── types/        # TypeScript types
│   │   ├── api/          # API client
│   │   └── utils/        # Utilities
│   └── package.json
└── README.md
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
black . && isort . && flake8

# Frontend linting
cd frontend
npm run lint
```

## 🌐 Deployment

### Backend Deployment (Railway/Render/DigitalOcean)
1. Set environment variables in your hosting platform
2. Deploy with: `python main.py` or `uvicorn main:app`

### Frontend Deployment (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy the `dist` folder
3. Configure API proxy to your backend

## 🔗 External API Integration

### Required APIs
- **OpenWeatherMap**: Weather & air quality data
  - Get API key: https://openweathermap.org/api
  - Free tier: 1000 calls/day

### Optional APIs
- **NASA POWER**: Satellite climate data
  - No API key required for basic usage
- **NOAA**: Climate and atmospheric data
  - Get token: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

## 🤖 AI/ML Features

### Climate Forecasting
- Time series prediction for temperature and AQI
- Random Forest models with feature importance
- SHAP values for model interpretability

### Image Analysis
- Environmental content detection
- Vegetation and pollution analysis
- Air quality assessment from photos

### Personalized Recommendations
- ML-powered carbon reduction tips
- Location-based suggestions
- Behavioral pattern analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript strict mode for frontend
- Write tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA POWER**: Satellite and meteorological data
- **OpenWeatherMap**: Weather and air quality data
- **NOAA**: Climate and atmospheric data
- **React Leaflet**: Interactive mapping functionality
- **Chart.js**: Data visualization components

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- ✅ FastAPI backend with API Gateway
- ✅ React frontend with modern UI
- ✅ Authentication system
- ✅ Database models (PostgreSQL + MongoDB)
- ✅ Basic API endpoints structure

### Phase 2 (Next) 🔄
- 🔄 Real API integrations (NASA, NOAA, OpenWeather)
- 🔄 Carbon footprint calculator implementation
- 🔄 File upload and image processing
- 🔄 ML models training and deployment
- 🔄 Interactive map with Leaflet

### Phase 3 (Future) 📋
- 📋 Mobile app (React Native)
- 📋 Real-time notifications
- 📋 Advanced AI features
- 📋 IoT sensor integration
- 📋 Corporate dashboard

---

**Built with ❤️ for a sustainable future**

For support, questions, or contributions, please open an issue or contact the development team.