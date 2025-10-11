from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api.climate_routes import climate_bp
from api.carbon_activity import carbon_activity_bp
from api.ccus import ccus_bp
from api.eco_shopping import eco_shopping_bp
from api.indian_climate import indian_climate_bp
from api.chatbot import chatbot_bp

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
app.register_blueprint(ccus_bp, url_prefix='/api/ccus')
app.register_blueprint(eco_shopping_bp, url_prefix='/api/eco-shopping')
app.register_blueprint(indian_climate_bp, url_prefix='/api/climate')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

@app.route('/')
def hello():
    """Root endpoint"""
    return jsonify({
        "message": "Climate Tracker API v2.0 with CCUS & Eco-Shopping",
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
            "health": "/api/health",
            # Indian Climate endpoints
            "india_overview": "/api/climate/india/overview",
            "india_cities": "/api/climate/india/cities",
            "india_city_detail": "/api/climate/india/city/<city_name>",
            "india_regions": "/api/climate/india/regions",
            "india_trends": "/api/climate/india/trends",
            "india_current": "/api/climate/india/current",
            # Chatbot endpoints
            "chatbot_chat": "/api/chatbot/chat",
            "chatbot_history": "/api/chatbot/chat/history/<user_id>",
            "chatbot_suggestions": "/api/chatbot/chat/suggestions",
            "chatbot_quick_response": "/api/chatbot/chat/quick-response",
            "chatbot_info": "/api/chatbot/chat/bot-info",
            # CCUS endpoints
            "ccus_capture_simulation": "/api/ccus/capture-simulation",
            "ccus_storage_sites": "/api/ccus/storage-sites",
            "ccus_utilization_pathways": "/api/ccus/utilization-pathways",
            "ccus_carbon_credits": "/api/ccus/carbon-credits",
            "ccus_comprehensive_analysis": "/api/ccus/comprehensive-analysis",
            "ccus_india_storage_overview": "/api/ccus/india-storage-overview",
            "ccus_industry_types": "/api/ccus/industry-types",
            # Eco-Shopping endpoints
            "eco_products": "/api/eco-shopping/products",
            "eco_product_detail": "/api/eco-shopping/products/<id>",
            "eco_categories": "/api/eco-shopping/categories",
            "eco_cart": "/api/eco-shopping/cart",
            "eco_cart_add": "/api/eco-shopping/cart/add",
            "eco_facts": "/api/eco-shopping/educational/facts",
            "eco_tips": "/api/eco-shopping/educational/tips",
            "eco_challenges": "/api/eco-shopping/educational/challenges",
            "eco_content": "/api/eco-shopping/educational/content",
            "eco_recommendations": "/api/eco-shopping/recommendations"
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
