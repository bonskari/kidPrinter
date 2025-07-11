#!/usr/bin/env python3
"""
Simple record and repeat test for the kid printer audio system
Records 3 seconds from USB microphone and plays it back through ROG Hive speakers
"""

import subprocess
import time
import os
import math
import wave

def record_and_repeat():
    """Record 3 seconds and immediately play it back"""
    
    # File path for temporary recording
    audio_file = "/tmp/record_repeat.wav"
    
    # Remove old recording if it exists
    if os.path.exists(audio_file):
        os.remove(audio_file)
    
    print("🎤 Get ready to speak...")
    time.sleep(1)
    
    # Play audio cue to signal start of recording
    print("🔊 Playing start beep...")
    
    # Generate a simple beep tone
    beep_file = "/tmp/beep.wav"
    
    # Create a 600Hz tone for 0.3 seconds at reduced volume
    sample_rate = 44100
    duration = 0.3
    frequency = 600
    volume = 0.3  # Reduced volume (30% of max)
    
    # Generate sine wave with volume control
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
    
    # Play the beep
    try:
        subprocess.run(["aplay", "-D", "hw:2,0", beep_file], capture_output=True, timeout=3)
        time.sleep(0.2)
        # Play again for double beep
        subprocess.run(["aplay", "-D", "hw:2,0", beep_file], capture_output=True, timeout=3)
    except Exception as e:
        print(f"Audio cue failed: {e}")
    
    # Clean up beep file
    if os.path.exists(beep_file):
        os.remove(beep_file)
    
    time.sleep(0.5)  # Small pause after beep
    
    print("🔴 Recording for 3 seconds - speak now!")
    
    # Record 3 seconds from USB microphone
    record_cmd = [
        "arecord",
        "-D", "plughw:1,0",  # USB microphone
        "-f", "cd",          # CD quality (44.1kHz, 16-bit, stereo)
        "-t", "wav",         # WAV format
        "-d", "3",           # 3 seconds duration
        audio_file
    ]
    
    try:
        # Start recording
        result = subprocess.run(record_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Recording complete!")
            
            # Small pause before playback
            time.sleep(0.5)
            
            print("🔊 Playing back your recording...")
            
            # Play back through ROG Hive speakers
            playback_cmd = [
                "aplay",
                "-D", "hw:2,0",  # ROG Hive speakers
                audio_file
            ]
            
            result = subprocess.run(playback_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Playback complete!")
            else:
                print(f"❌ Playback failed: {result.stderr}")
                
        else:
            print(f"❌ Recording failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Clean up
    if os.path.exists(audio_file):
        os.remove(audio_file)

if __name__ == "__main__":
    print("🎵 Record and Repeat Test")
    print("=" * 30)
    record_and_repeat()
    print("Test complete!")