#!/usr/bin/env python3
"""
Test STT with boosted microphone gain
"""

import speech_recognition as sr
import wave
import numpy as np
import os

def analyze_audio_quality(audio_data):
    """Quick audio quality check"""
    # Convert to numpy array
    raw_data = np.frombuffer(audio_data, dtype=np.int16)
    
    # Calculate metrics
    max_amp = np.max(np.abs(raw_data))
    rms = np.sqrt(np.mean(raw_data**2))
    
    print(f"   Max amplitude: {max_amp} ({max_amp/32767*100:.1f}% of max)")
    print(f"   RMS level: {rms:.0f} ({rms/32767*100:.1f}% of max)")
    
    if max_amp < 1000:
        print("   ⚠️  STILL TOO LOW")
        return False
    elif max_amp < 5000:
        print("   ⚠️  Low but better")
        return True
    else:
        print("   ✅ Good audio level!")
        return True

def test_boosted_microphone():
    """Test microphone with boosted gain"""
    print("🔊 Testing Boosted Microphone")
    print("=" * 30)
    
    r = sr.Recognizer()
    
    # Lower energy threshold for better sensitivity
    r.energy_threshold = 200
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            print("🎤 SPEAK LOUDLY NOW - say 'HELLO WORLD'!")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            print("📊 Analyzing audio quality...")
            analyze_audio_quality(audio.get_raw_data())
            
            print("🔄 Testing speech recognition...")
            
            # Test both languages
            success = False
            
            # English first
            try:
                text = r.recognize_google(audio, language='en-US')
                print(f"✅ English SUCCESS: '{text}'")
                success = True
            except sr.UnknownValueError:
                print("❌ English: Could not understand")
            except sr.RequestError as e:
                print(f"❌ English: Error - {e}")
            
            # Finnish
            try:
                text = r.recognize_google(audio, language='fi-FI')
                print(f"✅ Finnish SUCCESS: '{text}'")
                success = True
            except sr.UnknownValueError:
                print("❌ Finnish: Could not understand")
            except sr.RequestError as e:
                print(f"❌ Finnish: Error - {e}")
            
            return success
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_continuous_recognition():
    """Test continuous recognition with boosted audio"""
    print("\n🔄 Continuous Recognition Test")
    print("=" * 30)
    
    r = sr.Recognizer()
    r.energy_threshold = 200
    
    print("🎤 Listening continuously... speak clearly!")
    print("   Try: 'hello', 'test', 'tulosta', 'hei'")
    print("   Press Ctrl+C to stop")
    
    try:
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            
            success_count = 0
            total_attempts = 0
            
            while True:
                try:
                    print("\n🎤 Listening...")
                    audio = r.listen(source, timeout=1, phrase_time_limit=3)
                    
                    total_attempts += 1
                    
                    # Quick quality check
                    raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    max_amp = np.max(np.abs(raw_data))
                    print(f"   Audio level: {max_amp/32767*100:.1f}%")
                    
                    if max_amp < 1000:
                        print("   ⚠️  Too quiet, try speaking louder")
                        continue
                    
                    # Try recognition
                    recognized = False
                    for lang, lang_name in [('en-US', 'English'), ('fi-FI', 'Finnish')]:
                        try:
                            text = r.recognize_google(audio, language=lang)
                            print(f"   ✅ {lang_name}: '{text}'")
                            success_count += 1
                            recognized = True
                            break
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError as e:
                            print(f"   ❌ {lang_name}: {e}")
                            break
                    
                    if not recognized:
                        print("   ❌ No recognition")
                        
                except sr.WaitTimeoutError:
                    continue
                except KeyboardInterrupt:
                    break
                    
            print(f"\n📊 Results: {success_count}/{total_attempts} successful recognitions")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 STT Test with Boosted Microphone")
    print("=" * 40)
    
    # Test 1: Single recognition
    if test_boosted_microphone():
        print("\n🎉 SUCCESS! STT is working with boosted microphone!")
        
        # Test 2: Continuous recognition
        try:
            test_continuous_recognition()
        except KeyboardInterrupt:
            print("\n👋 Test completed!")
    else:
        print("\n⚠️  Still having issues. Try:")
        print("   - Speaking MUCH louder")
        print("   - Getting closer to microphone")
        print("   - Using simple English words")