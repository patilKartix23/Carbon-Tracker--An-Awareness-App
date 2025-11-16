"""
CCUS (Carbon Capture, Utilization and Storage) API Routes
Handles carbon capture simulation, storage mapping, and utilization pathways
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
import math

router = APIRouter()
ccus_bp = router  # Alias for compatibility

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
            'fertilizer_plant': 0.89,
            'petrochemical_plant': 0.86,
            'glass_manufacturing': 0.83,
            'sugar_mill': 0.72,
            'textile_industry': 0.68,
            'pharmaceutical_plant': 0.78,
            'food_processing': 0.70,
            'brewery_distillery': 0.95,
            'hydrogen_production': 0.92,
            'lng_terminal': 0.84,
            'iron_smelting': 0.83,
            'copper_smelting': 0.81,
            'zinc_smelting': 0.80,
            'ceramic_tiles': 0.85,
            'lime_production': 0.88,
            'ethanol_plant': 0.93,
            'methanol_production': 0.91,
            # New industries added for better coverage
            'solar_panel_manufacturing': 0.76,
            'battery_manufacturing': 0.82,
            'semiconductor_fabrication': 0.79,
            'automotive_manufacturing': 0.74,
            'rubber_processing': 0.71,
            'cement_grinding_unit': 0.88,
            'coal_washery': 0.69,
            'thermal_coal_plant': 0.89,
            'waste_incineration': 0.87,
            'paper_recycling': 0.73,
            'plastic_manufacturing': 0.81,
            'paint_coating_industry': 0.77,
            'aerospace_manufacturing': 0.75,
            'shipbuilding_industry': 0.78,
            'data_center': 0.65,
            # Additional emerging industries
            'biofuel_production': 0.94,
            'green_hydrogen_plant': 0.96,
            'carbon_black_manufacturing': 0.89,
            'magnesium_production': 0.84,
            'nickel_refining': 0.83,
            'cobalt_processing': 0.80,
            'lithium_processing': 0.78,
            'rare_earth_mining': 0.73,
            'wind_turbine_manufacturing': 0.72,
            'electric_vehicle_battery': 0.85,
            'synthetic_diamond_production': 0.91,
            'graphene_manufacturing': 0.87,
            'carbon_nanotube_production': 0.90,
            'bio_plastic_manufacturing': 0.86,
            'algae_cultivation': 0.98
        }
        
        # Storage capacity estimates for different geological formations (MT CO2)
        # Based on NITI Aayog and TERI research estimates for India
        self.storage_sites_india = {
            'Gujarat': {
                'depleted_oil_wells': 2800,
                'saline_aquifers': 9500,
                'coal_seams': 550,
                'total_capacity': 12850,
                'active_projects': ['ONGC CCS Project at Hazira', 'Gujarat State Petroleum CCS Initiative'],
                'description': 'Largest CCUS potential state with extensive oil fields and saline aquifers'
            },
            'Rajasthan': {
                'depleted_oil_wells': 2200,
                'saline_aquifers': 6800,
                'coal_seams': 100,
                'total_capacity': 9100,
                'active_projects': ['Barmer Basin CCS Study'],
                'description': 'Significant oil and gas fields suitable for CO2 storage'
            },
            'Jharkhand': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 3800,
                'coal_seams': 2400,
                'total_capacity': 6200,
                'active_projects': ['Coal India CCUS Pilot Project'],
                'description': 'Major coal-bearing state with enhanced coal bed methane potential'
            },
            'Assam': {
                'depleted_oil_wells': 1200,
                'saline_aquifers': 3200,
                'coal_seams': 450,
                'total_capacity': 4850,
                'active_projects': ['Oil India CCS Research Project'],
                'description': 'Oil-producing state with mature fields for CO2-EOR'
            },
            'Odisha': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 5200,
                'coal_seams': 2200,
                'total_capacity': 7400,
                'active_projects': ['Talcher Fertilizer CCUS Pilot'],
                'description': 'Industrial hub with multiple cement and steel plants'
            },
            'Maharashtra': {
                'depleted_oil_wells': 550,
                'saline_aquifers': 3800,
                'coal_seams': 850,
                'total_capacity': 5200,
                'active_projects': ['Tata Steel CCUS Initiative at Jamshedpur'],
                'description': 'Industrial powerhouse with cement, steel, and chemical industries'
            },
            'Tamil Nadu': {
                'depleted_oil_wells': 300,
                'saline_aquifers': 2800,
                'coal_seams': 0,
                'total_capacity': 3100,
                'active_projects': ['Chennai Petroleum CO2 Capture Study'],
                'description': 'Major refining and chemical manufacturing state'
            },
            'West Bengal': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 2400,
                'coal_seams': 1800,
                'total_capacity': 4200,
                'active_projects': ['Durgapur Steel Plant CCS Feasibility Study'],
                'description': 'Industrial state with coal mining and steel production'
            },
            'Andhra Pradesh': {
                'depleted_oil_wells': 400,
                'saline_aquifers': 3600,
                'coal_seams': 600,
                'total_capacity': 4600,
                'active_projects': ['Krishna-Godavari Basin CCS Study'],
                'description': 'Coastal state with Krishna-Godavari basin potential'
            },
            'Madhya Pradesh': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 2200,
                'coal_seams': 1400,
                'total_capacity': 3600,
                'active_projects': ['UltraTech Cement CO2 Utilization Project'],
                'description': 'Central India with cement and power generation industries'
            },
            'Chhattisgarh': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 1800,
                'coal_seams': 1600,
                'total_capacity': 3400,
                'active_projects': ['NTPC CCS Pilot at Korba'],
                'description': 'Coal-rich state with thermal power plants'
            },
            'Karnataka': {
                'depleted_oil_wells': 0,
                'saline_aquifers': 2600,
                'coal_seams': 300,
                'total_capacity': 2900,
                'active_projects': ['JSW Steel Carbon Capture Initiative'],
                'description': 'Growing industrial state with steel and IT sectors'
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
        
        # Carbon credit pricing (INR per tonne CO2) - Updated to 2024 Indian market rates
        self.carbon_credit_price = {
            'voluntary_market': 1500,  # INR per tonne (voluntary carbon market)
            'compliance_market': 2800,  # INR per tonne (PAT scheme, emissions trading)
            'government_incentive': 2200  # INR per tonne (PLI scheme, green hydrogen mission)
        }
        
        # Real CCUS projects and initiatives in India
        self.india_ccus_projects = [
            {
                'name': 'ONGC CCS Pilot Project',
                'location': 'Hazira, Gujarat',
                'industry': 'Oil & Gas',
                'capacity_tpa': 60000,
                'status': 'Operational',
                'technology': 'Post-combustion capture + CO2-EOR',
                'start_year': 2020,
                'partner': 'ONGC Energy Centre'
            },
            {
                'name': 'Tata Steel Carbon Capture Initiative',
                'location': 'Jamshedpur, Jharkhand',
                'industry': 'Steel',
                'capacity_tpa': 40000,
                'status': 'Pilot Phase',
                'technology': 'Blast furnace gas CO2 capture',
                'start_year': 2023,
                'partner': 'IIT Delhi, CSIR-NCL'
            },
            {
                'name': 'UltraTech Cement CO2 Utilization',
                'location': 'Hirmi, Chhattisgarh',
                'industry': 'Cement',
                'capacity_tpa': 30000,
                'status': 'Under Construction',
                'technology': 'CO2 mineralization for building materials',
                'start_year': 2024,
                'partner': 'Carbon Clean Solutions'
            },
            {
                'name': 'NTPC CCS Demonstration Plant',
                'location': 'Vindhyachal, Madhya Pradesh',
                'industry': 'Power Generation',
                'capacity_tpa': 50000,
                'status': 'Feasibility Study',
                'technology': 'Post-combustion MEA capture',
                'start_year': 2025,
                'partner': 'BHEL, NTPC'
            },
            {
                'name': 'Indian Oil R&D Centre CCS Lab',
                'location': 'Faridabad, Haryana',
                'industry': 'Oil Refining',
                'capacity_tpa': 10000,
                'status': 'Research Phase',
                'technology': 'Various capture technologies',
                'start_year': 2022,
                'partner': 'IIT Bombay, CSIR'
            },
            {
                'name': 'Reliance CCUS at Jamnagar Refinery',
                'location': 'Jamnagar, Gujarat',
                'industry': 'Oil Refining',
                'capacity_tpa': 80000,
                'status': 'Planning Phase',
                'technology': 'Integrated CCS for refinery complex',
                'start_year': 2026,
                'partner': 'Reliance Industries Ltd'
            },
            {
                'name': 'JSW Steel CCUS Project',
                'location': 'Vijayanagar, Karnataka',
                'industry': 'Steel',
                'capacity_tpa': 35000,
                'status': 'Feasibility Study',
                'technology': 'Top gas CO2 capture',
                'start_year': 2025,
                'partner': 'JSW Steel, IIT Madras'
            },
            {
                'name': 'GAIL Green Hydrogen and CCUS',
                'location': 'Multiple locations',
                'industry': 'Natural Gas',
                'capacity_tpa': 45000,
                'status': 'Planning Phase',
                'technology': 'Blue hydrogen with CCS',
                'start_year': 2025,
                'partner': 'GAIL India Ltd'
            }
        ]

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

# Pydantic models for request/response validation
class CCUSCaptureRequest(BaseModel):
    industry_type: str
    annual_emissions_tonnes: float

class CCUSStorageRequest(BaseModel):
    co2_tonnes: float
    state: Optional[str] = None

class CCUSUtilizationRequest(BaseModel):
    co2_tonnes: float

class CCUSCarbonCreditRequest(BaseModel):
    stored_co2_tonnes: float
    credit_type: Optional[str] = "voluntary_market"

class CCUSComprehensiveRequest(BaseModel):
    industry_type: str
    annual_emissions_tonnes: float
    state: Optional[str] = None
    credit_type: Optional[str] = "voluntary_market"

@router.post('/capture-simulation')
def simulate_carbon_capture(request: CCUSCaptureRequest):
    """Simulate carbon capture for industrial emissions"""
    try:
        capture_result = ccus_simulator.calculate_capture_potential(
            request.industry_type, 
            request.annual_emissions_tonnes
        )
        
        if 'error' in capture_result:
            raise HTTPException(status_code=400, detail=capture_result['error'])
        
        return {
            'success': True,
            'capture_simulation': capture_result,
            'available_industries': list(ccus_simulator.capture_efficiency.keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/storage-sites')
def get_storage_sites(request: CCUSStorageRequest):
    """Get suitable storage sites for captured CO2"""
    try:
        storage_suggestions = ccus_simulator.suggest_storage_sites(
            request.co2_tonnes, 
            request.state
        )
        
        return {
            'success': True,
            'co2_amount_tonnes': request.co2_tonnes,
            'storage_suggestions': storage_suggestions,
            'total_sites_available': len(storage_suggestions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/utilization-pathways')
def get_utilization_pathways(request: CCUSUtilizationRequest):
    """Get CO2 utilization pathways and potential"""
    try:
        utilization_pathways = ccus_simulator.calculate_utilization_potential(request.co2_tonnes)
        
        return {
            'success': True,
            'co2_amount_tonnes': request.co2_tonnes,
            'utilization_pathways': utilization_pathways,
            'recommended_pathways': [p for p in utilization_pathways if p['recommended']]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/carbon-credits')
def calculate_carbon_credits(request: CCUSCarbonCreditRequest):
    """Calculate carbon credit value for stored CO2"""
    try:
        credit_calculation = ccus_simulator.calculate_carbon_credits(
            request.stored_co2_tonnes, 
            request.credit_type
        )
        
        return {
            'success': True,
            'carbon_credits': credit_calculation,
            'available_credit_types': list(ccus_simulator.carbon_credit_price.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/comprehensive-analysis')
def comprehensive_ccus_analysis(request: CCUSComprehensiveRequest):
    """Comprehensive CCUS analysis including capture, storage, utilization, and credits"""
    try:
        if not request.industry_type or request.annual_emissions_tonnes <= 0:
            raise HTTPException(status_code=400, detail='Valid industry_type and annual_emissions_tonnes required')
        
        # 1. Calculate capture potential
        capture_result = ccus_simulator.calculate_capture_potential(
            request.industry_type, 
            request.annual_emissions_tonnes
        )
        if 'error' in capture_result:
            raise HTTPException(status_code=400, detail=capture_result['error'])
        
        capturable_co2 = capture_result['capturable_co2_tonnes']
        
        # 2. Get storage suggestions
        storage_suggestions = ccus_simulator.suggest_storage_sites(capturable_co2, request.state)
        
        # 3. Get utilization pathways
        utilization_pathways = ccus_simulator.calculate_utilization_potential(capturable_co2)
        
        # 4. Calculate carbon credits
        credit_calculation = ccus_simulator.calculate_carbon_credits(capturable_co2, request.credit_type)
        
        # 5. Generate recommendations
        recommendations = generate_ccus_recommendations(capture_result, storage_suggestions, utilization_pathways, credit_calculation)
        
        return {
            'success': True,
            'input_data': {
                'industry_type': request.industry_type,
                'annual_emissions_tonnes': request.annual_emissions_tonnes,
                'state': request.state,
                'credit_type': request.credit_type
            },
            'capture_analysis': capture_result,
            'storage_options': storage_suggestions[:3],  # Top 3 recommendations
            'utilization_options': utilization_pathways[:5],  # Top 5 pathways
            'carbon_credits': credit_calculation,
            'recommendations': recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get('/india-storage-overview')
def get_india_storage_overview():
    """Get overview of CCUS storage potential across India"""
    try:
        total_capacity = sum(site['total_capacity'] for site in ccus_simulator.storage_sites_india.values())
        
        return {
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
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/industry-types')
def get_supported_industries():
    """Get list of supported industry types for CCUS"""
    return {
        'success': True,
        'supported_industries': [
            {
                'industry_type': industry,
                'capture_efficiency_percent': round(efficiency * 100, 1),
                'description': get_industry_description(industry)
            }
            for industry, efficiency in ccus_simulator.capture_efficiency.items()
        ]
    }

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
        'fertilizer_plant': 'Fertilizer manufacturing - ammonia production emissions',
        'petrochemical_plant': 'Petrochemical facilities - ethylene, propylene, and polymer production',
        'glass_manufacturing': 'Glass and bottle manufacturing - high temperature melting furnaces',
        'sugar_mill': 'Sugar mills and refineries - bagasse boilers and fermentation',
        'textile_industry': 'Textile and garment manufacturing - dyeing and processing emissions',
        'pharmaceutical_plant': 'Pharmaceutical manufacturing - chemical synthesis and processing',
        'food_processing': 'Food processing plants - cooking, drying, and refrigeration',
        'brewery_distillery': 'Breweries and distilleries - excellent capture from fermentation CO2',
        'hydrogen_production': 'Hydrogen production facilities - steam methane reforming emissions',
        'lng_terminal': 'LNG terminals and regasification - boil-off gas emissions',
        'iron_smelting': 'Iron ore smelting - blast furnace and direct reduction emissions',
        'copper_smelting': 'Copper smelting and refining - pyrometallurgical process emissions',
        'zinc_smelting': 'Zinc smelting facilities - roasting and sintering emissions',
        'ceramic_tiles': 'Ceramic and tile manufacturing - kiln firing emissions',
        'lime_production': 'Lime and quicklime production - limestone decomposition',
        'ethanol_plant': 'Ethanol and biofuel production - high-purity fermentation CO2',
        'methanol_production': 'Methanol synthesis plants - syngas conversion emissions',
        # New industry descriptions
        'solar_panel_manufacturing': 'Solar panel production - silicon purification and cell manufacturing',
        'battery_manufacturing': 'Battery and energy storage manufacturing - lithium processing and assembly',
        'semiconductor_fabrication': 'Semiconductor and chip manufacturing - high-tech clean room facilities',
        'automotive_manufacturing': 'Vehicle and auto parts manufacturing - assembly and painting operations',
        'rubber_processing': 'Rubber and tire manufacturing - vulcanization and compounding processes',
        'cement_grinding_unit': 'Cement grinding and packaging units - final processing facilities',
        'coal_washery': 'Coal washing and beneficiation plants - coal preparation facilities',
        'thermal_coal_plant': 'Thermal power stations - coal-fired electricity generation',
        'waste_incineration': 'Waste-to-energy and incineration plants - municipal solid waste processing',
        'paper_recycling': 'Paper recycling and de-inking mills - secondary fiber processing',
        'plastic_manufacturing': 'Plastic and polymer manufacturing - petrochemical derivatives',
        'paint_coating_industry': 'Paint, coatings, and adhesives manufacturing - solvent-based processes',
        'aerospace_manufacturing': 'Aircraft and aerospace components manufacturing - precision manufacturing',
        'shipbuilding_industry': 'Shipbuilding and marine equipment manufacturing - heavy industrial operations',
        'data_center': 'Data centers and server farms - cooling and backup power emissions',
        'biofuel_production': 'Advanced biofuel and renewable fuel production - biomass conversion',
        'green_hydrogen_plant': 'Green hydrogen production via electrolysis - renewable energy powered',
        'carbon_black_manufacturing': 'Carbon black and industrial carbon production - tire and rubber additives',
        'magnesium_production': 'Magnesium smelting and refining - lightweight metal production',
        'nickel_refining': 'Nickel extraction and refining - battery and stainless steel materials',
        'cobalt_processing': 'Cobalt processing and refining - battery and superalloy materials',
        'lithium_processing': 'Lithium extraction and processing - electric vehicle battery materials',
        'rare_earth_mining': 'Rare earth element mining and processing - high-tech component materials',
        'wind_turbine_manufacturing': 'Wind turbine and renewable energy equipment manufacturing',
        'electric_vehicle_battery': 'EV battery pack assembly and electric drivetrain manufacturing',
        'synthetic_diamond_production': 'Industrial and synthetic diamond manufacturing - high pressure processes',
        'graphene_manufacturing': 'Advanced carbon materials and graphene production - next-gen materials',
        'carbon_nanotube_production': 'Carbon nanotube and advanced carbon fiber manufacturing',
        'bio_plastic_manufacturing': 'Biodegradable and bio-based plastic production - sustainable polymers',
        'algae_cultivation': 'Large-scale algae cultivation for biofuels and biomaterials - CO2 feedstock'
    }
    return descriptions.get(industry_type, 'Industrial facility with CO2 emissions')

@router.get('/india-projects')
def get_india_ccus_projects():
    """Get list of real CCUS projects and initiatives in India"""
    try:
        return {
            'success': True,
            'total_projects': len(ccus_simulator.india_ccus_projects),
            'projects': ccus_simulator.india_ccus_projects,
            'summary': {
                'operational': len([p for p in ccus_simulator.india_ccus_projects if p['status'] == 'Operational']),
                'pilot_phase': len([p for p in ccus_simulator.india_ccus_projects if p['status'] == 'Pilot Phase']),
                'under_construction': len([p for p in ccus_simulator.india_ccus_projects if p['status'] == 'Under Construction']),
                'planning': len([p for p in ccus_simulator.india_ccus_projects if p['status'] in ['Planning Phase', 'Feasibility Study']]),
                'total_capacity_tpa': sum(p['capacity_tpa'] for p in ccus_simulator.india_ccus_projects)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
