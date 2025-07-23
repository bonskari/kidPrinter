#!/usr/bin/env python3
"""
Boot greeting script for Juuso's KidPrinter
Plays a Finnish greeting when the OS boots up
"""

import subprocess
import tempfile
import os
import time

def play_boot_greeting():
    """Play Finnish boot greeting for Juuso using Google TTS"""
    try:
        from gtts import gTTS
        
        # Finnish greeting for Juuso
        greeting = "Hei Juuso! Tulostinrobottisi on nyt käynnistynyt ja valmis toimimaan!"
        
        print(f"Playing boot greeting: {greeting}")
        
        # Create TTS object
        tts = gTTS(text=greeting, lang='fi', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            
            # Convert to WAV and play through ROG Hive speakers
            wav_file = tmp_file.name.replace('.mp3', '.wav')
            subprocess.run(['ffmpeg', '-i', tmp_file.name, '-acodec', 'pcm_s16le', 
                          '-ar', '44100', wav_file], capture_output=True, check=True)
            subprocess.run(['aplay', '-D', 'hw:2,0', wav_file], check=True)
            os.unlink(wav_file)
            
            # Cleanup
            os.unlink(tmp_file.name)
            
    except Exception as e:
        print(f"Error playing boot greeting: {e}")

if __name__ == "__main__":
    # Small delay to ensure audio system is ready
    time.sleep(3)
    play_boot_greeting()