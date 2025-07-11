#!/usr/bin/env python3
"""
Test Finnish TTS functionality
"""

import os
import sys
import subprocess
import tempfile
import time

def test_google_tts():
    """Test Google TTS for Finnish"""
    print("Testing Google TTS for Finnish...")
    
    try:
        import gtts
        
        # Test text in Finnish
        text = "Hei! Olen tulostinrobotti. Sano mitä haluat tulostaa!"
        
        # Create TTS object
        tts = gtts.gTTS(text=text, lang='fi', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            print(f"Saving TTS to: {tmp_file.name}")
            tts.save(tmp_file.name)
            
            print(f"✅ TTS file created: {os.path.getsize(tmp_file.name)} bytes")
            
            # Try to play the file using different methods
            print("Attempting to play through speakers...")
            
            # Method 1: Try playing MP3 directly with aplay (won't work but let's see)
            try:
                print("Trying aplay...")
                result = subprocess.run(['aplay', '-D', 'hw:2,0', tmp_file.name], 
                                      capture_output=True, timeout=5)
                print("aplay result:", result.returncode)
            except Exception as e:
                print(f"aplay failed: {e}")
            
            # Method 2: Check if we can at least verify the file
            print(f"File exists: {os.path.exists(tmp_file.name)}")
            print(f"File size: {os.path.getsize(tmp_file.name)} bytes")
            
            # Method 3: Try using python to play (if pygame available)
            try:
                print("Trying pygame mixer...")
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                print("✅ Pygame playback completed")
            except ImportError:
                print("Pygame not available")
            except Exception as e:
                print(f"Pygame failed: {e}")
            
            # Clean up
            os.unlink(tmp_file.name)
            print("✅ Test completed")
            
    except ImportError:
        print("❌ gTTS not available")
    except Exception as e:
        print(f"❌ TTS test failed: {e}")

if __name__ == "__main__":
    test_google_tts()