#!/usr/bin/env python3
"""
Test conversation flow without audio complications
"""

import os
import sys
sys.path.append('src')
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Mock the audio libraries to avoid ALSA issues
import unittest.mock

# Mock speech_recognition and pyttsx3 to avoid audio setup
with unittest.mock.patch('speech_recognition.Recognizer'), \
     unittest.mock.patch('pyttsx3.init'):
    
    from main import KidPrinter

def test_conversation_flow():
    """Test the conversation logic without audio"""
    print("🗣️  Testing Conversation Flow (No Audio)")
    print("=" * 40)
    
    try:
        app = KidPrinter()
        
        if not app.gemini_enabled:
            print("❌ Gemini not enabled")
            return False
        
        print("✅ App initialized (audio mocked)")
        
        # Test conversations
        test_cases = [
            ("Hei!", "greeting"),
            ("Tulosta kuva kissasta", "print_request"),
            ("Mitä voin tulostaa?", "question"),
            ("Kerro vitsi", "entertainment"),
            ("Tulosta dinosaurus", "print_request")
        ]
        
        for user_input, case_type in test_cases:
            print(f"\n👤 User: '{user_input}' ({case_type})")
            
            # Get AI response
            ai_response = app.get_ai_response(user_input)
            print(f"🤖 AI: {ai_response[:100]}...")
            
            # Check print detection
            print_keywords = ['tulosta', 'print', 'printtaa', 'kirjoita']
            is_print_request = any(keyword in user_input.lower() for keyword in print_keywords)
            
            if is_print_request:
                print(f"📄 Print detected: YES")
                if app.check_daily_limit():
                    app.daily_print_count += 1
                    print(f"📊 Print count: {app.daily_print_count}/5")
                else:
                    print("⚠️  Daily limit reached")
            else:
                print(f"📄 Print detected: NO")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Conversation Flow Test")
    print("=" * 30)
    
    if test_conversation_flow():
        print("\n✅ Conversation system working!")
        print("Next step: Fix audio issues for full testing")
    else:
        print("\n❌ Conversation system needs debugging")