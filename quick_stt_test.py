#!/usr/bin/env python3
"""
Quick STT test with improved microphone
"""

import speech_recognition as sr
import numpy as np

def quick_stt_test():
    """Quick STT test"""
    print("🎯 Quick STT Test - Improved Microphone")
    print("=" * 40)
    
    r = sr.Recognizer()
    r.energy_threshold = 200  # Lower threshold for better sensitivity
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            print("🎤 Speak NOW for 3 seconds - say 'HELLO'!")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            
            # Check audio quality
            raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            max_amp = np.max(np.abs(raw_data))
            print(f"📊 Audio level: {max_amp} ({max_amp/32767*100:.1f}% of max)")
            
            if max_amp < 2000:
                print("⚠️  Audio still too low - try speaking MUCH louder")
                return False
            
            print("🔄 Testing recognition...")
            
            # Try English
            try:
                text = r.recognize_google(audio, language='en-US')
                print(f"✅ English SUCCESS: '{text}'")
                return True
            except sr.UnknownValueError:
                print("❌ English: Could not understand")
            except sr.RequestError as e:
                print(f"❌ English: Error - {e}")
            
            # Try Finnish
            try:
                text = r.recognize_google(audio, language='fi-FI')
                print(f"✅ Finnish SUCCESS: '{text}'")
                return True
            except sr.UnknownValueError:
                print("❌ Finnish: Could not understand")
            except sr.RequestError as e:
                print(f"❌ Finnish: Error - {e}")
            
            return False
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_stt_test()
    
    if success:
        print("\n🎉 STT IS WORKING!")
        print("The microphone boost fixed the issue!")
    else:
        print("\n⚠️  STT still needs improvement")
        print("Try speaking even louder or closer to the microphone")