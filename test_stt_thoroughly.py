#!/usr/bin/env python3
"""
Thorough STT test - try different approaches
"""

import speech_recognition as sr
import time

def test_stt_thoroughly():
    """Test STT with different settings and approaches"""
    print("🎤 Thorough STT Test")
    print("=" * 30)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Test 1: Basic microphone test
    print("\n1. Testing microphone accessibility...")
    try:
        with sr.Microphone(device_index=0) as source:
            print("   ✅ Microphone accessible")
            print(f"   Device: {source.device_index}")
            print(f"   Sample rate: {source.SAMPLE_RATE}")
            print(f"   Chunk size: {source.CHUNK}")
    except Exception as e:
        print(f"   ❌ Microphone error: {e}")
        return
    
    # Test 2: Audio capture test
    print("\n2. Testing audio capture...")
    try:
        with sr.Microphone(device_index=0) as source:
            print("   🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            print("   🎤 Capturing 3 seconds of audio...")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            
            print(f"   ✅ Audio captured: {len(audio.get_raw_data())} bytes")
            print(f"   Sample rate: {audio.sample_rate}")
            print(f"   Sample width: {audio.sample_width}")
            
            # Test 3: Try recognition with debug info
            print("\n3. Testing speech recognition...")
            
            # Try Google with show_all for debug
            try:
                print("   🔄 Trying Google STT with debug...")
                result = r.recognize_google(audio, language='fi-FI', show_all=True)
                print(f"   🇫🇮 Google debug result: {result}")
            except sr.UnknownValueError:
                print("   🇫🇮 Google: No speech detected")
            except sr.RequestError as e:
                print(f"   🇫🇮 Google: Network error - {e}")
            
            # Try English
            try:
                print("   🔄 Trying Google STT (English)...")
                result = r.recognize_google(audio, language='en-US', show_all=True)
                print(f"   🇺🇸 Google English result: {result}")
            except sr.UnknownValueError:
                print("   🇺🇸 Google English: No speech detected")
            except sr.RequestError as e:
                print(f"   🇺🇸 Google English: Network error - {e}")
                
    except sr.WaitTimeoutError:
        print("   ⏰ No audio captured (timeout)")
    except Exception as e:
        print(f"   ❌ Audio capture error: {e}")
    
    # Test 4: Interactive test
    print("\n4. Interactive test...")
    print("   Now I'll listen for 10 seconds.")
    print("   Please speak LOUDLY and CLEARLY:")
    print("   Try: 'HELLO WORLD' or 'HYVÄÄ PÄIVÄÄ'")
    print("   Speak NOW!")
    
    try:
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            
            print("   🔄 Processing your speech...")
            
            # Try both languages
            recognized = False
            
            try:
                text = r.recognize_google(audio, language='en-US')
                print(f"   🇺🇸 English: '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("   🇺🇸 English: Could not understand")
            except sr.RequestError as e:
                print(f"   🇺🇸 English: Error - {e}")
            
            try:
                text = r.recognize_google(audio, language='fi-FI')
                print(f"   🇫🇮 Finnish: '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("   🇫🇮 Finnish: Could not understand")
            except sr.RequestError as e:
                print(f"   🇫🇮 Finnish: Error - {e}")
            
            if not recognized:
                print("   ❌ No speech recognized in either language")
                print("   💡 Try speaking louder or closer to the microphone")
            
    except sr.WaitTimeoutError:
        print("   ⏰ No speech detected in 10 seconds")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ STT test completed")
    print("\nTroubleshooting tips:")
    print("- Speak loudly and clearly")
    print("- Get closer to the microphone")
    print("- Try simple words like 'hello' or 'test'")
    print("- Check internet connection for Google STT")

if __name__ == "__main__":
    test_stt_thoroughly()