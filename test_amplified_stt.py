#!/usr/bin/env python3
"""
Test STT with software audio amplification
"""

import speech_recognition as sr
import numpy as np
import io
import wave

def amplify_audio(audio_data, amplification=10):
    """Amplify audio data by specified factor"""
    # Convert to numpy array
    raw_data = np.frombuffer(audio_data, dtype=np.int16)
    
    # Amplify and clip to prevent overflow
    amplified = np.clip(raw_data * amplification, -32767, 32767).astype(np.int16)
    
    return amplified.tobytes()

def test_amplified_stt():
    """Test STT with amplified audio"""
    print("🔊 Testing STT with Software Amplification")
    print("=" * 45)
    
    r = sr.Recognizer()
    r.energy_threshold = 50  # Very low threshold
    r.dynamic_energy_threshold = False  # Disable auto-adjustment
    
    amplification_levels = [5, 10, 20, 50]
    
    for amp_level in amplification_levels:
        print(f"\n🧪 Testing {amp_level}x amplification")
        
        try:
            with sr.Microphone(device_index=0) as source:
                print("   🎤 Speak now...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                
                # Check original level
                raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                original_level = np.max(np.abs(raw_data)) / 32767 * 100
                print(f"   📊 Original level: {original_level:.1f}%")
                
                if original_level < 0.5:
                    print("   ⚠️  Too quiet for testing")
                    continue
                
                # Amplify audio
                amplified_data = amplify_audio(audio.get_raw_data(), amp_level)
                
                # Check amplified level
                amp_array = np.frombuffer(amplified_data, dtype=np.int16)
                amp_level_pct = np.max(np.abs(amp_array)) / 32767 * 100
                print(f"   📊 Amplified level: {amp_level_pct:.1f}%")
                
                # Create new AudioData object with amplified data
                amplified_audio = sr.AudioData(
                    amplified_data,
                    audio.sample_rate,
                    audio.sample_width
                )
                
                # Try recognition on amplified audio
                try:
                    text = r.recognize_google(amplified_audio, language='en-US')
                    print(f"   ✅ SUCCESS: '{text}'")
                    return True, amp_level
                except sr.UnknownValueError:
                    print("   ❌ Still not understood")
                except sr.RequestError as e:
                    print(f"   ❌ Error: {e}")
                
        except sr.WaitTimeoutError:
            print("   ⏰ No speech detected")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False, None

if __name__ == "__main__":
    print("🎯 Software Audio Amplification Test")
    print("=" * 40)
    
    success, best_amp = test_amplified_stt()
    
    if success:
        print(f"\n🎉 SUCCESS! {best_amp}x amplification works!")
        print("This can be integrated into the main application")
    else:
        print("\n⚠️  Amplification alone not sufficient")
        print("Need to try alternative approaches")