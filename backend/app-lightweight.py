from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Only import routes that don't require heavy dependencies
# Comment out routes that need numpy/pandas/opencv to make deployment lighter
try:
    from api.chatbot import chatbot_bp
    HAS_CHATBOT = True
except ImportError:
    HAS_CHATBOT = False
    print("Warning: Chatbot not available (missing dependencies)")

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure CORS to allow requests from frontend
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Register available blueprints
if HAS_CHATBOT:
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

@app.route('/')
def hello():
    """Root endpoint"""
    return jsonify({
        "message": "Climate Tracker API v2.0 - Lightweight Deployment",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "health": "/api/health",
            "chatbot": "/api/chatbot/chat" if HAS_CHATBOT else "disabled"
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "climate-tracker-api",
        "features": {
            "chatbot": HAS_CHATBOT
        }
    })

# Simple carbon footprint calculator endpoint (no dependencies needed)
@app.route('/api/carbon-footprint/simple', methods=['POST'])
def simple_carbon_footprint():
    """
    Simple carbon footprint calculator without heavy dependencies
    """
    try:
        data = request.get_json()
        
        # Basic emission factors (kg CO2 per unit)
        factors = {
            'car_km': 0.192,        # kg CO2 per km
            'bus_km': 0.089,        # kg CO2 per km
            'train_km': 0.041,      # kg CO2 per km  
            'flight_km': 0.255,     # kg CO2 per km
            'electricity_kwh': 0.527,  # kg CO2 per kWh
            'gas_kwh': 0.203,       # kg CO2 per kWh
            'meat_kg': 27.0,        # kg CO2 per kg
            'vegetarian_meal': 1.5,  # kg CO2 per meal
            'waste_kg': 0.5         # kg CO2 per kg
        }
        
        total_emissions = 0
        breakdown = {}
        
        for activity, value in data.items():
            if activity in factors:
                emissions = value * factors[activity]
                total_emissions += emissions
                breakdown[activity] = round(emissions, 2)
        
        return jsonify({
            "total_co2_kg": round(total_emissions, 2),
            "breakdown": breakdown,
            "message": "Carbon footprint calculated successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting Climate Tracker API on 0.0.0.0:{port}")
    print(f"Debug mode: {app.config['DEBUG']}")
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
