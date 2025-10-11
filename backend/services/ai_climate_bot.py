"""
AI-Powered Climate Chatbot using OpenRouter
Simple integration with fallback to rule-based responses
"""
import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AIClimateBot:
    def __init__(self):
        self.name = "EcoBot AI"
        self.version = "2.0.0"
        
        # OpenRouter Configuration - Direct Integration
        self.openrouter_api_key = "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"
        self.model = "google/gemini-2.0-flash-exp:free"
        
        # System prompt for AI - Optimized for Gemini 2.0 Flash
        self.system_prompt = """You are EcoBot, an intelligent climate and sustainability assistant powered by Gemini 2.0 Flash for India. 

Your role is to help users with:
- 🌡️ Weather and climate information for Indian cities
- 🌱 Carbon footprint calculations and reduction tips
- 🛒 Eco-friendly product recommendations
- 💨 Air quality insights and health advisories
- ♻️ Sustainable living practices and green solutions
- 🌍 Climate change awareness and environmental education

Guidelines:
- Be friendly, conversational, and highly helpful
- Focus on India-specific climate data, weather patterns, and environmental solutions
- Provide actionable, practical advice tailored to Indian context
- Use clear, simple language that everyone can understand
- Keep responses concise (under 200 words) but informative
- When asked about specific data, provide accurate information or guide users to features
- Show empathy and encourage sustainable lifestyle choices
- Use emojis sparingly to make responses engaging

Remember: You're helping Indians make climate-conscious decisions in their daily lives!"""
    
    def process_message(self, message: str, user_id: str = "default", use_ai: bool = True) -> Dict[str, Any]:
        """Process user message using AI if available"""
        
        if use_ai and self.openrouter_api_key:
            try:
                response = self._call_openrouter_api(message)
                return {
                    "success": True,
                    "response": response,
                    "intent": self._detect_intent(message),
                    "suggestions": self._generate_suggestions(message),
                    "ai_powered": True,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"AI API error: {e}")
                # Fallback to simple response
                return self._simple_response(message)
        else:
            return self._simple_response(message)
    
    def _call_openrouter_api(self, message: str) -> str:
        """Call OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"API error: {response.status_code}")
    
    def _simple_response(self, message: str) -> Dict[str, Any]:
        """Simple fallback response"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm EcoBot, your climate assistant. Ask me about weather, sustainability, or carbon footprint!"
        elif 'weather' in message_lower or 'climate' in message_lower:
            response = "I can help with weather and climate data! Ask about specific cities like Mumbai, Delhi, or Bangalore."
        elif 'carbon' in message_lower or 'footprint' in message_lower:
            response = "To reduce your carbon footprint: Use public transport, switch to LED bulbs, eat more plant-based meals, and reduce waste!"
        elif 'eco' in message_lower or 'sustainable' in message_lower:
            response = "Sustainable living tips: Choose reusable products, buy local, reduce energy consumption, and support eco-friendly brands!"
        else:
            response = "I can help with climate data, carbon footprint reduction, and sustainable living. What would you like to know?"
        
        return {
            "success": True,
            "response": response,
            "intent": self._detect_intent(message),
            "suggestions": self._generate_suggestions(message),
            "ai_powered": False,
            "timestamp": datetime.now().isoformat()
        }
    
    def _detect_intent(self, message: str) -> str:
        """Simple intent detection"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['weather', 'temperature', 'climate']):
            return 'weather'
        elif any(word in message_lower for word in ['carbon', 'footprint', 'emissions']):
            return 'carbon'
        elif any(word in message_lower for word in ['eco', 'sustainable', 'green']):
            return 'eco_shopping'
        elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return 'greeting'
        else:
            return 'general'
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Generate contextual suggestions"""
        intent = self._detect_intent(message)
        
        suggestions_map = {
            'weather': ["What's the weather in Mumbai?", "Compare Delhi and Bangalore climate", "Show air quality data"],
            'carbon': ["Calculate my carbon footprint", "Energy saving tips", "Transportation alternatives"],
            'eco_shopping': ["Show eco-friendly products", "Sustainable alternatives", "Green certifications"],
            'greeting': ["What's the weather like?", "How can I reduce my carbon footprint?", "Show sustainable products"],
            'general': ["Weather in my city", "Carbon reduction tips", "Eco-friendly products"]
        }
        
        return suggestions_map.get(intent, suggestions_map['general'])
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Placeholder for conversation history"""
        return []
    
    def clear_conversation_history(self, user_id: str) -> bool:
        """Placeholder for clearing history"""
        return True
    
    def get_bot_info(self) -> Dict[str, Any]:
        """Get bot information"""
        return {
            "name": self.name,
            "version": self.version,
            "ai_powered": True,
            "model": "Google Gemini 2.0 Flash Experimental",
            "model_id": self.model,
            "features": [
                "Ultra-fast response times",
                "Advanced multimodal understanding",
                "Enhanced coding capabilities",
                "Complex instruction following",
                "1M+ token context window"
            ],
            "capabilities": [
                "AI-powered climate conversations",
                "Real-time weather and climate data",
                "Carbon footprint calculations & advice",
                "Eco-friendly product recommendations",
                "Sustainable living tips",
                "Air quality insights",
                "Environmental education"
            ]
        }

# Create global instance
ai_climate_bot = AIClimateBot()

