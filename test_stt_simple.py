#!/usr/bin/env python3
"""
Simple STT test - listens for 10 seconds and shows what it hears
"""

import speech_recognition as sr
import time

def test_stt():
    """Test speech-to-text recognition"""
    print("🎤 Simple STT Test")
    print("=" * 30)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    try:
        mic_list = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_list):
            print(f"  {i}: {name}")
    except Exception as e:
        print(f"Error listing microphones: {e}")
        return
    
    print("\nUsing USB microphone (device 0)...")
    
    try:
        # Use USB microphone
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            print("🎤 Listening for 10 seconds - speak now!")
            print("   Try saying: 'tulosta kuva' or 'hello world'")
            
            # Listen for speech
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            
            # Try Finnish first
            try:
                text = r.recognize_google(audio, language='fi-FI')
                print(f"🇫🇮 Finnish: {text}")
            except sr.UnknownValueError:
                print("🇫🇮 Finnish: Could not understand")
            except sr.RequestError as e:
                print(f"🇫🇮 Finnish: Error - {e}")
            
            # Try English as backup
            try:
                text = r.recognize_google(audio, language='en-US')
                print(f"🇺🇸 English: {text}")
            except sr.UnknownValueError:
                print("🇺🇸 English: Could not understand")
            except sr.RequestError as e:
                print(f"🇺🇸 English: Error - {e}")
                
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within 10 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ STT test completed")

if __name__ == "__main__":
    test_stt()