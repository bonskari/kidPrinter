#!/usr/bin/env python3
"""
Test TTS with environment variables to force correct audio output
"""

import os
import tempfile
import pygame
import time
from gtts import gTTS

def test_tts_with_alsa():
    """Test TTS with ALSA environment variables"""
    print("🔊 Testing TTS with ALSA environment variables...")
    
    # Set environment variables for ALSA
    os.environ['SDL_AUDIODRIVER'] = 'alsa'
    os.environ['ALSA_DEVICE'] = 'hw:2,0'
    
    text = "Hei! Kuuletko minut nyt kaiuttimista?"
    
    try:
        # Create TTS
        tts = gTTS(text=text, lang='fi', slow=True)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            
            print(f"TTS file saved: {tmp_file.name}")
            
            # Try pygame with ALSA settings
            try:
                pygame.mixer.quit()  # Make sure it's clean
                pygame.mixer.pre_init(devicename='hw:2,0')
                pygame.mixer.init()
                
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.quit()
                print("✅ ALSA pygame test completed")
                
            except Exception as e:
                print(f"❌ ALSA pygame failed: {e}")
                
                # Fallback to default pygame
                print("Trying default pygame...")
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.quit()
                print("✅ Default pygame completed")
            
            # Clean up
            os.unlink(tmp_file.name)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_tts_with_alsa()