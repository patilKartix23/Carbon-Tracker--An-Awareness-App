"""
Carbon Activity Service - Business logic for activity-based carbon tracking
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

class CarbonActivityService:
    """Service for handling carbon activity calculations and recommendations"""
    
    def __init__(self):
        self.activity_units = {
            'transport': 'km',
            'food': 'meals',
            'energy': 'kWh',
            'shopping': 'items'
        }
        
        self.activity_display_names = {
            'car': 'Car (Petrol/Diesel)',
            'bus': 'Bus/Public Transport',
            'train': 'Train',
            'flight': 'Flight',
            'motorcycle': 'Motorcycle',
            'bicycle': 'Bicycle',
            'walking': 'Walking',
            'beef': 'Beef Meal',
            'lamb': 'Lamb Meal',
            'pork': 'Pork Meal',
            'chicken': 'Chicken Meal',
            'fish': 'Fish Meal',
            'vegetarian': 'Vegetarian Meal',
            'vegan': 'Vegan Meal',
            'dairy': 'Dairy Products',
            'electricity': 'Electricity Usage',
            'gas': 'Natural Gas',
            'heating_oil': 'Heating Oil',
            'coal': 'Coal',
            'clothes': 'Clothing Item',
            'electronics': 'Electronics',
            'books': 'Books',
            'furniture': 'Furniture'
        }
    
    def get_unit_for_activity(self, activity: str, category: str) -> str:
        """Get the unit of measurement for an activity"""
        if category == 'transport':
            return 'km'
        elif category == 'food':
            return 'meals' if 'meal' in activity else 'servings'
        elif category == 'energy':
            return 'kWh'
        elif category == 'shopping':
            return 'items'
        return 'units'
    
    def get_display_name(self, activity: str) -> str:
        """Get human-readable display name for activity"""
        return self.activity_display_names.get(activity, activity.title())
    
    def get_examples(self, activity: str, category: str) -> List[str]:
        """Get example values for an activity"""
        examples = {
            'car': ['Daily commute: 20km', 'Weekend trip: 150km', 'Short trip: 5km'],
            'bus': ['Daily commute: 15km', 'City travel: 8km', 'Long distance: 200km'],
            'train': ['City metro: 10km', 'Intercity: 300km', 'Daily commute: 25km'],
            'flight': ['Domestic flight: 1000km', 'International: 8000km', 'Regional: 500km'],
            'bicycle': ['Daily commute: 10km', 'Exercise ride: 30km', 'Short trip: 3km'],
            'walking': ['Daily walk: 3km', 'Exercise: 5km', 'Short trip: 1km'],
            'beef': ['Lunch: 1 meal', 'Dinner: 1 meal', 'Weekly total: 7 meals'],
            'chicken': ['Lunch: 1 meal', 'Dinner: 1 meal', 'Weekly total: 5 meals'],
            'vegetarian': ['Lunch: 1 meal', 'Dinner: 1 meal', 'Daily total: 3 meals'],
            'vegan': ['Breakfast: 1 meal', 'Lunch: 1 meal', 'Dinner: 1 meal'],
            'electricity': ['Daily usage: 15 kWh', 'Monthly bill: 300 kWh', 'AC usage: 8 kWh'],
            'gas': ['Daily cooking: 2 kWh', 'Heating: 20 kWh', 'Water heating: 5 kWh'],
            'clothes': ['New shirt: 1 item', 'Jeans: 1 item', 'Shopping spree: 5 items'],
            'electronics': ['Smartphone: 1 item', 'Laptop: 1 item', 'TV: 1 item']
        }
        return examples.get(activity, [f'{activity}: 1 unit'])
    
    def get_impact_message(self, emissions: float, category: str) -> str:
        """Generate an impact message based on emissions"""
        if emissions < 0.5:
            return f"🌱 Great choice! Very low impact activity."
        elif emissions < 2.0:
            return f"🟢 Good choice! This activity has moderate impact."
        elif emissions < 5.0:
            return f"🟡 Consider alternatives - this has significant impact."
        else:
            return f"🔴 High impact activity - look for greener alternatives!"
    
    def get_personalized_suggestions(self, user_id: str, category: str = 'all') -> List[Dict]:
        """Get personalized suggestions for reducing carbon footprint"""
        
        base_suggestions = {
            'transport': [
                {
                    'title': 'Try Cycling',
                    'description': 'Replace short car trips with cycling',
                    'impact': 'Save 2-5 kg CO₂ per day',
                    'difficulty': 'Easy',
                    'category': 'transport',
                    'icon': '🚲'
                },
                {
                    'title': 'Use Public Transport',
                    'description': 'Take the bus or train instead of driving',
                    'impact': 'Save 3-8 kg CO₂ per day',
                    'difficulty': 'Easy',
                    'category': 'transport',
                    'icon': '🚌'
                },
                {
                    'title': 'Carpool or Rideshare',
                    'description': 'Share rides with colleagues or friends',
                    'impact': 'Save 2-4 kg CO₂ per trip',
                    'difficulty': 'Medium',
                    'category': 'transport',
                    'icon': '🚗'
                }
            ],
            'food': [
                {
                    'title': 'Meatless Monday',
                    'description': 'Try plant-based meals once a week',
                    'impact': 'Save 4-5 kg CO₂ per meal',
                    'difficulty': 'Easy',
                    'category': 'food',
                    'icon': '🥗'
                },
                {
                    'title': 'Choose Chicken over Beef',
                    'description': 'Swap beef meals for chicken or fish',
                    'impact': 'Save 3.5 kg CO₂ per meal',
                    'difficulty': 'Easy',
                    'category': 'food',
                    'icon': '🐔'
                },
                {
                    'title': 'Buy Local Produce',
                    'description': 'Choose locally grown fruits and vegetables',
                    'impact': 'Save 0.5-1 kg CO₂ per meal',
                    'difficulty': 'Easy',
                    'category': 'food',
                    'icon': '🥕'
                }
            ],
            'energy': [
                {
                    'title': 'Switch to LED Bulbs',
                    'description': 'Replace old bulbs with energy-efficient LEDs',
                    'impact': 'Save 2-3 kg CO₂ per month',
                    'difficulty': 'Easy',
                    'category': 'energy',
                    'icon': '💡'
                },
                {
                    'title': 'Unplug Electronics',
                    'description': 'Turn off devices when not in use',
                    'impact': 'Save 1-2 kg CO₂ per day',
                    'difficulty': 'Easy',
                    'category': 'energy',
                    'icon': '🔌'
                },
                {
                    'title': 'Adjust Thermostat',
                    'description': 'Set AC/heating 2°C closer to outside temperature',
                    'impact': 'Save 5-10 kg CO₂ per month',
                    'difficulty': 'Easy',
                    'category': 'energy',
                    'icon': '🌡️'
                }
            ],
            'shopping': [
                {
                    'title': 'Buy Second-hand',
                    'description': 'Choose pre-owned clothes and electronics',
                    'impact': 'Save 10-50 kg CO₂ per item',
                    'difficulty': 'Easy',
                    'category': 'shopping',
                    'icon': '♻️'
                },
                {
                    'title': 'Quality over Quantity',
                    'description': 'Buy fewer, higher-quality items that last longer',
                    'impact': 'Save 20-100 kg CO₂ per year',
                    'difficulty': 'Medium',
                    'category': 'shopping',
                    'icon': '⭐'
                }
            ]
        }
        
        if category == 'all':
            suggestions = []
            for cat_suggestions in base_suggestions.values():
                suggestions.extend(cat_suggestions)
            # Return random selection of 5 suggestions
            return random.sample(suggestions, min(5, len(suggestions)))
        else:
            return base_suggestions.get(category, [])
    
    def calculate_weekly_progress(self, user_activities: List[Dict]) -> Dict:
        """Calculate weekly progress and insights"""
        if not user_activities:
            return {
                'total_emissions': 0,
                'daily_average': 0,
                'trend': 'no_data',
                'insights': ['Start logging activities to see your progress!']
            }
        
        # Group activities by day
        daily_totals = {}
        category_totals = {'transport': 0, 'food': 0, 'energy': 0, 'shopping': 0}
        
        for activity in user_activities:
            date = activity['date'].date() if isinstance(activity['date'], datetime) else activity['date']
            emissions = activity.get('emissions_kg_co2', 0)
            category = activity.get('category', 'other')
            
            if date not in daily_totals:
                daily_totals[date] = 0
            daily_totals[date] += emissions
            
            if category in category_totals:
                category_totals[category] += emissions
        
        # Calculate metrics
        total_emissions = sum(daily_totals.values())
        daily_average = total_emissions / len(daily_totals) if daily_totals else 0
        
        # Determine trend (simplified)
        dates = sorted(daily_totals.keys())
        if len(dates) >= 3:
            recent_avg = sum(daily_totals[d] for d in dates[-3:]) / 3
            older_avg = sum(daily_totals[d] for d in dates[:-3]) / max(1, len(dates) - 3)
            
            if recent_avg < older_avg * 0.9:
                trend = 'improving'
            elif recent_avg > older_avg * 1.1:
                trend = 'worsening'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        # Generate insights
        insights = []
        highest_category = max(category_totals, key=category_totals.get)
        if category_totals[highest_category] > 0:
            insights.append(f"Your highest emissions come from {highest_category}")
        
        if daily_average < 8.0:
            insights.append("You're below the global average - keep it up!")
        elif daily_average > 15.0:
            insights.append("There's room for improvement - try our suggestions!")
        
        return {
            'total_emissions': round(total_emissions, 2),
            'daily_average': round(daily_average, 2),
            'trend': trend,
            'category_breakdown': category_totals,
            'insights': insights,
            'days_logged': len(daily_totals)
        }
    
    def get_achievement_badges(self, user_stats: Dict) -> List[Dict]:
        """Generate achievement badges based on user behavior"""
        badges = []
        
        total_emissions = user_stats.get('total_emissions', 0)
        days_logged = user_stats.get('days_logged', 0)
        
        # Logging badges
        if days_logged >= 7:
            badges.append({
                'name': 'Week Warrior',
                'description': 'Logged activities for 7 days',
                'icon': '📅',
                'earned': True
            })
        
        if days_logged >= 30:
            badges.append({
                'name': 'Monthly Master',
                'description': 'Logged activities for 30 days',
                'icon': '🗓️',
                'earned': True
            })
        
        # Low emission badges
        daily_avg = user_stats.get('daily_average', 0)
        if daily_avg < 5.0 and days_logged >= 3:
            badges.append({
                'name': 'Eco Champion',
                'description': 'Maintained low daily emissions',
                'icon': '🌍',
                'earned': True
            })
        
        # Improvement badges
        if user_stats.get('trend') == 'improving':
            badges.append({
                'name': 'Progress Pioneer',
                'description': 'Reduced emissions over time',
                'icon': '📉',
                'earned': True
            })
        
        return badges
