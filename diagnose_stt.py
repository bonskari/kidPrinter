#!/usr/bin/env python3
"""
Comprehensive STT diagnostic tool
"""

import speech_recognition as sr
import pyaudio
import wave
import numpy as np
import time
import json
import subprocess
import os

def analyze_audio_file(filename):
    """Analyze audio file quality"""
    try:
        # Read WAV file
        with wave.open(filename, 'rb') as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Calculate audio metrics
            max_amplitude = np.max(np.abs(audio_data))
            rms = np.sqrt(np.mean(audio_data**2))
            
            print(f"   Audio file: {filename}")
            print(f"   Sample rate: {wav_file.getframerate()} Hz")
            print(f"   Channels: {wav_file.getnchannels()}")
            print(f"   Duration: {wav_file.getnframes() / wav_file.getframerate():.2f} seconds")
            print(f"   Max amplitude: {max_amplitude} ({max_amplitude/32767*100:.1f}% of max)")
            print(f"   RMS level: {rms:.0f} ({rms/32767*100:.1f}% of max)")
            
            # Audio quality assessment
            if max_amplitude < 1000:
                print("   ⚠️  Audio level is VERY LOW - microphone may not be working")
            elif max_amplitude < 5000:
                print("   ⚠️  Audio level is LOW - try speaking louder")
            elif max_amplitude > 30000:
                print("   ⚠️  Audio level is HIGH - may be clipping")
            else:
                print("   ✅ Audio level looks good")
                
            return True
            
    except Exception as e:
        print(f"   ❌ Error analyzing audio: {e}")
        return False

def test_microphone_devices():
    """Test different microphone devices"""
    print("🎤 Testing All Microphone Devices")
    print("=" * 40)
    
    r = sr.Recognizer()
    
    # List all microphones
    mic_list = sr.Microphone.list_microphone_names()
    print(f"Found {len(mic_list)} microphones:")
    for i, name in enumerate(mic_list):
        print(f"  {i}: {name}")
    
    # Test each microphone
    for device_index in range(len(mic_list)):
        print(f"\n🔍 Testing device {device_index}: {mic_list[device_index]}")
        
        try:
            with sr.Microphone(device_index=device_index) as source:
                print("   🔧 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1)
                
                print("   🎤 Recording 3 seconds of audio...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                
                # Save audio for analysis
                wav_file = f"/tmp/mic_test_{device_index}.wav"
                with open(wav_file, "wb") as f:
                    f.write(audio.get_wav_data())
                
                print("   📊 Analyzing audio quality...")
                analyze_audio_file(wav_file)
                
                # Try speech recognition
                print("   🔄 Testing speech recognition...")
                try:
                    text = r.recognize_google(audio, language='en-US')
                    print(f"   ✅ STT SUCCESS: '{text}'")
                    return device_index, text  # Return successful device
                except sr.UnknownValueError:
                    print("   ❌ STT: Could not understand audio")
                except sr.RequestError as e:
                    print(f"   ❌ STT: Request error - {e}")
                
                # Clean up
                os.unlink(wav_file)
                
        except Exception as e:
            print(f"   ❌ Device error: {e}")
            
    return None, None

def test_recognition_settings():
    """Test different recognition settings"""
    print("\n🔧 Testing Recognition Settings")
    print("=" * 35)
    
    r = sr.Recognizer()
    
    # Test different energy thresholds
    print("Testing different energy thresholds...")
    
    # Get the best microphone device from previous test
    best_device = 0  # Default to device 0
    
    try:
        with sr.Microphone(device_index=best_device) as source:
            print("🎤 Speak NOW for 5 seconds - say 'HELLO WORLD' clearly!")
            
            # Test with different settings
            r.adjust_for_ambient_noise(source, duration=1)
            
            # Lower energy threshold for more sensitive detection
            original_threshold = r.energy_threshold
            r.energy_threshold = 300  # Lower threshold
            
            print(f"   Energy threshold: {r.energy_threshold} (original: {original_threshold})")
            
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            print("🔄 Processing with optimized settings...")
            
            # Try multiple recognition attempts
            languages = ['en-US', 'fi-FI']
            for lang in languages:
                try:
                    result = r.recognize_google(audio, language=lang, show_all=True)
                    print(f"   {lang}: {result}")
                    
                    # Also try simple recognition
                    text = r.recognize_google(audio, language=lang)
                    print(f"   ✅ {lang} SUCCESS: '{text}'")
                    return True
                    
                except sr.UnknownValueError:
                    print(f"   ❌ {lang}: Could not understand")
                except sr.RequestError as e:
                    print(f"   ❌ {lang}: Error - {e}")
                    
    except Exception as e:
        print(f"❌ Settings test error: {e}")
    
    return False

def test_with_recorded_audio():
    """Test with the previously recorded audio"""
    print("\n🔄 Testing with Recorded Audio")
    print("=" * 30)
    
    # Check if we have a recording from the record_repeat test
    test_file = "/tmp/mic_test.wav"
    if os.path.exists(test_file):
        print(f"Found test recording: {test_file}")
        
        # Analyze the recording
        analyze_audio_file(test_file)
        
        # Try STT on the recording
        r = sr.Recognizer()
        try:
            with sr.AudioFile(test_file) as source:
                audio = r.record(source)
                
            print("🔄 Testing STT on recorded audio...")
            
            # Try recognition
            for lang in ['en-US', 'fi-FI']:
                try:
                    text = r.recognize_google(audio, language=lang)
                    print(f"   ✅ {lang}: '{text}'")
                except sr.UnknownValueError:
                    print(f"   ❌ {lang}: Could not understand")
                except sr.RequestError as e:
                    print(f"   ❌ {lang}: Error - {e}")
                    
        except Exception as e:
            print(f"❌ Recorded audio test error: {e}")
    else:
        print("No test recording found")

def main():
    """Main diagnostic function"""
    print("🔍 STT Comprehensive Diagnostic")
    print("=" * 50)
    
    # Test 1: Microphone devices
    best_device, success_text = test_microphone_devices()
    
    if success_text:
        print(f"\n🎉 SUCCESS! Device {best_device} recognized: '{success_text}'")
        print("STT is working - the issue may be with specific test conditions")
    else:
        print("\n⚠️  No device successfully recognized speech")
        
        # Test 2: Recognition settings
        if test_recognition_settings():
            print("🎉 SUCCESS with optimized settings!")
        else:
            # Test 3: Recorded audio
            test_with_recorded_audio()
            
            print("\n🔧 Troubleshooting Recommendations:")
            print("1. Speak MUCH louder and closer to microphone")
            print("2. Try simple English words: 'hello', 'test', 'one two three'")
            print("3. Ensure microphone is not muted")
            print("4. Check if microphone works with other applications")
            print("5. Try different microphone if available")

if __name__ == "__main__":
    main()