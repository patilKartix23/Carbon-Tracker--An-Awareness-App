#!/usr/bin/env python3
"""
Development startup script for Climate Tracker Backend
This script starts the FastAPI server with mock data when external services are not available.
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    print("🌍 Starting Climate Tracker Backend (Development Mode)")
    print("=" * 50)
    
    # Set development environment variables if not already set
    if not os.getenv('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing-only'
    
    if not os.getenv('DEBUG'):
        os.environ['DEBUG'] = 'True'
    
    if not os.getenv('ENVIRONMENT'):
        os.environ['ENVIRONMENT'] = 'development'
    
    print("✅ Environment configured for development")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔧 Using mock data for external APIs (NASA, OpenWeather, etc.)")
    print("💾 Database: Using SQLite for development (no PostgreSQL/MongoDB required)")
    print("")
    print("To stop the server, press Ctrl+C")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure you have installed requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
