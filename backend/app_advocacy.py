"""
Minimal FastAPI app for Advocacy features only
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import only advocacy router
from api.advocacy import router as advocacy_router

# Create FastAPI app
app = FastAPI(
    title="Climate Tracker Advocacy API",
    description="Advocacy and Policy features",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register advocacy router
app.include_router(advocacy_router, tags=["Advocacy"])

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "Climate Tracker Advocacy API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "advocacy": "/api/v1/advocacy"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "climate-tracker-advocacy-api",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Advocacy API on http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    uvicorn.run(
        "app_advocacy:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
