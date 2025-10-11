import re
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from services.indian_weather_service import indian_weather_service
from services.carbon_calculator import CarbonFootprintCalculator
import logging

logger = logging.getLogger(__name__)

class ClimateBot:
    def __init__(self):
        self.name = "EcoBot"
        self.version = "1.0.0"
        self.carbon_calculator = CarbonFootprintCalculator()
        self.conversation_history = {}
        self.initialize_responses()
    
    def initialize_responses(self):
        """Initialize predefined responses and patterns"""
        self.greetings = [
            "Hello! I'm EcoBot, your climate assistant. How can I help you with climate data, carbon footprint, or eco-friendly tips today?",
            "Hi there! I'm here to help with all things climate and environment. What would you like to know?",
            "Welcome! I can help you understand climate data, reduce your carbon footprint, or find eco-friendly solutions. What interests you?",
            "Greetings! I'm your personal climate guide. Ask me about weather, sustainability, or environmental tips!"
        ]
        
        self.farewell_patterns = [
            r'\b(bye|goodbye|see you|farewell|quit|exit)\b',
            r'\b(thank you|thanks|thx)\b.*\b(bye|goodbye)\b',
            r'\b(that\'s all|nothing else|no more questions)\b'
        ]
        
        self.climate_patterns = {
            'weather_query': [
                r'\b(weather|temperature|humidity|rainfall|climate)\b.*\b(in|at|for)\b.*\b([A-Z][a-z]+)\b',
                r'\b(how is|what is|tell me about)\b.*\b(weather|climate)\b.*\b([A-Z][a-z]+)\b',
                r'\b([A-Z][a-z]+)\b.*\b(weather|temperature|rainfall|humidity)\b'
            ],
            'comparison': [
                r'\bcompare\b.*\b([A-Z][a-z]+)\b.*\b(and|vs|versus|with)\b.*\b([A-Z][a-z]+)\b',
                r'\b([A-Z][a-z]+)\b.*\b(vs|versus|compared to)\b.*\b([A-Z][a-z]+)\b'
            ],
            'carbon_footprint': [
                r'\b(carbon|footprint|emissions|co2)\b',
                r'\b(reduce|lower|decrease)\b.*\b(carbon|emissions|footprint)\b',
                r'\b(calculate|compute)\b.*\b(footprint|carbon|emissions)\b'
            ],
            'eco_shopping': [
                r'\b(eco|sustainable|green|organic)\b.*\b(products|shopping|buy)\b',
                r'\b(environmentally friendly|eco-friendly)\b',
                r'\bsustainable\b.*\b(alternatives|options)\b'
            ],
            'air_quality': [
                r'\b(air quality|pollution|aqi)\b',
                r'\b(clean air|air pollution)\b'
            ],
            'monsoon_season': [
                r'\b(monsoon|rainy season|rains)\b',
                r'\b(when does.*rain|rainfall season)\b'
            ],
            'seasonal': [
                r'\b(winter|summer|monsoon|post-monsoon)\b.*\b(season|weather)\b',
                r'\b(best time|when to visit)\b'
            ]
        }
        
        self.response_templates = {
            'greeting': self.greetings,
            'weather_info': [
                "Based on the latest data for {city}, the current temperature is {temp}°C with {humidity}% humidity. {additional_info}",
                "In {city}, it's currently {temp}°C. The humidity level is {humidity}% and recent rainfall is {rainfall}mm. {weather_advice}",
                "The weather in {city} shows {temp}°C temperature, {humidity}% humidity, and {rainfall}mm rainfall. {climate_insight}"
            ],
            'comparison': [
                "Comparing {city1} and {city2}: {city1} has {temp1}°C while {city2} has {temp2}°C. {comparison_insight}",
                "Weather comparison shows {city1} is {temp_diff}°C {'warmer' if '{temp_diff}' > '0' else 'cooler'} than {city2}. {additional_comparison}"
            ],
            'carbon_help': [
                "I can help you calculate and reduce your carbon footprint! Here are some quick tips: {carbon_tips}",
                "Your carbon footprint matters! Try these sustainable practices: {sustainability_tips}",
                "Let's work on reducing emissions together! {carbon_reduction_tips}"
            ],
            'eco_shopping': [
                "Great choice going eco-friendly! Here are some sustainable options: {eco_suggestions}",
                "I recommend these environmentally conscious products: {green_products}",
                "Sustainable living starts with conscious choices: {eco_tips}"
            ],
            'no_understand': [
                "I didn't quite understand that. Could you ask about climate data, carbon footprint, or eco-friendly tips?",
                "I'm specialized in climate and environmental topics. Try asking about weather, sustainability, or carbon emissions!",
                "Let me help with climate-related questions! Ask me about weather data, eco-shopping, or carbon footprint."
            ],
            'farewell': [
                "Goodbye! Keep making sustainable choices for our planet! 🌱",
                "Thanks for chatting! Remember, every small action helps the environment! 🌍",
                "See you soon! Stay climate-conscious! ♻️"
            ]
        }
        
        # Climate insights and tips
        self.climate_insights = {
            'hot_weather': "It's quite warm! Stay hydrated and consider using fans instead of AC when possible to reduce energy consumption.",
            'humid_weather': "High humidity can feel uncomfortable. Natural ventilation and light clothing can help you stay cool efficiently.",
            'rainy_weather': "Great for the environment! Rainwater harvesting is an excellent sustainable practice.",
            'winter_weather': "Perfect weather for outdoor activities! Walking or cycling instead of driving helps reduce emissions.",
            'dry_weather': "Low humidity weather. Consider water conservation and check air quality levels."
        }
        
        self.carbon_tips = [
            "Use public transport or carpool to reduce transportation emissions",
            "Switch to LED bulbs to cut energy consumption by up to 75%",
            "Eat more plant-based meals to lower your food-related carbon footprint",
            "Unplug electronics when not in use to prevent phantom energy drain",
            "Choose local and seasonal produce to reduce transportation emissions",
            "Use a programmable thermostat to optimize heating and cooling",
            "Walk or bike for short trips instead of driving",
            "Reduce, reuse, and recycle to minimize waste"
        ]
        
        self.eco_products = [
            "Bamboo toothbrushes and reusable water bottles",
            "Solar-powered chargers and energy-efficient appliances",
            "Organic cotton clothing and biodegradable cleaning products",
            "Compost bins and reusable shopping bags",
            "LED light bulbs and smart thermostats",
            "Electric or hybrid vehicles for sustainable transportation"
        ]
    
    def process_message(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """Process user message and generate appropriate response"""
        try:
            # Initialize conversation history for new users
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Add user message to history
            self.conversation_history[user_id].append({
                "role": "user",
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Clean and analyze message
            clean_message = message.lower().strip()
            response_data = self._generate_response(clean_message, user_id)
            
            # Add bot response to history
            self.conversation_history[user_id].append({
                "role": "bot",
                "message": response_data["message"],
                "timestamp": datetime.now().isoformat(),
                "intent": response_data.get("intent", "unknown")
            })
            
            return {
                "success": True,
                "response": response_data["message"],
                "intent": response_data.get("intent", "unknown"),
                "suggestions": response_data.get("suggestions", []),
                "data": response_data.get("data"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "success": False,
                "response": "I'm having trouble processing your request. Please try again!",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_response(self, message: str, user_id: str) -> Dict[str, Any]:
        """Generate response based on message analysis"""
        
        # Check for greetings
        if self._is_greeting(message):
            return {
                "message": random.choice(self.greetings),
                "intent": "greeting",
                "suggestions": [
                    "What's the weather like in Mumbai?",
                    "How can I reduce my carbon footprint?",
                    "Show me eco-friendly products",
                    "Compare climate data between cities"
                ]
            }
        
        # Check for farewells
        if self._is_farewell(message):
            return {
                "message": random.choice(self.response_templates['farewell']),
                "intent": "farewell"
            }
        
        # Analyze intent and generate response
        intent, entities = self._analyze_intent(message)
        
        if intent == "weather_query":
            return self._handle_weather_query(entities)
        elif intent == "comparison":
            return self._handle_comparison(entities)
        elif intent == "carbon_footprint":
            return self._handle_carbon_query(message)
        elif intent == "eco_shopping":
            return self._handle_eco_shopping(message)
        elif intent == "air_quality":
            return self._handle_air_quality_query(entities)
        elif intent == "seasonal":
            return self._handle_seasonal_query(message)
        else:
            return self._handle_fallback(message)
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'start', 'begin']
        return any(greeting in message for greeting in greetings)
    
    def _is_farewell(self, message: str) -> bool:
        """Check if message is a farewell"""
        return any(re.search(pattern, message, re.IGNORECASE) for pattern in self.farewell_patterns)
    
    def _analyze_intent(self, message: str) -> Tuple[str, Dict[str, Any]]:
        """Analyze message intent and extract entities"""
        entities = {}
        
        for intent, patterns in self.climate_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    if intent == "weather_query" and groups:
                        entities['city'] = groups[-1].title()  # Last group is usually the city
                    elif intent == "comparison" and len(groups) >= 2:
                        entities['city1'] = groups[0].title()
                        entities['city2'] = groups[-1].title()
                    return intent, entities
        
        return "unknown", entities
    
    def _handle_weather_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle weather-related queries"""
        city_name = entities.get('city', 'Delhi')  # Default to Delhi
        
        try:
            # Get weather data from Indian weather service
            if not indian_weather_service.processed_data:
                indian_weather_service.initialize()
            
            city_data = indian_weather_service.get_city_weather(city_name)
            
            if city_data:
                temp = city_data['current']['temperature']
                humidity = city_data['current']['humidity']
                rainfall = city_data['current']['rainfall']
                
                # Generate weather advice based on conditions
                weather_advice = self._get_weather_advice(temp, humidity, rainfall)
                
                response = random.choice(self.response_templates['weather_info']).format(
                    city=city_name,
                    temp=temp,
                    humidity=humidity,
                    rainfall=rainfall,
                    additional_info=f"Wind speed is {city_data['current']['wind_speed']} km/h.",
                    weather_advice=weather_advice,
                    climate_insight=self._get_climate_insight(temp, humidity, rainfall)
                )
                
                return {
                    "message": response,
                    "intent": "weather_query",
                    "data": city_data,
                    "suggestions": [
                        f"Compare {city_name} with another city",
                        "Show me air quality data",
                        "What's the carbon footprint of this weather?",
                        "Eco-friendly tips for this weather"
                    ]
                }
            else:
                return {
                    "message": f"I couldn't find weather data for {city_name}. Try asking about Mumbai, Delhi, Bangalore, or other major Indian cities!",
                    "intent": "weather_query",
                    "suggestions": ["Weather in Mumbai", "Delhi climate data", "Bangalore temperature"]
                }
                
        except Exception as e:
            logger.error(f"Error handling weather query: {e}")
            return {
                "message": f"I'm having trouble getting weather data for {city_name}. Please try again!",
                "intent": "weather_query"
            }
    
    def _handle_comparison(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle city comparison queries"""
        city1 = entities.get('city1', 'Mumbai')
        city2 = entities.get('city2', 'Delhi')
        
        try:
            if not indian_weather_service.processed_data:
                indian_weather_service.initialize()
            
            data1 = indian_weather_service.get_city_weather(city1)
            data2 = indian_weather_service.get_city_weather(city2)
            
            if data1 and data2:
                temp1 = data1['current']['temperature']
                temp2 = data2['current']['temperature']
                temp_diff = round(temp1 - temp2, 1)
                
                comparison_insight = self._get_comparison_insight(data1, data2)
                
                response = f"Comparing {city1} and {city2}: {city1} has {temp1}°C while {city2} has {temp2}°C. "
                if temp_diff > 0:
                    response += f"{city1} is {abs(temp_diff)}°C warmer than {city2}. "
                elif temp_diff < 0:
                    response += f"{city1} is {abs(temp_diff)}°C cooler than {city2}. "
                else:
                    response += "Both cities have similar temperatures! "
                
                response += comparison_insight
                
                return {
                    "message": response,
                    "intent": "comparison",
                    "data": {"city1": data1, "city2": data2},
                    "suggestions": [
                        "Show me more city comparisons",
                        "What about humidity differences?",
                        "Carbon footprint comparison",
                        "Best eco-practices for these climates"
                    ]
                }
            else:
                return {
                    "message": f"I couldn't find data for one or both cities. Try comparing major Indian cities like Mumbai, Delhi, Bangalore, Chennai, or Kolkata!",
                    "intent": "comparison"
                }
                
        except Exception as e:
            logger.error(f"Error handling comparison: {e}")
            return {
                "message": "I'm having trouble comparing those cities. Please try again!",
                "intent": "comparison"
            }
    
    def _handle_carbon_query(self, message: str) -> Dict[str, Any]:
        """Handle carbon footprint queries"""
        tips = random.sample(self.carbon_tips, 3)
        
        response = "Here are some effective ways to reduce your carbon footprint:\n\n"
        for i, tip in enumerate(tips, 1):
            response += f"{i}. {tip}\n"
        
        response += "\nWould you like me to calculate your carbon footprint based on specific activities?"
        
        return {
            "message": response,
            "intent": "carbon_footprint",
            "suggestions": [
                "Calculate my transportation footprint",
                "Energy consumption tips",
                "Eco-friendly transportation options",
                "Show me sustainable products"
            ]
        }
    
    def _handle_eco_shopping(self, message: str) -> Dict[str, Any]:
        """Handle eco-shopping queries"""
        products = random.sample(self.eco_products, 2)
        
        response = "Here are some eco-friendly product recommendations:\n\n"
        for product in products:
            response += f"• {product}\n"
        
        response += "\nThese products help reduce environmental impact while maintaining quality and functionality!"
        
        return {
            "message": response,
            "intent": "eco_shopping",
            "suggestions": [
                "More sustainable alternatives",
                "Carbon footprint of products",
                "Local eco-friendly stores",
                "DIY eco-friendly solutions"
            ]
        }
    
    def _handle_air_quality_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle air quality queries"""
        city = entities.get('city', 'Delhi')
        
        response = f"Air quality is crucial for health and climate! For {city}, I recommend:\n\n"
        response += "• Check AQI levels before outdoor activities\n"
        response += "• Use air purifiers indoors during high pollution days\n"
        response += "• Plant trees and support green spaces\n"
        response += "• Use public transport to reduce emissions\n"
        response += "• Avoid burning waste or firecrackers\n\n"
        response += "Would you like tips on improving air quality in your area?"
        
        return {
            "message": response,
            "intent": "air_quality",
            "suggestions": [
                "How to improve indoor air quality",
                "Best plants for air purification",
                "Transportation choices for clean air",
                "Carbon footprint and air quality"
            ]
        }
    
    def _handle_seasonal_query(self, message: str) -> Dict[str, Any]:
        """Handle seasonal weather queries"""
        current_month = datetime.now().month
        
        if 'monsoon' in message or 'rain' in message:
            response = "The Indian monsoon season (June-September) brings:\n\n"
            response += "• Southwest monsoon: June-September (main rainy season)\n"
            response += "• Northeast monsoon: October-December (affects Tamil Nadu, Kerala)\n"
            response += "• 70-80% of India's annual rainfall occurs during monsoon\n"
            response += "• Best time for water conservation and rainwater harvesting!\n\n"
            response += "Monsoons are crucial for agriculture and water resources."
        elif 'winter' in message:
            response = "Indian winter (December-February) features:\n\n"
            response += "• Cool, dry weather across most regions\n"
            response += "• Perfect for outdoor activities and reduced AC usage\n"
            response += "• Great time for solar energy generation\n"
            response += "• Ideal for tree plantation and gardening\n"
        elif 'summer' in message:
            response = "Indian summer (March-May) characteristics:\n\n"
            response += "• High temperatures, especially in northern plains\n"
            response += "• Increased energy consumption for cooling\n"
            response += "• Important to conserve water and energy\n"
            response += "• Best practices: natural cooling, efficient appliances\n"
        else:
            seasons = ['winter', 'summer', 'monsoon', 'post-monsoon']
            response = f"India has distinct seasons: {', '.join(seasons)}. Each season brings unique climate patterns and environmental considerations!"
        
        return {
            "message": response,
            "intent": "seasonal",
            "suggestions": [
                "Seasonal carbon footprint tips",
                "Best eco-practices for this season",
                "Weather patterns in my city",
                "Seasonal sustainable living"
            ]
        }
    
    def _handle_fallback(self, message: str) -> Dict[str, Any]:
        """Handle unknown queries with helpful suggestions"""
        response = random.choice(self.response_templates['no_understand'])
        
        return {
            "message": response,
            "intent": "fallback",
            "suggestions": [
                "What's the weather like in Mumbai?",
                "How can I reduce my carbon footprint?",
                "Show me eco-friendly products",
                "Compare Delhi and Bangalore climate",
                "Tell me about air quality",
                "Explain monsoon patterns"
            ]
        }
    
    def _get_weather_advice(self, temp: float, humidity: float, rainfall: float) -> str:
        """Generate weather-specific advice"""
        if temp > 35:
            return "Stay cool and hydrated! Consider using natural cooling methods."
        elif temp < 15:
            return "Bundle up! This is great weather for outdoor activities without AC."
        elif humidity > 80:
            return "High humidity - use fans and ensure good ventilation."
        elif rainfall > 10:
            return "Perfect for rainwater harvesting and enjoying the natural cooling!"
        else:
            return "Pleasant weather for eco-friendly outdoor activities!"
    
    def _get_climate_insight(self, temp: float, humidity: float, rainfall: float) -> str:
        """Generate climate insights"""
        if temp > 35 and humidity > 70:
            return self.climate_insights['humid_weather']
        elif temp > 35:
            return self.climate_insights['hot_weather']
        elif rainfall > 5:
            return self.climate_insights['rainy_weather']
        elif temp < 20:
            return self.climate_insights['winter_weather']
        elif humidity < 50:
            return self.climate_insights['dry_weather']
        else:
            return "Perfect weather for sustainable outdoor activities!"
    
    def _get_comparison_insight(self, data1: Dict, data2: Dict) -> str:
        """Generate insights from city comparison"""
        city1_humid = data1['current']['humidity']
        city2_humid = data2['current']['humidity']
        
        if abs(city1_humid - city2_humid) > 20:
            if city1_humid > city2_humid:
                return f"{data1['city']} is much more humid, which affects energy usage for cooling."
            else:
                return f"{data2['city']} is much more humid, requiring more energy for comfort."
        else:
            return "Both cities have similar humidity levels and climate patterns."
    
    def get_conversation_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        return self.conversation_history.get(user_id, [])
    
    def clear_conversation_history(self, user_id: str) -> bool:
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
            return True
        return False
    
    def get_bot_info(self) -> Dict[str, Any]:
        """Get bot information and capabilities"""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": [
                "Weather data for Indian cities",
                "Climate comparisons between cities",
                "Carbon footprint advice and calculations",
                "Eco-friendly product recommendations",
                "Air quality insights",
                "Seasonal climate patterns",
                "Sustainable living tips"
            ],
            "supported_cities": [
                "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", 
                "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Kochi"
            ],
            "sample_queries": [
                "What's the weather like in Mumbai?",
                "Compare climate between Delhi and Bangalore",
                "How can I reduce my carbon footprint?",
                "Show me eco-friendly products",
                "Tell me about monsoon season",
                "Air quality tips for Delhi"
            ]
        }

# Create global instance
climate_bot = ClimateBot()