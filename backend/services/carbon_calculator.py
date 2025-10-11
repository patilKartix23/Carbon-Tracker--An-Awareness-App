from typing import Dict, List
import numpy as np
from datetime import datetime

class CarbonFootprintCalculator:
    def __init__(self):
        # Emission factors (kg CO2 equivalent)
        self.emission_factors = {
            'transportation': {
                'car_gasoline': 0.404,  # kg CO2 per mile
                'car_diesel': 0.411,    # kg CO2 per mile
                'car_electric': 0.124,  # kg CO2 per mile (varies by grid)
                'bus': 0.089,          # kg CO2 per mile
                'train': 0.041,        # kg CO2 per mile
                'plane_domestic': 0.255, # kg CO2 per mile
                'plane_international': 0.195, # kg CO2 per mile
                'motorcycle': 0.212,   # kg CO2 per mile
                'bicycle': 0.0,        # kg CO2 per mile
                'walking': 0.0         # kg CO2 per mile
            },
            'energy': {
                'electricity_grid': 0.417,  # kg CO2 per kWh (US average)
                'natural_gas': 0.181,       # kg CO2 per kWh
                'heating_oil': 0.264,       # kg CO2 per kWh
                'propane': 0.215,          # kg CO2 per kWh
                'solar': 0.041,            # kg CO2 per kWh
                'wind': 0.011,             # kg CO2 per kWh
                'nuclear': 0.012           # kg CO2 per kWh
            },
            'consumption': {
                'lamb': 24.0,              # kg CO2 per kg
                'cheese': 21.0,            # kg CO2 per kg
                'pork': 12.1,              # kg CO2 per kg
                'chicken': 6.9,            # kg CO2 per kg
                'fish': 6.1,               # kg CO2 per kg
                'eggs': 4.2,               # kg CO2 per kg
                'rice': 4.0,               # kg CO2 per kg
                'milk': 3.2,               # kg CO2 per liter
                'vegetables': 2.0,         # kg CO2 per kg
                'fruits': 1.1,             # kg CO2 per kg
                'grains': 1.4              # kg CO2 per kg
            }
        }
    
    def calculate_transportation_footprint(self, transportation_data: Dict) -> Dict:
        """Calculate CO2 emissions from transportation"""
        total_emissions = 0.0
        breakdown = {}
        
        for transport_type, distance in transportation_data.items():
            if transport_type in self.emission_factors['transportation']:
                emissions = distance * self.emission_factors['transportation'][transport_type]
                total_emissions += emissions
                breakdown[transport_type] = round(emissions, 3)
        
        return {
            'total_kg_co2': round(total_emissions, 3),
            'breakdown': breakdown
        }
    
    def calculate_energy_footprint(self, energy_data: Dict) -> Dict:
        """Calculate CO2 emissions from energy consumption"""
        total_emissions = 0.0
        breakdown = {}
        
        for energy_type, consumption in energy_data.items():
            if energy_type in self.emission_factors['energy']:
                emissions = consumption * self.emission_factors['energy'][energy_type]
                total_emissions += emissions
                breakdown[energy_type] = round(emissions, 3)
        
        return {
            'total_kg_co2': round(total_emissions, 3),
            'breakdown': breakdown
        }
    
    def calculate_consumption_footprint(self, consumption_data: Dict) -> Dict:
        """Calculate CO2 emissions from food/product consumption"""
        total_emissions = 0.0
        breakdown = {}
        
        for item_type, amount in consumption_data.items():
            if item_type in self.emission_factors['consumption']:
                emissions = amount * self.emission_factors['consumption'][item_type]
                total_emissions += emissions
                breakdown[item_type] = round(emissions, 3)
        
        return {
            'total_kg_co2': round(total_emissions, 3),
            'breakdown': breakdown
        }
    
    def calculate_total_footprint(self, user_data: Dict) -> Dict:
        """Calculate total carbon footprint from all sources"""
        transportation = self.calculate_transportation_footprint(
            user_data.get('transportation', {})
        )
        energy = self.calculate_energy_footprint(
            user_data.get('energy', {})
        )
        consumption = self.calculate_consumption_footprint(
            user_data.get('consumption', {})
        )
        
        total_emissions = (
            transportation['total_kg_co2'] + 
            energy['total_kg_co2'] + 
            consumption['total_kg_co2']
        )
        
        return {
            'daily_footprint_kg_co2': round(total_emissions, 3),
            'daily_footprint_lbs_co2': round(total_emissions * 2.20462, 3),
            'annual_estimate_kg_co2': round(total_emissions * 365, 1),
            'annual_estimate_tons_co2': round(total_emissions * 365 / 1000, 2),
            'breakdown': {
                'transportation': transportation,
                'energy': energy,
                'consumption': consumption
            }
        }
    
    def get_personalized_recommendations(self, footprint_data: Dict, user_location: Dict = None) -> List[str]:
        """Generate personalized recommendations based on footprint analysis"""
        recommendations = []
        breakdown = footprint_data.get('breakdown', {})
        
        # Transportation recommendations
        transport_emissions = breakdown.get('transportation', {}).get('total_kg_co2', 0)
        if transport_emissions > 5.0:  # High transportation emissions
            recommendations.extend([
                "Consider carpooling or using public transportation for daily commutes",
                "Try walking or cycling for short trips under 2 miles",
                "Consider switching to an electric or hybrid vehicle",
                "Combine multiple errands into one trip to reduce overall driving"
            ])
        elif transport_emissions > 2.0:
            recommendations.extend([
                "Great job! Consider further reducing by walking or cycling occasionally",
                "Look into electric vehicle options for your next car purchase"
            ])
        
        # Energy recommendations
        energy_emissions = breakdown.get('energy', {}).get('total_kg_co2', 0)
        if energy_emissions > 8.0:  # High energy emissions
            recommendations.extend([
                "Switch to LED light bulbs to reduce electricity consumption",
                "Consider installing programmable thermostats",
                "Look into solar panel installation or green energy plans",
                "Improve home insulation to reduce heating/cooling needs",
                "Unplug electronics when not in use"
            ])
        elif energy_emissions > 4.0:
            recommendations.extend([
                "Consider upgrading to energy-efficient appliances",
                "Look into renewable energy options in your area"
            ])
        
        # Consumption recommendations
        consumption_emissions = breakdown.get('consumption', {}).get('total_kg_co2', 0)
        if consumption_emissions > 10.0:  # High consumption emissions
            recommendations.extend([
                "Try reducing meat consumption, especially lamb",
                "Choose locally-sourced and seasonal produce",
                "Consider plant-based alternatives for some meals",
                "Reduce food waste by meal planning"
            ])
        elif consumption_emissions > 5.0:
            recommendations.extend([
                "Great progress! Try 'Meatless Monday' or other plant-based days",
                "Look for organic and locally-sourced options when possible"
            ])
        
        # General recommendations
        total_daily = footprint_data.get('daily_footprint_kg_co2', 0)
        if total_daily < 8.0:  # Low emissions
            recommendations.append("Excellent! You're below the global average. Keep it up!")
        elif total_daily > 20.0:  # High emissions
            recommendations.extend([
                "Consider setting monthly carbon reduction goals",
                "Track your progress weekly to see improvements",
                "Look into carbon offset programs for unavoidable emissions"
            ])
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def compare_to_averages(self, daily_footprint: float) -> Dict:
        """Compare user's footprint to global and national averages"""
        # Average daily emissions (kg CO2)
        global_average_daily = 10.96  # 4 tons per year
        us_average_daily = 43.84      # 16 tons per year
        eu_average_daily = 19.18      # 7 tons per year
        target_daily = 5.48           # 2 tons per year (Paris Agreement target)
        
        return {
            'user_daily_kg_co2': daily_footprint,
            'comparison': {
                'vs_global_average': {
                    'difference_kg': round(daily_footprint - global_average_daily, 2),
                    'percentage': round((daily_footprint / global_average_daily - 1) * 100, 1)
                },
                'vs_us_average': {
                    'difference_kg': round(daily_footprint - us_average_daily, 2),
                    'percentage': round((daily_footprint / us_average_daily - 1) * 100, 1)
                },
                'vs_paris_target': {
                    'difference_kg': round(daily_footprint - target_daily, 2),
                    'percentage': round((daily_footprint / target_daily - 1) * 100, 1)
                }
            },
            'averages': {
                'global_daily_kg': global_average_daily,
                'us_daily_kg': us_average_daily,
                'eu_daily_kg': eu_average_daily,
                'paris_target_daily_kg': target_daily
            }
        }
