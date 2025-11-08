"""
Start Advocacy API with SQLite (no PostgreSQL required)
"""
import os
import sys

# Force SQLite by unsetting PostgreSQL host
os.environ['POSTGRES_HOST'] = ''
os.environ['ENVIRONMENT'] = 'development'

# Now import and run the app
if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Starting Climate Tracker Advocacy API")
    print("=" * 60)
    print("Database: SQLite (./climate_tracker.db)")
    print("API Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app_advocacy:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
