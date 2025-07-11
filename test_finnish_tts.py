#!/usr/bin/env python3
"""
Test just the Finnish TTS functionality without speech recognition
"""

import os
import sys
import tempfile
import time
import pygame
from gtts import gTTS

def test_finnish_speech():
    """Test Finnish TTS output"""
    
    # Test phrases
    phrases = [
        "Hei! Olen tulostinrobotti.",
        "Sano mitä haluat tulostaa.",
        "Tulostan sinulle kuvan.",
        "Tulostus valmis!"
    ]
    
    print("Testing Finnish TTS...")
    
    for i, phrase in enumerate(phrases, 1):
        print(f"\n{i}. Testing: {phrase}")
        
        try:
            # Create TTS
            tts = gTTS(text=phrase, lang='fi', slow=False)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tts.save(tmp_file.name)
                print(f"   Saved audio: {os.path.getsize(tmp_file.name)} bytes")
                
                # Initialize pygame mixer
                pygame.mixer.init()
                
                # Load and play
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.quit()
                
                # Clean up
                os.unlink(tmp_file.name)
                print("   ✅ Playback completed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small pause between phrases
        time.sleep(1)
    
    print("\n🎉 Finnish TTS test completed!")

if __name__ == "__main__":
    test_finnish_speech()