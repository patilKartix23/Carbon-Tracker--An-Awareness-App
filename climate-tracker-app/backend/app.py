from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api.climate_routes import climate_bp
from api.carbon_activity import carbon_activity_bp

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure CORS to allow requests from frontend
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Register blueprints
app.register_blueprint(climate_bp, url_prefix='/api')
app.register_blueprint(carbon_activity_bp, url_prefix='/api/carbon-activity')

@app.route('/')
def hello():
    """Root endpoint"""
    return jsonify({
        "message": "Climate Tracker API v1.0",
        "status": "running",
        "endpoints": {
            "climate_data": "/api/climate-data",
            "carbon_footprint": "/api/carbon-footprint",
            "simple_footprint": "/api/carbon-footprint/simple",
            "carbon_activity_calculate": "/api/carbon-activity/calculate",
            "carbon_activity_log": "/api/carbon-activity/log",
            "daily_summary": "/api/carbon-activity/daily-summary/<user_id>",
            "weekly_trends": "/api/carbon-activity/weekly-trends/<user_id>",
            "activities_list": "/api/carbon-activity/activities",
            "leaderboard": "/api/carbon-activity/leaderboard",
            "suggestions": "/api/carbon-activity/suggestions",
            "air_quality": "/api/air-quality",
            "weather_forecast": "/api/weather-forecast",
            "health": "/api/health"
        }
    })

@app.route('/health')
def health_check():
    """Main health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "climate-tracker-api",
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": [
            "/",
            "/health",
            "/api/climate-data",
            "/api/carbon-footprint",
            "/api/air-quality",
            "/api/weather-forecast"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"Starting Climate Tracker API on {host}:{port}")
    print(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(
        debug=app.config['DEBUG'],
        host=host,
        port=port
    )
