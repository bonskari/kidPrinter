#!/usr/bin/env python3
"""
STT test with listening sound cue
"""

import speech_recognition as sr
import subprocess
import tempfile
import time
import math
import wave
import os

def play_listening_sound():
    """Play a sound to indicate listening has started"""
    print("🔊 Playing listening sound...")
    
    # Create a higher pitch beep for "listening"
    beep_file = "/tmp/listening_beep.wav"
    
    # Create a 1200Hz tone for 0.2 seconds at reduced volume
    sample_rate = 44100
    duration = 0.2
    frequency = 1200
    volume = 0.4
    
    # Generate sine wave
    samples = []
    for i in range(int(sample_rate * duration)):
        sample = int(32767 * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
        samples.append(sample)
    
    # Write to WAV file
    with wave.open(beep_file, 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        for sample in samples:
            wav_file.writeframes(sample.to_bytes(2, byteorder='little', signed=True))
            wav_file.writeframes(sample.to_bytes(2, byteorder='little', signed=True))  # Duplicate for stereo
    
    # Play the beep through speakers
    try:
        subprocess.run(["aplay", "-D", "hw:2,0", beep_file], capture_output=True, timeout=3)
    except Exception as e:
        print(f"Listening sound failed: {e}")
    
    # Clean up
    if os.path.exists(beep_file):
        os.remove(beep_file)

def test_stt_with_sound():
    """Test STT with listening sound"""
    print("🎤 STT Test with Listening Sound")
    print("=" * 35)
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("🔧 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            # Play listening sound
            play_listening_sound()
            
            print("🎤 LISTENING NOW - Speak clearly!")
            print("   Try: 'HELLO WORLD' or 'TEST TEST'")
            
            # Listen for speech
            audio = r.listen(source, timeout=8, phrase_time_limit=5)
            
            print("🔄 Processing speech...")
            
            # Try recognition
            recognized = False
            
            try:
                text = r.recognize_google(audio, language='en-US')
                print(f"✅ English: '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("❌ English: Could not understand")
            except sr.RequestError as e:
                print(f"❌ English: Error - {e}")
            
            try:
                text = r.recognize_google(audio, language='fi-FI')
                print(f"✅ Finnish: '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("❌ Finnish: Could not understand")
            except sr.RequestError as e:
                print(f"❌ Finnish: Error - {e}")
            
            if not recognized:
                print("💡 STT Tips:")
                print("   - Speak VERY loudly")
                print("   - Get closer to microphone")
                print("   - Try simple English words")
                print("   - Check internet connection")
                
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_stt_with_sound()