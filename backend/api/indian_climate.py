from flask import Blueprint, request, jsonify
from services.indian_weather_service import indian_weather_service
from datetime import datetime
import traceback
import logging

logger = logging.getLogger(__name__)

indian_climate_bp = Blueprint('indian_climate', __name__)

@indian_climate_bp.route('/india/overview', methods=['GET'])
def get_india_overview():
    """Get overview of Indian climate data"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        weather_data = indian_weather_service.get_weather_data()
        
        return jsonify({
            "status": "success",
            "data": weather_data,
            "timestamp": datetime.now().isoformat(),
            "country": "India"
        })
    
    except Exception as e:
        logger.error(f"Error in get_india_overview: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Failed to fetch India overview: {str(e)}"}), 500

@indian_climate_bp.route('/india/cities', methods=['GET'])
def get_indian_cities():
    """Get climate data for all Indian cities"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        weather_data = indian_weather_service.get_weather_data()
        cities_data = weather_data.get('cities_overview', [])
        
        return jsonify({
            "status": "success",
            "cities": cities_data,
            "count": len(cities_data),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_indian_cities: {e}")
        return jsonify({"error": f"Failed to fetch Indian cities data: {str(e)}"}), 500

@indian_climate_bp.route('/india/city/<city_name>', methods=['GET'])
def get_city_climate(city_name):
    """Get detailed climate data for a specific Indian city"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        city_data = indian_weather_service.get_city_weather(city_name)
        
        if not city_data:
            return jsonify({"error": f"City '{city_name}' not found"}), 404
        
        return jsonify({
            "status": "success",
            "city_data": city_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_city_climate: {e}")
        return jsonify({"error": f"Failed to fetch city climate data: {str(e)}"}), 500

@indian_climate_bp.route('/india/regions', methods=['GET'])
def get_regional_data():
    """Get climate data aggregated by Indian states/regions"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        weather_data = indian_weather_service.get_weather_data()
        regional_data = weather_data.get('regional_summary', {})
        
        return jsonify({
            "status": "success",
            "regions": regional_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_regional_data: {e}")
        return jsonify({"error": f"Failed to fetch regional data: {str(e)}"}), 500

@indian_climate_bp.route('/india/trends', methods=['GET'])
def get_monthly_trends():
    """Get monthly climate trends for India"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        weather_data = indian_weather_service.get_weather_data()
        trends_data = weather_data.get('monthly_trends', {})
        
        return jsonify({
            "status": "success",
            "trends": trends_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_monthly_trends: {e}")
        return jsonify({"error": f"Failed to fetch trends data: {str(e)}"}), 500

@indian_climate_bp.route('/india/current', methods=['GET'])
def get_current_conditions():
    """Get current weather conditions summary for India"""
    try:
        # Initialize service if not already done
        if not indian_weather_service.processed_data:
            success = indian_weather_service.initialize()
            if not success:
                return jsonify({"error": "Failed to initialize weather service"}), 500
        
        weather_data = indian_weather_service.get_weather_data()
        current_data = weather_data.get('current_conditions', {})
        
        return jsonify({
            "status": "success",
            "current": current_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_current_conditions: {e}")
        return jsonify({"error": f"Failed to fetch current conditions: {str(e)}"}), 500

@indian_climate_bp.route('/india/download-status', methods=['GET'])
def get_download_status():
    """Check if the Kaggle dataset has been downloaded successfully"""
    try:
        dataset_path = indian_weather_service.dataset_path
        has_real_data = dataset_path is not None
        
        return jsonify({
            "status": "success",
            "dataset_downloaded": has_real_data,
            "dataset_path": dataset_path,
            "using_mock_data": not has_real_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_download_status: {e}")
        return jsonify({"error": f"Failed to check download status: {str(e)}"}), 500

@indian_climate_bp.route('/india/initialize', methods=['POST'])
def initialize_service():
    """Manually initialize/reinitialize the Indian weather service"""
    try:
        success = indian_weather_service.initialize()
        
        return jsonify({
            "status": "success" if success else "partial",
            "initialized": success,
            "message": "Service initialized successfully" if success else "Service initialized with mock data",
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in initialize_service: {e}")
        return jsonify({"error": f"Failed to initialize service: {str(e)}"}), 500

@indian_climate_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Indian climate API"""
    return jsonify({
        "status": "healthy",
        "service": "indian-climate-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })