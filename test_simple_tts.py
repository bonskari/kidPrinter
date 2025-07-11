#!/usr/bin/env python3
"""
Simple TTS test - check if we can hear anything
"""

import os
import time
import tempfile
import pygame
from gtts import gTTS

def simple_tts_test():
    """Simple TTS test"""
    print("🔊 Simple TTS Test")
    
    text = "Hei! Testaan ääntä."
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            print(f"TTS saved: {os.path.getsize(tmp_file.name)} bytes")
            
            # Test 1: Default pygame
            print("Test 1: Default pygame...")
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            print("✅ Default pygame completed")
            
            time.sleep(1)
            
            # Test 2: Try with different pygame settings
            print("Test 2: Pygame with specific settings...")
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2)
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.set_volume(1.0)  # Max volume
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            print("✅ Pygame with settings completed")
            
            # Clean up
            os.unlink(tmp_file.name)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_tts_test()