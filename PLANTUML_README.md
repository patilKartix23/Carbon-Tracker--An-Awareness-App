# Climate Tracker - PlantUML Architecture Documentation

This directory contains comprehensive PlantUML diagrams documenting the Climate Tracker application architecture from multiple perspectives.

## 📊 Available Diagrams

### 1. **ARCHITECTURE_DIAGRAM.puml** - System Architecture
**Component Diagram** showing the complete system structure:
- Frontend Layer (React + TypeScript)
- Backend Layer (FastAPI)
- API Routes and Services
- Database and Storage
- External API Integrations
- Data flow between components

**Key Features:**
- Visual representation of all major components
- API Gateway pattern implementation
- Service layer architecture
- External dependencies (NASA, NOAA, OpenWeatherMap, Gemini AI)

---

### 2. **SEQUENCE_DIAGRAM.puml** - Carbon Tracking Flow
**Sequence Diagram** illustrating the carbon tracking process:
- User interaction flow
- API request/response cycle
- Service layer processing
- Database operations
- Results presentation

**Demonstrates:**
- How users submit carbon activities
- Emission calculation process
- Data persistence workflow
- Historical data retrieval

---

### 3. **USECASE_DIAGRAM.puml** - System Use Cases
**Use Case Diagram** documenting all system functionalities:
- Authentication & Profile Management
- Carbon Tracking & Monitoring
- Climate Data Visualization
- Social Platform Features
- CCUS Education
- EcoMarket Shopping
- Advocacy & Petitions
- AI Chatbot Assistance

**Shows:**
- User roles (User, Admin, Activist)
- System capabilities
- External system interactions
- Use case relationships (extends, includes)

---

### 4. **DATAFLOW_DIAGRAM.puml** - Data Flow
**Data Flow Diagram (DFD)** at two levels:
- **Level 0**: Context diagram showing system boundaries
- **Level 1**: Detailed process breakdown

**Illustrates:**
- How data moves through the system
- Data stores (databases, JSON files)
- External data sources
- Process interactions
- Information transformation

---

### 5. **CLASS_DIAGRAM.puml** - Domain Model
**Class Diagram** showing core business entities:
- User Management (User, UserProfile)
- Carbon Management (CarbonActivity, CarbonCalculator, CarbonGoal)
- Climate Monitoring (ClimateData, AirQuality, DataIntegrator)
- Social Platform (SocialPost, Comment, Like)
- Advocacy System (Petition, ImpactStory)
- EcoMarket (Product, Order)
- CCUS Education (CCUSSimulation, CCUSResource)
- AI Services (ClimateBot, MLService)

**Details:**
- Class attributes and methods
- Relationships and cardinality
- Domain model structure

---

### 6. **DEPLOYMENT_DIAGRAM.puml** - Infrastructure
**Deployment Diagram** showing technical infrastructure:
- Client layer (Browser, React App)
- Web server (Nginx/Apache)
- Application server (Uvicorn/FastAPI)
- Database layer (PostgreSQL/SQLite)
- File storage (JSON files, Cloud storage)
- External services
- Monitoring and logging

**Deployment Options:**
- Development setup
- Production configuration
- Docker containerization

---

## 🛠 How to View These Diagrams

### Option 1: Online PlantUML Editor
1. Visit [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)
2. Copy the content of any `.puml` file
3. Paste into the editor
4. View the generated diagram

### Option 2: VS Code Extension
1. Install "PlantUML" extension in VS Code
2. Open any `.puml` file
3. Press `Alt + D` to preview

### Option 3: Local PlantUML Installation
```bash
# Install PlantUML (requires Java)
# Windows (with Chocolatey)
choco install plantuml

# macOS (with Homebrew)
brew install plantuml

# Generate PNG images
plantuml ARCHITECTURE_DIAGRAM.puml
plantuml SEQUENCE_DIAGRAM.puml
plantuml USECASE_DIAGRAM.puml
plantuml DATAFLOW_DIAGRAM.puml
plantuml CLASS_DIAGRAM.puml
plantuml DEPLOYMENT_DIAGRAM.puml
```

### Option 4: IntelliJ IDEA / PyCharm
1. Install "PlantUML integration" plugin
2. Right-click on `.puml` file
3. Select "Show PlantUML Diagram"

---

## 📋 Diagram Selection Guide

**For understanding overall system structure:**
→ Start with `ARCHITECTURE_DIAGRAM.puml`

**For understanding user interactions:**
→ View `USECASE_DIAGRAM.puml`

**For understanding specific workflows:**
→ Check `SEQUENCE_DIAGRAM.puml`

**For understanding data movement:**
→ Explore `DATAFLOW_DIAGRAM.puml`

**For understanding domain model:**
→ Study `CLASS_DIAGRAM.puml`

**For understanding deployment:**
→ Review `DEPLOYMENT_DIAGRAM.puml`

---

## 🎯 Architecture Highlights

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Routing**: React Router for SPA navigation
- **Styling**: Tailwind CSS for modern UI
- **State**: Context API for global state
- **Build**: Vite for fast development

### Backend Architecture
- **Framework**: FastAPI (Python)
- **Pattern**: API Gateway with modular routers
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic schemas
- **Logging**: Structured logging with structlog

### Data Architecture
- **Primary DB**: PostgreSQL (production)
- **Fallback**: SQLite (development)
- **Quick Start**: JSON files (no DB setup)
- **File Storage**: Local + optional cloud

### External Integrations
- **NASA POWER API**: Satellite climate data
- **NOAA**: Atmospheric data
- **OpenWeatherMap**: Weather & air quality
- **Google Gemini AI**: Chatbot & ML insights

---

## 🔄 System Workflow Summary

1. **User Authentication**
   - Register/Login through Auth API
   - JWT token-based authentication
   - Profile management

2. **Carbon Tracking**
   - User submits activities
   - Backend calculates emissions
   - Stores in database
   - Returns insights & recommendations

3. **Climate Monitoring**
   - Fetches real-time data from external APIs
   - Aggregates multiple sources
   - Displays on interactive maps
   - Location-based alerts

4. **Social Features**
   - Users create environmental posts
   - GPS-verified activities
   - Community engagement (likes, comments)
   - Impact sharing

5. **AI Assistance**
   - Natural language queries
   - Personalized recommendations
   - Climate education
   - Data-driven insights

---

## 📊 Technology Stack

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- React Router
- Axios
- Vite

### Backend
- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy
- Structlog

### Database
- PostgreSQL (production)
- SQLite (development)
- JSON files (quick start)

### External Services
- NASA POWER API
- NOAA Climate API
- OpenWeatherMap API
- Google Gemini AI

---

## 🎓 Learning Resources

- [PlantUML Official Documentation](https://plantuml.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [System Architecture Patterns](https://docs.microsoft.com/en-us/azure/architecture/)

---

## 📝 Notes

- These diagrams represent the **current implementation** (v2.0.0)
- Some features use JSON files for quick start (no database setup required)
- Production deployment should use PostgreSQL
- External API keys required for full functionality
- Multi-language support: English, Hindi, Kannada, Tamil, Telugu

---

## 🔮 Future Architecture Enhancements

- Microservices architecture for scalability
- Redis caching layer
- Message queue (RabbitMQ/Kafka)
- GraphQL API option
- Mobile apps (React Native)
- Real-time WebSocket features
- Enhanced ML models
- IoT device integration

---

**Last Updated**: November 2024  
**Version**: 2.0.0  
**Maintained by**: Climate Tracker Development Team
