"""
FastAPI Climate Tracker Application
Main entry point with API Gateway pattern
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
from datetime import datetime

# Load environment configuration
import env_config

# Import routers
from api.climate import router as climate_router
from api.carbon import router as carbon_router
from api.auth import router as auth_router
from api.social import router as social_router
from api.ml import router as ml_router
from api.upload import router as upload_router

# Import database
from database.connection import init_db, close_db
from core.config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Climate Tracker API")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down Climate Tracker API")
    await close_db()

# Create FastAPI app with API Gateway pattern
app = FastAPI(
    title="Climate Tracker API",
    description="Comprehensive climate monitoring and social platform API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# API Gateway - Register all routers
app.include_router(
    climate_router,
    prefix="/api/v1/climate",
    tags=["Climate Data"]
)

app.include_router(
    carbon_router,
    prefix="/api/v1/carbon",
    tags=["Carbon Footprint"]
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    social_router,
    prefix="/api/v1/social",
    tags=["Social Features"]
)

app.include_router(
    ml_router,
    prefix="/api/v1/ml",
    tags=["Machine Learning"]
)

app.include_router(
    upload_router,
    prefix="/api/v1/upload",
    tags=["File Upload"]
)

@app.get("/")
async def root():
    """API Gateway root endpoint"""
    return {
        "service": "Climate Tracker API Gateway",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "climate": "/api/v1/climate",
            "carbon": "/api/v1/carbon",
            "auth": "/api/v1/auth",
            "social": "/api/v1/social",
            "ml": "/api/v1/ml",
            "upload": "/api/v1/upload"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "climate-tracker-api-gateway",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return HTTPException(
        status_code=404,
        detail={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/docs",
                "/api/v1/climate",
                "/api/v1/carbon",
                "/api/v1/auth",
                "/api/v1/social",
                "/api/v1/ml",
                "/api/v1/upload"
            ]
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None  # Use structlog instead
    )
