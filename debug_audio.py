#!/usr/bin/env python3
"""
Debug audio devices and microphone detection
"""

import speech_recognition as sr
import pyaudio
import sys

def debug_pyaudio():
    """Debug PyAudio device detection"""
    print("PyAudio Device Detection:")
    print("-" * 40)
    
    p = pyaudio.PyAudio()
    
    print(f"Total devices: {p.get_device_count()}")
    
    for i in range(p.get_device_count()):
        try:
            info = p.get_device_info_by_index(i)
            print(f"Device {i}:")
            print(f"  Name: {info['name']}")
            print(f"  Input Channels: {info['maxInputChannels']}")
            print(f"  Output Channels: {info['maxOutputChannels']}")
            print(f"  Sample Rate: {info['defaultSampleRate']}")
            print(f"  Host API: {info['hostApi']}")
            print()
        except Exception as e:
            print(f"Error getting device {i}: {e}")
    
    p.terminate()

def debug_speech_recognition():
    """Debug SpeechRecognition microphone detection"""
    print("SpeechRecognition Microphone Detection:")
    print("-" * 40)
    
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"Found {len(mic_list)} microphones:")
        for i, name in enumerate(mic_list):
            print(f"  {i}: {name}")
        print()
        
        # Try to use default microphone
        r = sr.Recognizer()
        print("Testing default microphone access...")
        
        with sr.Microphone() as source:
            print("✓ Default microphone accessible")
            print(f"Device index: {source.device_index}")
            print(f"Sample rate: {source.SAMPLE_RATE}")
            print(f"Chunk size: {source.CHUNK}")
            
    except Exception as e:
        print(f"Error: {e}")

def test_microphone_recording():
    """Test basic microphone recording"""
    print("Testing Microphone Recording:")
    print("-" * 40)
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Microphone is accessible")
            print("Testing ambient noise adjustment...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("✓ Ambient noise adjustment successful")
            
            print("Testing audio capture (2 seconds)...")
            audio = r.listen(source, timeout=2, phrase_time_limit=2)
            print("✓ Audio capture successful")
            print(f"Audio data length: {len(audio.get_raw_data())} bytes")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main debug function"""
    print("Audio System Debug")
    print("=" * 50)
    
    debug_pyaudio()
    debug_speech_recognition()
    test_microphone_recording()

if __name__ == "__main__":
    main()