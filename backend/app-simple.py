from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure CORS - allow all origins for now
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = False

@app.route('/')
def hello():
    """Root endpoint"""
    return jsonify({
        "message": "Climate Tracker API v2.0 - Successfully Deployed on Render!",
        "status": "running",
        "version": "2.0.1",
        "author": "Kartik Patil",
        "endpoints": {
            "health": "/api/health",
            "carbon_calculator": "/api/carbon-footprint/simple"
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "climate-tracker-api",
        "message": "Backend is running successfully!"
    })

@app.route('/api/carbon-footprint/simple', methods=['POST', 'GET'])
def simple_carbon_footprint():
    """
    Simple carbon footprint calculator
    POST with JSON body or GET for demo
    """
    if request.method == 'GET':
        return jsonify({
            "message": "Send POST request with activity data",
            "example": {
                "car_km": 100,
                "electricity_kwh": 50,
                "meat_kg": 2
            }
        })
    
    try:
        data = request.get_json() or {}
        
        # Basic emission factors (kg CO2 per unit)
        factors = {
            'car_km': 0.192,
            'bus_km': 0.089,
            'train_km': 0.041,
            'flight_km': 0.255,
            'electricity_kwh': 0.527,
            'gas_kwh': 0.203,
            'meat_kg': 27.0,
            'vegetarian_meal': 1.5,
            'waste_kg': 0.5
        }
        
        total_emissions = 0
        breakdown = {}
        
        for activity, value in data.items():
            if activity in factors:
                emissions = float(value) * factors[activity]
                total_emissions += emissions
                breakdown[activity] = round(emissions, 2)
        
        return jsonify({
            "success": True,
            "total_co2_kg": round(total_emissions, 2),
            "breakdown": breakdown,
            "message": "Carbon footprint calculated successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error calculating carbon footprint"
        }), 400

@app.route('/api/test')
def test():
    """Test endpoint"""
    return jsonify({
        "test": "success",
        "message": "API is working correctly!",
        "timestamp": "2025-10-11"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong on the server",
        "status": 500
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"🚀 Starting Climate Tracker API on 0.0.0.0:{port}")
    print(f"📝 Debug mode: {app.config['DEBUG']}")
    print(f"✅ CORS enabled for all origins")
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
