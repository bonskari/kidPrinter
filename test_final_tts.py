#!/usr/bin/env python3
"""
Final TTS test with mpg123
"""

import os
import sys
import tempfile
import subprocess
from gtts import gTTS

def test_final_tts():
    """Test the final TTS implementation"""
    print("🔊 Final TTS Test with mpg123")
    
    phrases = [
        "Hei! Kuuletko minut nyt?",
        "Tämä on suomalainen robotti.",
        "Sano mitä haluat tulostaa.",
        "Tulostus valmis!"
    ]
    
    for i, phrase in enumerate(phrases, 1):
        print(f"\n{i}. Testing: {phrase}")
        
        try:
            # Create TTS
            tts = gTTS(text=phrase, lang='fi', slow=True)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tts.save(tmp_file.name)
                
                # Play through ROG Hive speakers using mpg123
                result = subprocess.run(['mpg123', '-a', 'hw:2,0', tmp_file.name], 
                                     capture_output=True, timeout=15)
                
                if result.returncode == 0:
                    print("   ✅ TTS playback successful")
                else:
                    print(f"   ❌ TTS failed: {result.stderr.decode()}")
                
                # Clean up
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small pause between phrases
        import time
        time.sleep(1)
    
    print("\n🎉 Final TTS test completed!")

if __name__ == "__main__":
    test_final_tts()