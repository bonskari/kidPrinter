#!/usr/bin/env python3
"""
USB Microphone Speech-to-Text Test Application
Tests microphone input and converts speech to text
"""

import speech_recognition as sr
import pyaudio
import sys
import time

def list_audio_devices():
    """List available audio input devices"""
    p = pyaudio.PyAudio()
    print("Available Audio Devices:")
    print("-" * 40)
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:  # Only show input devices
            print(f"Device {i}: {info['name']}")
            print(f"  Max Input Channels: {info['maxInputChannels']}")
            print(f"  Default Sample Rate: {info['defaultSampleRate']}")
            print()
    
    p.terminate()

def test_microphone_basic():
    """Test basic microphone functionality"""
    print("Testing microphone accessibility...")
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Test microphone list
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"Found {len(mic_list)} microphones:")
        for i, name in enumerate(mic_list):
            print(f"  {i}: {name}")
        print()
        return True
    except Exception as e:
        print(f"Error accessing microphones: {e}")
        return False

def speech_to_text_continuous():
    """Continuous speech recognition - speaks everything you say"""
    print("Starting continuous speech recognition...")
    print("Speak into your microphone. Press Ctrl+C to stop.")
    print("=" * 50)
    
    r = sr.Recognizer()
    
    # Try to use the default microphone
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening... (ambient noise adjusted)")
            print()
    except Exception as e:
        print(f"Error setting up microphone: {e}")
        return
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Listen for audio with a timeout
                audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
            print("Processing speech...")
            
            # Try different speech recognition services
            try:
                # Google Speech Recognition (requires internet)
                text = r.recognize_google(audio, language='fi-FI')
                print(f"Google (Finnish): {text}")
            except sr.UnknownValueError:
                print("Google: Could not understand audio")
            except sr.RequestError as e:
                print(f"Google: Error - {e}")
            
            try:
                # Google Speech Recognition (English as fallback)
                text = r.recognize_google(audio, language='en-US')
                print(f"Google (English): {text}")
            except sr.UnknownValueError:
                print("Google: Could not understand audio")
            except sr.RequestError as e:
                print(f"Google: Error - {e}")
            
            print("-" * 30)
            
        except sr.WaitTimeoutError:
            pass  # No speech detected, continue listening
        except KeyboardInterrupt:
            print("\nStopping speech recognition...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

def main():
    """Main test function"""
    print("USB Microphone Speech-to-Text Test")
    print("=" * 40)
    
    # List available audio devices
    list_audio_devices()
    
    # Test microphone basic functionality
    if not test_microphone_basic():
        print("Microphone test failed. Check if microphone is connected.")
        return
    
    print("Choose test mode:")
    print("1. Continuous speech recognition")
    print("2. Exit")
    
    try:
        choice = input("Enter choice (1-2): ").strip()
        
        if choice == "1":
            speech_to_text_continuous()
        elif choice == "2":
            print("Exiting...")
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()