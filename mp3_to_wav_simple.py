#!/usr/bin/env python3
"""
Simple MP3 to WAV converter using pygame
"""

import os
import tempfile
import pygame
import wave
import numpy as np

def convert_mp3_to_wav_simple(mp3_file, wav_file):
    """Convert MP3 to WAV using pygame"""
    try:
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Load the MP3 file
        sound = pygame.mixer.Sound(mp3_file)
        
        # Get raw audio data
        raw_data = pygame.sndarray.array(sound)
        
        # Convert to the right format for WAV
        if len(raw_data.shape) == 1:
            # Mono
            audio_data = raw_data.astype(np.int16)
            channels = 1
        else:
            # Stereo
            audio_data = raw_data.astype(np.int16)
            channels = 2
        
        # Write WAV file
        with wave.open(wav_file, 'w') as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(2)  # 16-bit
            wav.setframerate(22050)
            wav.writeframes(audio_data.tobytes())
        
        pygame.mixer.quit()
        return True
        
    except Exception as e:
        print(f"Conversion error: {e}")
        return False

def test_conversion():
    """Test the MP3 to WAV conversion"""
    mp3_file = "/tmp/tts_test.mp3"
    wav_file = "/tmp/tts_test.wav"
    
    if not os.path.exists(mp3_file):
        print("❌ MP3 file not found. Run test_tts_direct.py first.")
        return
    
    print("🔄 Converting MP3 to WAV...")
    
    if convert_mp3_to_wav_simple(mp3_file, wav_file):
        print(f"✅ WAV file created: {wav_file}")
        print(f"Size: {os.path.getsize(wav_file)} bytes")
        
        # Try to play through ROG Hive speakers
        print("🔊 Playing through ROG Hive speakers...")
        import subprocess
        result = subprocess.run(['aplay', '-D', 'hw:2,0', wav_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Playback successful!")
        else:
            print(f"❌ Playback failed: {result.stderr}")
    else:
        print("❌ Conversion failed")

if __name__ == "__main__":
    test_conversion()