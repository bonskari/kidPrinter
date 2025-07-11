#!/usr/bin/env python3
"""
Test TTS with aplay to ensure audio goes to ROG Hive speakers
"""

import os
import sys
import tempfile
import subprocess
from gtts import gTTS

def test_tts_with_aplay():
    """Test TTS using aplay to ROG Hive speakers"""
    print("🔊 Testing TTS with aplay to ROG Hive speakers...")
    
    text = "Hei! Kuuletko minut nyt? Puhun suomea ROG Hive kaiuttimien kautta."
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            print(f"TTS saved: {tmp_file.name}")
            
            # Convert MP3 to WAV for aplay
            wav_file = tmp_file.name.replace('.mp3', '.wav')
            
            # Use ffmpeg to convert (if available)
            try:
                print("Converting MP3 to WAV...")
                subprocess.run(['ffmpeg', '-i', tmp_file.name, '-acodec', 'pcm_s16le', 
                              '-ar', '44100', wav_file], 
                             capture_output=True, check=True)
                
                print("Playing through ROG Hive speakers...")
                # Play through ROG Hive speakers
                subprocess.run(['aplay', '-D', 'hw:2,0', wav_file], 
                             capture_output=True, timeout=15)
                
                print("✅ TTS playback completed via aplay")
                
                # Clean up
                os.unlink(wav_file)
                
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"❌ ffmpeg/aplay failed: {e}")
                print("Trying alternative method...")
                
                # Try mpg123 directly to hw:2,0
                try:
                    subprocess.run(['mpg123', '-a', 'hw:2,0', tmp_file.name], 
                                 capture_output=True, timeout=15)
                    print("✅ TTS playback completed via mpg123")
                except:
                    print("❌ mpg123 also failed")
            
            # Clean up
            os.unlink(tmp_file.name)
            
    except Exception as e:
        print(f"❌ TTS test failed: {e}")

if __name__ == "__main__":
    test_tts_with_aplay()