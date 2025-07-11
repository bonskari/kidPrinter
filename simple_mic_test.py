#!/usr/bin/env python3
"""
Simple USB Microphone Test - Auto-running version
"""

import speech_recognition as sr
import pyaudio
import sys
import time

def list_audio_devices():
    """List available audio input devices"""
    print("Available Audio Devices:")
    print("-" * 40)
    
    p = pyaudio.PyAudio()
    device_found = False
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            device_found = True
            print(f"Device {i}: {info['name']}")
            print(f"  Max Input Channels: {info['maxInputChannels']}")
            print(f"  Default Sample Rate: {info['defaultSampleRate']}")
            print()
    
    p.terminate()
    return device_found

def test_single_recognition():
    """Test single speech recognition"""
    print("Testing single speech recognition...")
    print("Say something now (you have 5 seconds)...")
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            
            # Listen for 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
        print("Processing speech...")
        
        # Try Finnish first
        try:
            text = r.recognize_google(audio, language='fi-FI')
            print(f"Recognized (Finnish): {text}")
            return True
        except sr.UnknownValueError:
            print("Finnish: Could not understand audio")
        except sr.RequestError as e:
            print(f"Finnish recognition error: {e}")
        
        # Try English as fallback
        try:
            text = r.recognize_google(audio, language='en-US')
            print(f"Recognized (English): {text}")
            return True
        except sr.UnknownValueError:
            print("English: Could not understand audio")
        except sr.RequestError as e:
            print(f"English recognition error: {e}")
            
        return False
        
    except sr.WaitTimeoutError:
        print("No speech detected within 5 seconds")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main test function"""
    print("Simple USB Microphone Test")
    print("=" * 40)
    
    # Check if devices are available
    if not list_audio_devices():
        print("No audio input devices found!")
        return
    
    # Test microphone list
    r = sr.Recognizer()
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"SpeechRecognition found {len(mic_list)} microphones:")
        for i, name in enumerate(mic_list):
            print(f"  {i}: {name}")
        print()
    except Exception as e:
        print(f"Error listing microphones: {e}")
        return
    
    # Test single recognition
    print("Ready to test speech recognition!")
    print("Make sure your USB microphone is connected and working.")
    print()
    
    success = test_single_recognition()
    
    if success:
        print("\n✓ Microphone test successful!")
        print("Your USB microphone is working with speech recognition.")
    else:
        print("\n✗ Microphone test failed.")
        print("Check your microphone connection and try speaking louder.")

if __name__ == "__main__":
    main()