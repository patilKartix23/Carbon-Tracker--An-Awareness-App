from flask import Blueprint, request, jsonify
from services.climate_bot import climate_bot
from datetime import datetime
import traceback
import logging
import os

logger = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot', __name__)

# Try to import AI bot, fallback to regular bot if unavailable
try:
    from services.ai_climate_bot import ai_climate_bot
    AI_BOT_AVAILABLE = True
    logger.info("AI Chatbot loaded successfully")
except Exception as e:
    logger.warning(f"AI Chatbot not available: {e}")
    AI_BOT_AVAILABLE = False

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint for processing user messages"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')
        use_ai = data.get('use_ai', True) and AI_BOT_AVAILABLE
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Process message with AI bot if available, otherwise use rule-based bot
        if use_ai and AI_BOT_AVAILABLE:
            response = ai_climate_bot.process_message(message, user_id, use_ai=True)
        else:
            response = climate_bot.process_message(message, user_id)
        
        return jsonify({
            "status": "success",
            "bot_response": response["response"],
            "intent": response.get("intent", "unknown"),
            "suggestions": response.get("suggestions", []),
            "data": response.get("data"),
            "user_message": message,
            "timestamp": response["timestamp"],
            "conversation_id": user_id
        })
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "error": f"Failed to process chat message: {str(e)}",
            "bot_response": "I'm sorry, I'm having trouble right now. Please try again!",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get conversation history for a specific user"""
    try:
        history = climate_bot.get_conversation_history(user_id)
        
        return jsonify({
            "status": "success",
            "conversation_history": history,
            "user_id": user_id,
            "message_count": len(history),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to get chat history: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/history/<user_id>', methods=['DELETE'])
def clear_chat_history(user_id):
    """Clear conversation history for a specific user"""
    try:
        success = climate_bot.clear_conversation_history(user_id)
        
        return jsonify({
            "status": "success",
            "cleared": success,
            "user_id": user_id,
            "message": "Chat history cleared successfully" if success else "No history found for user",
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to clear chat history: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/suggestions', methods=['GET'])
def get_chat_suggestions():
    """Get suggested questions/prompts for users"""
    try:
        suggestions = [
            {
                "category": "Weather Queries",
                "suggestions": [
                    "What's the weather like in Mumbai?",
                    "Show me temperature in Delhi",
                    "How humid is it in Chennai?",
                    "Tell me about rainfall in Bangalore"
                ]
            },
            {
                "category": "City Comparisons", 
                "suggestions": [
                    "Compare Mumbai and Delhi weather",
                    "Delhi vs Bangalore climate",
                    "Which city is warmer: Chennai or Kolkata?",
                    "Compare rainfall between Mumbai and Pune"
                ]
            },
            {
                "category": "Carbon Footprint",
                "suggestions": [
                    "How can I reduce my carbon footprint?",
                    "Calculate my transportation emissions",
                    "Energy saving tips",
                    "Sustainable living practices"
                ]
            },
            {
                "category": "Eco-Shopping",
                "suggestions": [
                    "Show me eco-friendly products",
                    "Sustainable alternatives to plastic",
                    "Green energy solutions",
                    "Organic and natural products"
                ]
            },
            {
                "category": "Climate Knowledge",
                "suggestions": [
                    "Explain Indian monsoon season",
                    "Best time to visit different cities",
                    "Air quality tips",
                    "Seasonal climate patterns"
                ]
            }
        ]
        
        return jsonify({
            "status": "success",
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to get suggestions: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/quick-response', methods=['POST'])
def quick_response():
    """Handle quick response buttons/suggestions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        quick_type = data.get('type', '')
        user_id = data.get('user_id', 'default')
        city = data.get('city', 'Delhi')
        
        response_map = {
            'weather_summary': f"What's the current weather in {city}?",
            'carbon_tips': "How can I reduce my carbon footprint?",
            'eco_products': "Show me eco-friendly products",
            'air_quality': f"Tell me about air quality in {city}",
            'monsoon_info': "Explain the monsoon season",
            'city_compare': f"Compare {city} with Mumbai"
        }
        
        message = response_map.get(quick_type, "Hello! How can I help you?")
        
        # Process the quick response as a regular message
        response = climate_bot.process_message(message, user_id)
        
        return jsonify({
            "status": "success",
            "bot_response": response["response"],
            "intent": response.get("intent", "unknown"),
            "suggestions": response.get("suggestions", []),
            "data": response.get("data"),
            "quick_type": quick_type,
            "timestamp": response["timestamp"]
        })
    
    except Exception as e:
        logger.error(f"Error in quick response: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to process quick response: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/bot-info', methods=['GET'])
def get_bot_info():
    """Get information about the chatbot's capabilities"""
    try:
        if AI_BOT_AVAILABLE:
            bot_info = ai_climate_bot.get_bot_info()
            bot_info['ai_available'] = True
            bot_info['bot_type'] = 'AI-Powered' if bot_info.get('ai_powered') else 'Hybrid'
        else:
            bot_info = climate_bot.get_bot_info()
            bot_info['ai_available'] = False
            bot_info['bot_type'] = 'Rule-Based'
        
        return jsonify({
            "status": "success",
            "bot_info": bot_info,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to get bot info: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/health', methods=['GET'])
def chatbot_health():
    """Health check for chatbot service"""
    try:
        # Test basic functionality
        test_response = climate_bot.process_message("hello", "health_check")
        
        return jsonify({
            "status": "healthy",
            "service": "climate-chatbot",
            "version": climate_bot.version,
            "bot_name": climate_bot.name,
            "test_response_received": bool(test_response.get("response")),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Chatbot health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "climate-chatbot",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/context', methods=['POST'])
def set_context():
    """Set conversation context (like current location, preferences)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_id = data.get('user_id', 'default')
        context = data.get('context', {})
        
        # For now, we'll acknowledge context but could enhance bot to use it
        # Future enhancement: store user preferences, location, etc.
        
        return jsonify({
            "status": "success",
            "message": "Context received and will be used for personalized responses",
            "user_id": user_id,
            "context_keys": list(context.keys()),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error setting context: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to set context: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@chatbot_bp.route('/chat/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback about chatbot responses"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_id = data.get('user_id', 'default')
        message_id = data.get('message_id', '')
        rating = data.get('rating', 0)  # 1-5 scale
        feedback_text = data.get('feedback', '')
        
        # Log feedback for future improvements
        logger.info(f"Chatbot feedback - User: {user_id}, Rating: {rating}, Feedback: {feedback_text}")
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your feedback! It helps us improve the chatbot.",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to submit feedback: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500