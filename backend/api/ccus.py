"""
CCUS (Carbon Capture, Utilization and Storage) API Routes
Handles carbon capture simulation, storage mapping, and utilization pathways
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
import math

ccus_bp = Blueprint('ccus', __name__)

class CCUSSimulator:
    def __init__(self):
        # CCUS efficiency rates (percentage of CO2 that can be captured)
        self.capture_efficiency = {
            'cement_industry': 0.90,
            'steel_industry': 0.85,
            'power_plant_coal': 0.90,
            'power_plant_gas': 0.85,
            'oil_refinery': 0.88,
            'chemical_plant': 0.87,
            'aluminum_smelting': 0.82,
            'pulp_paper': 0.75,
            'fertilizer_plant': 0.89
        }
        
        # Storage capacity estimates for different geological formations (MT CO2)
        self.storage_sites_india = {
            'Gujarat': {
                'depleted_oil_wells': 2500,
                'saline_aquifers': 8900,
                'coal_seams': 450,
                'total_capacity': 11850
            },
            'Rajasthan': {
                'depleted_oil_wells': 1800,
                'saline_aquifers': 6200,
                'coal_seams': 0,
                'total_capacity': 8000
            },
            'Jharkhand': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 3400,
                'coal_seams': 2100,
                'total_capacity': 5500
            },
            'Assam': {
                'depleted_oil_wells': 900,
                'saline_aquifers': 2800,
                'coal_seams': 300,
                'total_capacity': 4000
            },
            'Odisha': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 4500,
                'coal_seams': 1800,
                'total_capacity': 6300
            },
            'Maharashtra': {
                'depleted_oil_wells': 400,
                'saline_aquifers': 3200,
                'coal_seams': 600,
                'total_capacity': 4200
            }
        }
        
        # Utilization pathways and their conversion efficiency
        self.utilization_pathways = {
            'enhanced_oil_recovery': {
                'efficiency': 0.70,  # CO2 stored permanently
                'description': 'Inject CO2 into oil reservoirs to extract more oil',
                'economics': 'Revenue generating',
                'capacity_factor': 0.8
            },
            'concrete_building_materials': {
                'efficiency': 0.85,
                'description': 'Convert CO2 into building blocks and concrete',
                'economics': 'Cost neutral',
                'capacity_factor': 0.6
            },
            'synthetic_fuels': {
                'efficiency': 0.75,
                'description': 'Convert CO2 + H2 into synthetic gasoline/diesel',
                'economics': 'Cost premium',
                'capacity_factor': 0.9
            },
            'chemicals_plastics': {
                'efficiency': 0.80,
                'description': 'Use CO2 as feedstock for chemicals and plastics',
                'economics': 'Revenue generating',
                'capacity_factor': 0.7
            },
            'carbon_fiber': {
                'efficiency': 0.95,
                'description': 'Convert CO2 into carbon fiber materials',
                'economics': 'High value',
                'capacity_factor': 0.5
            },
            'algae_biofuels': {
                'efficiency': 0.65,
                'description': 'Feed CO2 to algae for biofuel production',
                'economics': 'Cost neutral',
                'capacity_factor': 0.8
            }
        }
        
        # Carbon credit pricing (INR per tonne CO2)
        self.carbon_credit_price = {
            'voluntary_market': 1200,  # INR per tonne
            'compliance_market': 2500,  # INR per tonne
            'government_incentive': 1800  # INR per tonne
        }

    def calculate_capture_potential(self, industry_type: str, annual_emissions: float) -> Dict:
        """Calculate CO2 capture potential for an industry"""
        if industry_type not in self.capture_efficiency:
            return {'error': f'Industry type {industry_type} not supported'}
        
        efficiency = self.capture_efficiency[industry_type]
        capturable_co2 = annual_emissions * efficiency
        remaining_emissions = annual_emissions * (1 - efficiency)
        
        return {
            'annual_emissions_tonnes': annual_emissions,
            'capture_efficiency': efficiency * 100,
            'capturable_co2_tonnes': round(capturable_co2, 2),
            'remaining_emissions_tonnes': round(remaining_emissions, 2),
            'reduction_percentage': round(efficiency * 100, 1)
        }

    def suggest_storage_sites(self, co2_amount: float, user_state: str = None) -> List[Dict]:
        """Suggest optimal storage sites based on CO2 amount and location"""
        suggestions = []
        
        # If user specifies state, prioritize that state
        if user_state and user_state in self.storage_sites_india:
            state_data = self.storage_sites_india[user_state]
            suggestions.append({
                'state': user_state,
                'total_capacity_mt': state_data['total_capacity'],
                'storage_options': state_data,
                'distance_factor': 1.0,  # Local storage
                'recommended': True
            })
        
        # Add other suitable states based on capacity
        for state, data in self.storage_sites_india.items():
            if state != user_state and data['total_capacity'] > co2_amount / 1000:  # Convert tonnes to MT
                distance_factor = self._calculate_distance_factor(user_state, state)
                suggestions.append({
                    'state': state,
                    'total_capacity_mt': data['total_capacity'],
                    'storage_options': data,
                    'distance_factor': distance_factor,
                    'recommended': distance_factor < 2.0
                })
        
        return sorted(suggestions, key=lambda x: (x['distance_factor'], -x['total_capacity_mt']))

    def calculate_utilization_potential(self, co2_amount: float) -> List[Dict]:
        """Calculate potential utilization pathways for captured CO2"""
        pathways = []
        
        for pathway, data in self.utilization_pathways.items():
            utilizable_amount = co2_amount * data['efficiency'] * data['capacity_factor']
            
            pathways.append({
                'pathway': pathway,
                'description': data['description'],
                'utilizable_co2_tonnes': round(utilizable_amount, 2),
                'efficiency_percent': round(data['efficiency'] * 100, 1),
                'economics': data['economics'],
                'capacity_factor': data['capacity_factor'],
                'recommended': data['capacity_factor'] > 0.7 and data['efficiency'] > 0.75
            })
        
        return sorted(pathways, key=lambda x: x['utilizable_co2_tonnes'], reverse=True)

    def calculate_carbon_credits(self, stored_co2: float, credit_type: str = 'voluntary_market') -> Dict:
        """Calculate carbon credit value for stored CO2"""
        if credit_type not in self.carbon_credit_price:
            credit_type = 'voluntary_market'
        
        price_per_tonne = self.carbon_credit_price[credit_type]
        total_value = stored_co2 * price_per_tonne
        
        return {
            'stored_co2_tonnes': stored_co2,
            'credit_type': credit_type,
            'price_per_tonne_inr': price_per_tonne,
            'total_value_inr': round(total_value, 2),
            'total_value_usd': round(total_value / 83, 2),  # Approximate INR to USD
            'annual_revenue_potential': round(total_value, 2)
        }

    def _calculate_distance_factor(self, origin_state: str, destination_state: str) -> float:
        """Simple distance factor calculation (in real app, use actual geographic data)"""
        # Simplified distance matrix (in reality, would use actual coordinates)
        state_distances = {
            ('Gujarat', 'Rajasthan'): 1.2,
            ('Gujarat', 'Maharashtra'): 1.5,
            ('Jharkhand', 'Odisha'): 1.3,
            ('Jharkhand', 'West Bengal'): 1.1,
            ('Assam', 'West Bengal'): 1.8,
        }
        
        if not origin_state:
            return 1.5  # Default moderate distance
        
        key = (origin_state, destination_state)
        reverse_key = (destination_state, origin_state)
        
        return state_distances.get(key, state_distances.get(reverse_key, 2.0))

# Initialize CCUS simulator
ccus_simulator = CCUSSimulator()

@ccus_bp.route('/capture-simulation', methods=['POST'])
def simulate_carbon_capture():
    """Simulate carbon capture for industrial emissions"""
    try:
        data = request.get_json()
        
        industry_type = data.get('industry_type')
        annual_emissions = data.get('annual_emissions_tonnes', 0)
        
        if not industry_type or annual_emissions <= 0:
            return jsonify({'error': 'Valid industry_type and annual_emissions_tonnes required'}), 400
        
        capture_result = ccus_simulator.calculate_capture_potential(industry_type, annual_emissions)
        
        if 'error' in capture_result:
            return jsonify(capture_result), 400
        
        return jsonify({
            'success': True,
            'capture_simulation': capture_result,
            'available_industries': list(ccus_simulator.capture_efficiency.keys())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ccus_bp.route('/storage-sites', methods=['POST'])
def get_storage_sites():
    """Get suitable storage sites for captured CO2"""
    try:
        data = request.get_json()
        
        co2_amount = data.get('co2_tonnes', 0)
        user_state = data.get('state')
        
        if co2_amount <= 0:
            return jsonify({'error': 'Valid co2_tonnes required'}), 400
        
        storage_suggestions = ccus_simulator.suggest_storage_sites(co2_amount, user_state)
        
        return jsonify({
            'success': True,
            'co2_amount_tonnes': co2_amount,
            'storage_suggestions': storage_suggestions,
            'total_sites_available': len(storage_suggestions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ccus_bp.route('/utilization-pathways', methods=['POST'])
def get_utilization_pathways():
    """Get CO2 utilization pathways and potential"""
    try:
        data = request.get_json()
        
        co2_amount = data.get('co2_tonnes', 0)
        
        if co2_amount <= 0:
            return jsonify({'error': 'Valid co2_tonnes required'}), 400
        
        utilization_pathways = ccus_simulator.calculate_utilization_potential(co2_amount)
        
        return jsonify({
            'success': True,
            'co2_amount_tonnes': co2_amount,
            'utilization_pathways': utilization_pathways,
            'recommended_pathways': [p for p in utilization_pathways if p['recommended']]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ccus_bp.route('/carbon-credits', methods=['POST'])
def calculate_carbon_credits():
    """Calculate carbon credit value for stored CO2"""
    try:
        data = request.get_json()
        
        stored_co2 = data.get('stored_co2_tonnes', 0)
        credit_type = data.get('credit_type', 'voluntary_market')
        
        if stored_co2 <= 0:
            return jsonify({'error': 'Valid stored_co2_tonnes required'}), 400
        
        credit_calculation = ccus_simulator.calculate_carbon_credits(stored_co2, credit_type)
        
        return jsonify({
            'success': True,
            'carbon_credits': credit_calculation,
            'available_credit_types': list(ccus_simulator.carbon_credit_price.keys())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ccus_bp.route('/comprehensive-analysis', methods=['POST'])
def comprehensive_ccus_analysis():
    """Comprehensive CCUS analysis including capture, storage, utilization, and credits"""
    try:
        data = request.get_json()
        
        industry_type = data.get('industry_type')
        annual_emissions = data.get('annual_emissions_tonnes', 0)
        user_state = data.get('state')
        credit_type = data.get('credit_type', 'voluntary_market')
        
        if not industry_type or annual_emissions <= 0:
            return jsonify({'error': 'Valid industry_type and annual_emissions_tonnes required'}), 400
        
        # 1. Calculate capture potential
        capture_result = ccus_simulator.calculate_capture_potential(industry_type, annual_emissions)
        if 'error' in capture_result:
            return jsonify(capture_result), 400
        
        capturable_co2 = capture_result['capturable_co2_tonnes']
        
        # 2. Get storage suggestions
        storage_suggestions = ccus_simulator.suggest_storage_sites(capturable_co2, user_state)
        
        # 3. Get utilization pathways
        utilization_pathways = ccus_simulator.calculate_utilization_potential(capturable_co2)
        
        # 4. Calculate carbon credits
        credit_calculation = ccus_simulator.calculate_carbon_credits(capturable_co2, credit_type)
        
        # 5. Generate recommendations
        recommendations = generate_ccus_recommendations(capture_result, storage_suggestions, utilization_pathways, credit_calculation)
        
        return jsonify({
            'success': True,
            'input_data': {
                'industry_type': industry_type,
                'annual_emissions_tonnes': annual_emissions,
                'state': user_state,
                'credit_type': credit_type
            },
            'capture_analysis': capture_result,
            'storage_options': storage_suggestions[:3],  # Top 3 recommendations
            'utilization_options': utilization_pathways[:5],  # Top 5 pathways
            'carbon_credits': credit_calculation,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_ccus_recommendations(capture_data, storage_sites, utilization_pathways, carbon_credits):
    """Generate actionable CCUS recommendations"""
    recommendations = []
    
    # Capture efficiency recommendation
    if capture_data['capture_efficiency'] >= 85:
        recommendations.append({
            'type': 'capture',
            'priority': 'high',
            'message': f"Excellent capture potential! You can capture {capture_data['capture_efficiency']:.1f}% of emissions.",
            'action': 'Proceed with CCUS implementation planning'
        })
    else:
        recommendations.append({
            'type': 'capture',
            'priority': 'medium',
            'message': f"Moderate capture efficiency of {capture_data['capture_efficiency']:.1f}%. Consider technology upgrades.",
            'action': 'Evaluate advanced capture technologies'
        })
    
    # Storage recommendation
    recommended_storage = [site for site in storage_sites if site.get('recommended', False)]
    if recommended_storage:
        recommendations.append({
            'type': 'storage',
            'priority': 'high',
            'message': f"Suitable storage sites available in {recommended_storage[0]['state']}",
            'action': f"Explore partnerships with storage facilities in {recommended_storage[0]['state']}"
        })
    
    # Utilization recommendation
    high_value_pathways = [p for p in utilization_pathways if p['economics'] in ['High value', 'Revenue generating']]
    if high_value_pathways:
        best_pathway = high_value_pathways[0]
        recommendations.append({
            'type': 'utilization',
            'priority': 'high',
            'message': f"Consider {best_pathway['pathway']} - {best_pathway['economics'].lower()}",
            'action': f"Evaluate {best_pathway['description'].lower()}"
        })
    
    # Financial recommendation
    annual_revenue = carbon_credits['annual_revenue_potential']
    if annual_revenue > 1000000:  # > 10 lakh INR
        recommendations.append({
            'type': 'financial',
            'priority': 'high',
            'message': f"Strong financial case with ₹{annual_revenue:,.0f} annual carbon credit potential",
            'action': 'Develop detailed financial model and seek funding'
        })
    
    return recommendations

@ccus_bp.route('/india-storage-overview', methods=['GET'])
def get_india_storage_overview():
    """Get overview of CCUS storage potential across India"""
    try:
        total_capacity = sum(site['total_capacity'] for site in ccus_simulator.storage_sites_india.values())
        
        return jsonify({
            'success': True,
            'india_storage_overview': {
                'total_capacity_mt': total_capacity,
                'states_covered': len(ccus_simulator.storage_sites_india),
                'state_wise_data': ccus_simulator.storage_sites_india,
                'top_states': sorted(
                    ccus_simulator.storage_sites_india.items(),
                    key=lambda x: x[1]['total_capacity'],
                    reverse=True
                )[:5]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ccus_bp.route('/industry-types', methods=['GET'])
def get_supported_industries():
    """Get list of supported industry types for CCUS"""
    return jsonify({
        'success': True,
        'supported_industries': [
            {
                'industry_type': industry,
                'capture_efficiency_percent': round(efficiency * 100, 1),
                'description': get_industry_description(industry)
            }
            for industry, efficiency in ccus_simulator.capture_efficiency.items()
        ]
    })

def get_industry_description(industry_type):
    """Get description for industry types"""
    descriptions = {
        'cement_industry': 'Cement manufacturing plants - high CO2 emissions from limestone calcination',
        'steel_industry': 'Steel production facilities - emissions from coke and limestone use',
        'power_plant_coal': 'Coal-fired power plants - major point source emissions',
        'power_plant_gas': 'Natural gas power plants - cleaner but still significant emissions',
        'oil_refinery': 'Petroleum refineries - process emissions from crude oil processing',
        'chemical_plant': 'Chemical manufacturing - various process emissions',
        'aluminum_smelting': 'Aluminum production - high energy intensity with CO2 emissions',
        'pulp_paper': 'Pulp and paper mills - biomass and fossil fuel emissions',
        'fertilizer_plant': 'Fertilizer manufacturing - ammonia production emissions'
    }
    return descriptions.get(industry_type, 'Industrial facility with CO2 emissions')
