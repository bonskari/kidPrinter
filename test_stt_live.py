#!/usr/bin/env python3
"""
Live STT test - shows what you speak in real time
Focus on debugging speech recognition issues
"""

import speech_recognition as sr
import numpy as np
import time

def test_live_stt():
    """Continuous STT testing"""
    print("🎤 Live STT Test")
    print("=" * 30)
    print("Speak clearly into the microphone...")
    print("Press Ctrl+C to stop")
    print()
    
    r = sr.Recognizer()
    r.energy_threshold = 200  # Optimized from our previous tests
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"📊 Energy threshold set to: {r.energy_threshold}")
            print()
            
            success_count = 0
            total_attempts = 0
            
            while True:
                try:
                    print("🎤 Listening... (speak now)")
                    
                    # Listen for speech
                    audio = r.listen(source, timeout=1, phrase_time_limit=5)
                    total_attempts += 1
                    
                    # Check audio quality
                    raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    max_amp = np.max(np.abs(raw_data))
                    audio_level = max_amp / 32767 * 100
                    
                    print(f"   📊 Audio level: {audio_level:.1f}%", end="")
                    
                    if max_amp < 1000:
                        print(" (TOO LOW - speak louder)")
                        continue
                    else:
                        print(" (Good)")
                    
                    # Try Finnish recognition
                    try:
                        text_fi = r.recognize_google(audio, language='fi-FI')
                        print(f"   🇫🇮 Finnish: '{text_fi}'")
                        success_count += 1
                        continue
                    except sr.UnknownValueError:
                        print("   🇫🇮 Finnish: (not understood)")
                    except sr.RequestError as e:
                        print(f"   🇫🇮 Finnish: ERROR - {e}")
                    
                    # Try English recognition
                    try:
                        text_en = r.recognize_google(audio, language='en-US')
                        print(f"   🇺🇸 English: '{text_en}'")
                        success_count += 1
                    except sr.UnknownValueError:
                        print("   🇺🇸 English: (not understood)")
                    except sr.RequestError as e:
                        print(f"   🇺🇸 English: ERROR - {e}")
                    
                    print()
                    
                except sr.WaitTimeoutError:
                    # No speech detected, continue listening
                    continue
                except KeyboardInterrupt:
                    break
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print(f"\n📊 Results: {success_count}/{total_attempts} successful recognitions")
    if success_count > 0:
        print("✅ STT is working!")
    else:
        print("⚠️  STT needs debugging")
    
    return success_count > 0

def quick_audio_test():
    """Quick test of microphone audio levels"""
    print("🔍 Quick Audio Level Test")
    print("=" * 25)
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🎤 Say something loud for 3 seconds...")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            
            raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            max_amp = np.max(np.abs(raw_data))
            rms = np.sqrt(np.mean(raw_data**2))
            
            print(f"📊 Max amplitude: {max_amp} ({max_amp/32767*100:.1f}%)")
            print(f"📊 RMS level: {rms:.0f} ({rms/32767*100:.1f}%)")
            
            if max_amp < 1000:
                print("⚠️  VERY LOW - check microphone gain")
            elif max_amp < 5000:
                print("⚠️  Low - try speaking louder")
            else:
                print("✅ Good audio level")
            
            return max_amp > 1000
            
    except Exception as e:
        print(f"❌ Audio test error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 STT Debugging Tool")
    print("=" * 40)
    
    # First do a quick audio test
    if quick_audio_test():
        print("\n🚀 Starting live STT test...")
        print("Say things like:")
        print("  - 'Hei' (Finnish hello)")
        print("  - 'Tulosta kuva' (print picture)")
        print("  - 'Hello world' (English)")
        print()
        
        test_live_stt()
    else:
        print("\n⚠️  Audio levels too low for STT")
        print("Try adjusting microphone gain or speaking louder")