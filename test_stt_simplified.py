#!/usr/bin/env python3
"""
Simplified STT test - speak VERY LOUDLY
"""

import speech_recognition as sr
import numpy as np

def test_loud_speech():
    """Test with very loud speech"""
    print("🎤 SIMPLIFIED STT TEST")
    print("=" * 25)
    print("⚠️  IMPORTANT: SPEAK VERY LOUDLY AND CLEARLY!")
    print("Get close to the microphone and SHOUT!")
    print()
    
    r = sr.Recognizer()
    r.energy_threshold = 100  # Lower threshold for more sensitivity
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"📊 Energy threshold: {r.energy_threshold}")
            print()
            
            for attempt in range(3):
                print(f"🎤 ATTEMPT {attempt+1}/3 - SPEAK VERY LOUDLY NOW!")
                print("Say: 'HELLO WORLD' or 'MOI' (Finnish hello)")
                
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    
                    # Check audio level
                    raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    max_amp = np.max(np.abs(raw_data))
                    level = max_amp / 32767 * 100
                    
                    print(f"   📊 Audio level: {level:.1f}%")
                    
                    if max_amp < 2000:
                        print("   ⚠️  TOO QUIET! Speak MUCH louder!")
                        continue
                    
                    # Try recognition
                    print("   🔄 Processing...")
                    
                    # Try English
                    try:
                        text = r.recognize_google(audio, language='en-US')
                        print(f"   ✅ ENGLISH: '{text}'")
                        return True
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"   ❌ English error: {e}")
                    
                    # Try Finnish
                    try:
                        text = r.recognize_google(audio, language='fi-FI')
                        print(f"   ✅ FINNISH: '{text}'")
                        return True
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"   ❌ Finnish error: {e}")
                    
                    print("   ❌ No recognition - try speaking louder")
                    
                except sr.WaitTimeoutError:
                    print("   ⏰ No speech detected")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                
                print()
        
        return False
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 LOUD SPEECH STT TEST")
    print("=" * 30)
    print("Microphone is at 100% gain")
    print("Auto Gain Control is ON")
    print()
    
    if test_loud_speech():
        print("🎉 STT WORKING! Speech recognized!")
    else:
        print("⚠️  Try speaking even LOUDER or closer to microphone")
        print("   - Get microphone 5cm from your mouth")
        print("   - Speak as loud as comfortable")
        print("   - Try simple words: 'HELLO', 'TEST', 'MOI'")