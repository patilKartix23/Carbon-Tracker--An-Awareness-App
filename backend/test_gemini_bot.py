"""
Test script for Gemini 2.0 Flash EcoBot integration
Run this to verify the AI chatbot is working correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.ai_climate_bot import ai_climate_bot
import json

def test_bot():
    """Test the Gemini-powered EcoBot"""
    
    print("=" * 60)
    print("🤖 Testing EcoBot with Gemini 2.0 Flash Experimental")
    print("=" * 60)
    
    # Get bot info
    bot_info = ai_climate_bot.get_bot_info()
    print("\n📋 Bot Information:")
    print(json.dumps(bot_info, indent=2))
    
    # Test messages
    test_messages = [
        "Hello! What can you help me with?",
        "What's the weather like in Mumbai?",
        "How can I reduce my carbon footprint?",
        "Show me eco-friendly products"
    ]
    
    print("\n" + "=" * 60)
    print("🧪 Running Test Conversations")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Test {i}] User: {message}")
        print("-" * 60)
        
        try:
            response = ai_climate_bot.process_message(message, user_id="test_user")
            
            if response["success"]:
                print(f"✅ Bot Response: {response['response']}")
                print(f"   Intent: {response.get('intent', 'unknown')}")
                print(f"   AI Powered: {response.get('ai_powered', False)}")
                
                if response.get('suggestions'):
                    print(f"   Suggestions: {', '.join(response['suggestions'][:2])}...")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✨ Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_bot()

