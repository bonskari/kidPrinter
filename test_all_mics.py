#!/usr/bin/env python3
"""
Test all available microphone devices
"""

import speech_recognition as sr
import numpy as np

def test_all_microphones():
    """Test all available microphone devices"""
    print("🎤 Testing All Microphone Devices")
    print("=" * 35)
    
    r = sr.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False
    
    # Get all microphones
    mic_list = sr.Microphone.list_microphone_names()
    print(f"Found {len(mic_list)} microphones:")
    for i, name in enumerate(mic_list):
        print(f"  {i}: {name}")
    print()
    
    for device_index in range(len(mic_list)):
        print(f"🧪 Testing device {device_index}: {mic_list[device_index]}")
        
        try:
            with sr.Microphone(device_index=device_index) as source:
                print("   🎤 Speak loudly now...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                
                # Check audio level
                raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                max_amp = np.max(np.abs(raw_data))
                level = max_amp / 32767 * 100
                
                print(f"   📊 Audio level: {level:.1f}%")
                
                if max_amp < 1000:
                    print("   ⚠️  Too low for STT")
                    continue
                
                # Try recognition
                print("   🔄 Testing recognition...")
                
                success = False
                for lang, lang_name in [('en-US', 'English'), ('fi-FI', 'Finnish')]:
                    try:
                        text = r.recognize_google(audio, language=lang)
                        print(f"   ✅ {lang_name}: '{text}'")
                        success = True
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(f"   ❌ {lang_name}: {e}")
                        break
                
                if success:
                    print(f"   🎉 SUCCESS with device {device_index}!")
                    return device_index
                else:
                    print("   ❌ No recognition")
                
        except sr.WaitTimeoutError:
            print("   ⏰ No speech detected")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    return None

if __name__ == "__main__":
    print("🎯 Microphone Device Test")
    print("=" * 30)
    
    working_device = test_all_microphones()
    
    if working_device is not None:
        print(f"🎉 FOUND WORKING DEVICE: {working_device}")
        print("Update your application to use this device index")
    else:
        print("⚠️  No working microphone device found")
        print("Try speaking much louder or closer to microphone")