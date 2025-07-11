#!/usr/bin/env python3
"""
Direct TTS test - save file and let you manually test it
"""

import os
import tempfile
from gtts import gTTS

def create_tts_file():
    """Create TTS file for manual testing"""
    print("🔊 Creating TTS file for testing...")
    
    text = "Hei! Kuuletko minut nyt? Tämä on testi."
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to a known location
        tts_file = "/tmp/tts_test.mp3"
        tts.save(tts_file)
        
        print(f"✅ TTS file created: {tts_file}")
        print(f"File size: {os.path.getsize(tts_file)} bytes")
        
        print("\nTo test manually, try:")
        print(f"  aplay -D hw:2,0 {tts_file}")
        print("  (This won't work because aplay doesn't handle MP3)")
        
        print("\nOr try:")
        print(f"  mpg123 -a hw:2,0 {tts_file}")
        
        return tts_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    create_tts_file()