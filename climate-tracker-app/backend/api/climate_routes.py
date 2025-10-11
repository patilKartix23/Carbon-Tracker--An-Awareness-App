from flask import Blueprint, request, jsonify
from services.data_integrator import ClimateDataIntegrator
from services.carbon_calculator import CarbonFootprintCalculator
from datetime import datetime, timedelta
import traceback

climate_bp = Blueprint('climate', __name__)
data_integrator = ClimateDataIntegrator()
carbon_calculator = CarbonFootprintCalculator()

@climate_bp.route('/climate-data', methods=['GET'])
def get_climate_data():
    """Get comprehensive climate data for a location"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        days = request.args.get('days', 7, type=int)
        
        if not lat or not lon:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({"error": "Invalid coordinates"}), 400
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for NASA API
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Fetch data from multiple sources
        nasa_data = data_integrator.get_nasa_satellite_data(lat, lon, start_str, end_str)
        air_quality = data_integrator.get_air_quality_data(lat, lon)
        weather_forecast = data_integrator.get_weather_forecast(lat, lon)
        
        # Process and combine data
        processed_data = data_integrator.process_and_normalize_data(nasa_data)
        
        return jsonify({
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "date_range": {"start": start_str, "end": end_str},
            "data": {
                "historical_climate": nasa_data,
                "air_quality": air_quality,
                "weather_forecast": weather_forecast,
                "processed_summary": processed_data.to_dict() if not processed_data.empty else {}
            },
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in get_climate_data: {e}")
        print(traceback.format_exc())
        return jsonify({"error": f"Failed to fetch climate data: {str(e)}"}), 500

@climate_bp.route('/carbon-footprint', methods=['POST'])
def calculate_carbon_footprint():
    """Calculate carbon footprint based on user activities"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Calculate footprint using the enhanced calculator
        footprint_result = carbon_calculator.calculate_total_footprint(data)
        
        # Get personalized recommendations
        recommendations = carbon_calculator.get_personalized_recommendations(
            footprint_result, 
            data.get('location')
        )
        
        # Compare to averages
        comparison = carbon_calculator.compare_to_averages(
            footprint_result['daily_footprint_kg_co2']
        )
        
        return jsonify({
            "status": "success",
            "footprint": footprint_result,
            "recommendations": recommendations,
            "comparison": comparison,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in calculate_carbon_footprint: {e}")
        print(traceback.format_exc())
        return jsonify({"error": f"Failed to calculate carbon footprint: {str(e)}"}), 500

@climate_bp.route('/carbon-footprint/simple', methods=['POST'])
def calculate_simple_footprint():
    """Simplified carbon footprint calculation for basic inputs"""
    try:
        data = request.get_json()
        
        # Extract simple inputs
        transportation = data.get('transportation', {})
        energy = data.get('energy', {})
        
        # Convert to standard format
        standard_data = {
            'transportation': {},
            'energy': {}
        }
        
        # Handle transportation
        if 'car_miles' in transportation:
            standard_data['transportation']['car_gasoline'] = transportation['car_miles']
        
        # Handle energy
        if 'electricity_kwh' in energy:
            standard_data['energy']['electricity_grid'] = energy['electricity_kwh']
        
        # Calculate using enhanced calculator
        footprint_result = carbon_calculator.calculate_total_footprint(standard_data)
        recommendations = carbon_calculator.get_personalized_recommendations(footprint_result)
        
        # Return simplified response for backward compatibility
        return jsonify({
            "daily_footprint_lbs_co2": footprint_result['daily_footprint_lbs_co2'],
            "daily_footprint_kg_co2": footprint_result['daily_footprint_kg_co2'],
            "breakdown": {
                "transportation": footprint_result['breakdown']['transportation']['total_kg_co2'],
                "energy": footprint_result['breakdown']['energy']['total_kg_co2']
            },
            "recommendations": recommendations[:3],  # Top 3 for simple version
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in calculate_simple_footprint: {e}")
        return jsonify({"error": f"Failed to calculate footprint: {str(e)}"}), 500

@climate_bp.route('/air-quality', methods=['GET'])
def get_air_quality():
    """Get current air quality data for a location"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        air_quality_data = data_integrator.get_air_quality_data(lat, lon)
        
        return jsonify({
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "air_quality": air_quality_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in get_air_quality: {e}")
        return jsonify({"error": f"Failed to fetch air quality data: {str(e)}"}), 500

@climate_bp.route('/weather-forecast', methods=['GET'])
def get_weather_forecast():
    """Get weather forecast for a location"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        forecast_data = data_integrator.get_weather_forecast(lat, lon)
        
        return jsonify({
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "forecast": forecast_data,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in get_weather_forecast: {e}")
        return jsonify({"error": f"Failed to fetch weather forecast: {str(e)}"}), 500

@climate_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the climate API"""
    return jsonify({
        "status": "healthy",
        "service": "climate-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })
