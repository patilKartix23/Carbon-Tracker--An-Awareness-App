"""
Carbon Activity Tracking API - Activity-based carbon footprint logging
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import structlog
from typing import Dict, List
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import User, CarbonLog
from services.carbon_activity_service import CarbonActivityService

logger = structlog.get_logger()

# Create blueprint
carbon_activity_bp = Blueprint('carbon_activity', __name__)

# Initialize service
carbon_service = CarbonActivityService()

# Emission factors for different activities (kg CO₂ per unit)
EMISSION_FACTORS = {
    "transport": {
        "car": 0.12,        # per km
        "bus": 0.05,        # per km
        "train": 0.041,     # per km
        "flight": 0.25,     # per km
        "motorcycle": 0.08, # per km
        "bicycle": 0.0,     # per km
        "walking": 0.0      # per km
    },
    "food": {
        "beef": 5.0,        # per meal
        "lamb": 3.5,        # per meal
        "pork": 1.8,        # per meal
        "chicken": 1.5,     # per meal
        "fish": 1.2,        # per meal
        "vegetarian": 0.8,  # per meal
        "vegan": 0.5,       # per meal
        "dairy": 0.9        # per serving
    },
    "energy": {
        "electricity": 0.82,    # per kWh (India average)
        "gas": 0.184,          # per kWh
        "heating_oil": 0.264,  # per kWh
        "coal": 0.820          # per kWh
    },
    "shopping": {
        "clothes": 20.0,       # per item
        "electronics": 50.0,   # per item
        "books": 2.5,          # per item
        "furniture": 100.0     # per item
    }
}

@carbon_activity_bp.route('/calculate', methods=['POST'])
def calculate_activity_emission():
    """Calculate CO₂ emissions for a single activity"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'activity_type' not in data or 'value' not in data:
            return jsonify({
                'error': 'Missing required fields: activity_type and value'
            }), 400
        
        activity_type = data['activity_type'].lower()
        value = float(data['value'])
        user_id = data.get('user_id')
        category = data.get('category', 'transport')  # default category
        
        # Find emission factor
        factor = None
        for cat, activities in EMISSION_FACTORS.items():
            if activity_type in activities:
                factor = activities[activity_type]
                category = cat
                break
        
        if factor is None:
            return jsonify({
                'error': f'Unknown activity type: {activity_type}',
                'available_activities': EMISSION_FACTORS
            }), 400
        
        # Calculate emissions
        emissions = value * factor
        
        # Prepare response
        result = {
            'user_id': user_id,
            'activity_type': activity_type,
            'category': category,
            'value': value,
            'unit': carbon_service.get_unit_for_activity(activity_type, category),
            'emissions_kg_co2': round(emissions, 3),
            'timestamp': datetime.now().isoformat(),
            'message': carbon_service.get_impact_message(emissions, category)
        }
        
        logger.info("Activity emission calculated", 
                   activity=activity_type, 
                   emissions=emissions,
                   user_id=user_id)
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': f'Invalid value format: {str(e)}'}), 400
    except Exception as e:
        logger.error("Error calculating activity emission", error=str(e))
        return jsonify({'error': 'Internal server error'}), 500

@carbon_activity_bp.route('/log', methods=['POST'])
def log_activity():
    """Log an activity and save to database"""
    try:
        data = request.get_json()
        
        # Calculate emissions first
        calc_result = calculate_activity_emission()
        if calc_result[1] != 200:  # If calculation failed
            return calc_result
        
        calc_data = calc_result[0].get_json()
        
        # Save to database (simplified - in real app, you'd use proper user auth)
        user_id = data.get('user_id', 'anonymous')
        
        activity_log = {
            'user_id': user_id,
            'date': datetime.now(),
            'activity_type': calc_data['activity_type'],
            'category': calc_data['category'],
            'value': calc_data['value'],
            'unit': calc_data['unit'],
            'emissions_kg_co2': calc_data['emissions_kg_co2'],
            'description': data.get('description', ''),
            'location': data.get('location', '')
        }
        
        # For now, we'll create a simplified log entry
        # In production, this would be saved to the database
        
        result = {
            **calc_data,
            'saved': True,
            'log_id': f"log_{datetime.now().timestamp()}",
            'daily_total_updated': True
        }
        
        logger.info("Activity logged successfully", 
                   activity=calc_data['activity_type'],
                   user_id=user_id)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error("Error logging activity", error=str(e))
        return jsonify({'error': 'Failed to log activity'}), 500

@carbon_activity_bp.route('/daily-summary/<user_id>', methods=['GET'])
def get_daily_summary(user_id):
    """Get daily carbon footprint summary for a user"""
    try:
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # In a real implementation, this would query the database
        # For now, return mock data
        summary = {
            'user_id': user_id,
            'date': date_str,
            'total_emissions_kg_co2': 8.5,
            'breakdown': {
                'transport': 4.2,
                'food': 3.1,
                'energy': 1.0,
                'shopping': 0.2
            },
            'activities_logged': 6,
            'comparison': {
                'vs_yesterday': -1.2,  # kg CO₂ difference
                'vs_weekly_avg': 0.8,
                'vs_global_avg': -2.5   # Below global average
            },
            'achievements': [
                "🚲 Chose cycling over driving",
                "🥗 Had 2 vegetarian meals today"
            ],
            'recommendations': [
                "Try taking the bus instead of driving tomorrow",
                "Consider having one more plant-based meal"
            ]
        }
        
        return jsonify(summary)
    
    except Exception as e:
        logger.error("Error fetching daily summary", error=str(e))
        return jsonify({'error': 'Failed to fetch daily summary'}), 500

@carbon_activity_bp.route('/activities', methods=['GET'])
def get_available_activities():
    """Get list of all available activities for tracking"""
    try:
        activities = []
        
        for category, acts in EMISSION_FACTORS.items():
            for activity, factor in acts.items():
                activities.append({
                    'category': category,
                    'activity': activity,
                    'display_name': carbon_service.get_display_name(activity),
                    'unit': carbon_service.get_unit_for_activity(activity, category),
                    'emission_factor': factor,
                    'examples': carbon_service.get_examples(activity, category)
                })
        
        return jsonify({
            'activities': activities,
            'categories': list(EMISSION_FACTORS.keys()),
            'total_count': len(activities)
        })
    
    except Exception as e:
        logger.error("Error fetching activities", error=str(e))
        return jsonify({'error': 'Failed to fetch activities'}), 500

@carbon_activity_bp.route('/weekly-trends/<user_id>', methods=['GET'])
def get_weekly_trends(user_id):
    """Get weekly carbon footprint trends"""
    try:
        # Mock data for weekly trends
        end_date = datetime.now()
        dates = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        trends = {
            'user_id': user_id,
            'period': f"{dates[0]} to {dates[-1]}",
            'daily_emissions': [
                {'date': dates[0], 'total': 9.2, 'transport': 5.1, 'food': 2.8, 'energy': 1.1, 'shopping': 0.2},
                {'date': dates[1], 'total': 7.8, 'transport': 3.2, 'food': 3.5, 'energy': 0.9, 'shopping': 0.2},
                {'date': dates[2], 'total': 6.5, 'transport': 2.1, 'food': 3.2, 'energy': 1.0, 'shopping': 0.2},
                {'date': dates[3], 'total': 8.9, 'transport': 4.8, 'food': 2.9, 'energy': 1.0, 'shopping': 0.2},
                {'date': dates[4], 'total': 7.2, 'transport': 2.9, 'food': 3.1, 'energy': 1.0, 'shopping': 0.2},
                {'date': dates[5], 'total': 8.1, 'transport': 4.2, 'food': 2.7, 'energy': 1.0, 'shopping': 0.2},
                {'date': dates[6], 'total': 8.5, 'transport': 4.2, 'food': 3.1, 'energy': 1.0, 'shopping': 0.2}
            ],
            'weekly_total': 56.2,
            'weekly_average': 8.0,
            'trend': 'decreasing',  # increasing, decreasing, stable
            'best_day': dates[2],
            'worst_day': dates[0],
            'insights': [
                "Your transport emissions were highest on Monday and Thursday",
                "You had your lowest footprint on Wednesday - great job!",
                "Consider reducing car travel on Mondays"
            ]
        }
        
        return jsonify(trends)
    
    except Exception as e:
        logger.error("Error fetching weekly trends", error=str(e))
        return jsonify({'error': 'Failed to fetch weekly trends'}), 500

@carbon_activity_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get carbon footprint leaderboard (lowest emissions win)"""
    try:
        # Mock leaderboard data
        leaderboard = {
            'period': 'This Week',
            'rankings': [
                {'rank': 1, 'user': 'EcoWarrior23', 'emissions': 4.2, 'trend': 'down'},
                {'rank': 2, 'user': 'GreenThumb', 'emissions': 5.8, 'trend': 'stable'},
                {'rank': 3, 'user': 'ClimateHero', 'emissions': 6.1, 'trend': 'down'},
                {'rank': 4, 'user': 'SustainableSara', 'emissions': 6.7, 'trend': 'up'},
                {'rank': 5, 'user': 'You', 'emissions': 8.0, 'trend': 'down', 'is_current_user': True},
            ],
            'total_participants': 1247,
            'your_rank': 5,
            'percentile': 'Top 15%',
            'improvement_tip': "You're doing great! Try cycling once more this week to move up the leaderboard."
        }
        
        return jsonify(leaderboard)
    
    except Exception as e:
        logger.error("Error fetching leaderboard", error=str(e))
        return jsonify({'error': 'Failed to fetch leaderboard'}), 500

@carbon_activity_bp.route('/suggestions', methods=['GET'])
def get_activity_suggestions():
    """Get personalized activity suggestions to reduce carbon footprint"""
    try:
        user_id = request.args.get('user_id', 'anonymous')
        category = request.args.get('category', 'all')
        
        suggestions = carbon_service.get_personalized_suggestions(user_id, category)
        
        return jsonify({
            'user_id': user_id,
            'suggestions': suggestions,
            'tips_of_the_day': [
                "🚲 Cycling 5km saves 0.6kg CO₂ compared to driving",
                "🥗 Choosing vegetarian over beef saves 4.2kg CO₂ per meal",
                "💡 Switching off lights saves 0.1kg CO₂ per hour"
            ]
        })
    
    except Exception as e:
        logger.error("Error fetching suggestions", error=str(e))
        return jsonify({'error': 'Failed to fetch suggestions'}), 500
