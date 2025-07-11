#!/usr/bin/env python3
"""
Fast TTS test - direct to speakers
"""

import os
import subprocess
import tempfile
from gtts import gTTS
from pydub import AudioSegment

def fast_tts_test():
    """Quick TTS test"""
    print("🚀 Fast TTS Test")
    
    text = "Hei! Kuuletko minut nyt?"
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            
            # Convert to WAV
            wav_file = tmp_file.name.replace('.mp3', '.wav')
            audio = AudioSegment.from_mp3(tmp_file.name)
            audio.export(wav_file, format="wav")
            
            # Play through speakers
            subprocess.run(['aplay', '-D', 'hw:2,0', wav_file], 
                         capture_output=True, timeout=10)
            
            # Clean up
            os.unlink(tmp_file.name)
            os.unlink(wav_file)
            
            print("✅ Fast TTS completed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fast_tts_test()