#!/usr/bin/env python3
"""
Test Gemini integration with KidPrinter
"""

import os
import sys
sys.path.append('src')
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from main import KidPrinter

def test_gemini_only():
    """Test just the Gemini AI functionality"""
    print("🔍 Testing Gemini Integration")
    print("=" * 30)
    
    # Use the API key from environment variable
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable not set")
        return False
    
    print(f"✅ Using API key: {os.getenv('GEMINI_API_KEY')[:20]}...")
    
    try:
        app = KidPrinter()
        
        if not app.gemini_enabled:
            print("❌ Gemini not enabled. Check your API key.")
            return False
        
        print("✅ Gemini initialized successfully!")
        print("\n🧪 Testing conversations...")
        
        # Test conversations
        test_inputs = [
            "Hei!",
            "Mitä voin tulostaa?",
            "Tulosta kuva kissasta",
            "Kerro vitsi",
            "Mikä on sinun nimesi?"
        ]
        
        for test_input in test_inputs:
            print(f"\n👤 User: {test_input}")
            response = app.get_ai_response(test_input)
            print(f"🤖 AI: {response}")
            
        print("\n✅ Gemini conversation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_without_tts():
    """Test the conversation logic without TTS"""
    print("\n🔇 Testing conversation logic (no TTS)")
    print("=" * 35)
    
    try:
        app = KidPrinter()
        
        if not app.gemini_enabled:
            print("❌ Gemini not enabled. Check your API key.")
            return False
        
        # Disable TTS for testing
        app.tts_enabled = False
        
        # Simulate speech input
        test_speech = "Tulosta kuva koirasta"
        print(f"👂 Simulated speech: {test_speech}")
        
        # Test the AI response
        ai_response = app.get_ai_response(test_speech)
        print(f"🤖 AI Response: {ai_response}")
        
        # Test print detection
        print_keywords = ['tulosta', 'print', 'printtaa', 'kirjoita']
        is_print_request = any(keyword in test_speech.lower() for keyword in print_keywords)
        print(f"📄 Print request detected: {is_print_request}")
        
        if is_print_request and app.check_daily_limit():
            print("✅ Print request would be processed")
            # Simulate print
            app.daily_print_count += 1
            print(f"📊 Daily count updated: {app.daily_print_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Gemini Integration Test")
    print("=" * 40)
    
    # Test 1: Basic Gemini functionality
    if test_gemini_only():
        print("\n🎉 Gemini integration working!")
        
        # Test 2: Conversation logic
        test_without_tts()
        
        print("\n✅ All tests completed!")
        print("Your KidPrinter is ready for conversational AI!")
    else:
        print("\n⚠️  Gemini integration needs setup")
        print("Please ensure you have a valid API key")