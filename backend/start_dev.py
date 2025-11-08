#!/usr/bin/env python3
"""
Development startup script for Climate Tracker Backend
This script starts the FastAPI server with mock data when external services are not available.
"""

import uvicorn
import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        # Try to set UTF-8 encoding
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        # If that fails, we'll use ASCII-safe output
        pass

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def safe_print(text):
    """Print text with fallback for encoding errors"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove emojis and special characters
        ascii_text = text.encode('ascii', 'ignore').decode('ascii')
        print(ascii_text)

def main():
    safe_print("Starting Climate Tracker Backend (Development Mode)")
    safe_print("=" * 50)
    
    # Set development environment variables if not already set
    if not os.getenv('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing-only'
    
    if not os.getenv('DEBUG'):
        os.environ['DEBUG'] = 'True'
    
    if not os.getenv('ENVIRONMENT'):
        os.environ['ENVIRONMENT'] = 'development'
    
    safe_print("[OK] Environment configured for development")
    safe_print("[API] Will be available at: http://localhost:8000")
    safe_print("[DOCS] API docs at: http://localhost:8000/docs")
    safe_print("[MOCK] Using mock data for external APIs (NASA, OpenWeather, etc.)")
    safe_print("[DB] Database: Using SQLite for development (no PostgreSQL/MongoDB required)")
    safe_print("")
    safe_print("To stop the server, press Ctrl+C")
    safe_print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        safe_print("\n[STOP] Server stopped by user")
    except Exception as e:
        safe_print(f"[ERROR] Error starting server: {e}")
        safe_print("[TIP] Make sure you have installed requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
