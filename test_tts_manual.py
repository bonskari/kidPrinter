#!/usr/bin/env python3
"""
Manual TTS test - you confirm when you hear it
"""

import gtts
import tempfile
import subprocess
import os
import time

def test_tts_manually():
    """Test TTS with manual confirmation"""
    print("🔊 Manual TTS Test")
    print("=" * 20)
    
    phrases = [
        ("Hello world", "en"),
        ("Test one two three", "en"),
        ("Moi maailma", "fi"),
        ("Tulosta kuva kissasta", "fi")
    ]
    
    for i, (text, lang) in enumerate(phrases):
        print(f"\n🧪 Test {i+1}/4: '{text}' ({lang})")
        
        try:
            # Create TTS
            print("   🗣️  Creating TTS...")
            tts = gtts.gTTS(text=text, lang=lang, slow=True)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tts.save(tmp.name)
                
                # Play TTS
                print("   🔊 Playing TTS... (listen now!)")
                result = subprocess.run(['mpg123', '-a', 'hw:2,0', tmp.name], 
                                      capture_output=True, timeout=10)
                
                if result.returncode == 0:
                    print("   ✅ TTS playback completed")
                    
                    # Ask user if they heard it
                    heard = input("   ❓ Did you hear the TTS? (y/n): ").strip().lower()
                    
                    if heard.startswith('y'):
                        print("   🎉 SUCCESS! TTS is working")
                        return True
                    else:
                        print("   ❌ TTS not heard")
                else:
                    print("   ❌ TTS playback failed")
                
                # Clean up
                os.unlink(tmp.name)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("🎯 Manual TTS Verification")
    print("=" * 30)
    print("This will play TTS through speakers")
    print("You confirm when you hear it")
    print()
    
    if test_tts_manually():
        print("\n✅ TTS system is working!")
        print("Next: Test the microphone input")
    else:
        print("\n⚠️  TTS system needs debugging")
        print("Check speaker connections and volume")