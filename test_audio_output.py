#!/usr/bin/env python3
"""
Test audio output - check which device TTS is using
"""

import subprocess
import tempfile
from gtts import gTTS

def test_audio_routing():
    """Test where TTS audio is going"""
    print("🔊 Audio Routing Test")
    
    # Create a simple test phrase
    text = "Audio test - kuuletko minut?"
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            
            print(f"TTS file created: {tmp_file.name}")
            print("File size:", os.path.getsize(tmp_file.name), "bytes")
            
            # Try playing with different methods
            print("\n1. Testing with system default...")
            # This might go to the wrong speakers
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.play()
            
            import time
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            print("   Did you hear that? (probably not)")
            
            time.sleep(2)
            
            print("\n2. Manual check - file saved to:", tmp_file.name)
            print("   You could manually test this file if needed")
            
            # Clean up
            import os
            os.unlink(tmp_file.name)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_audio_routing()