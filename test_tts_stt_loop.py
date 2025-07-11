#!/usr/bin/env python3
"""
TTS-STT Feedback Loop Test
TTS speaks through speakers, microphone records, STT recognizes
"""

import speech_recognition as sr
import subprocess
import tempfile
import time
import os
import numpy as np

def create_tts_audio(text, lang='en'):
    """Create TTS audio file"""
    try:
        import gtts
        
        # Create TTS
        tts = gtts.gTTS(text=text, lang=lang, slow=True)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return None

def play_tts_through_speakers(mp3_file):
    """Play TTS through ROG Hive speakers"""
    try:
        # Play through hw:2,0 (ROG Hive speakers)
        result = subprocess.run(['mpg123', '-a', 'hw:2,0', mp3_file], 
                               capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ TTS playback failed: {e}")
        return False

def test_stt_recognition(text_spoken, lang='en-US'):
    """Test if STT can recognize the spoken text"""
    r = sr.Recognizer()
    r.energy_threshold = 100  # Lower threshold
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("   🎤 Listening for recognition...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for the audio
            audio = r.listen(source, timeout=3, phrase_time_limit=8)
            
            # Check audio level
            raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            max_amp = np.max(np.abs(raw_data))
            level = max_amp / 32767 * 100
            
            print(f"   📊 Recorded level: {level:.1f}%")
            
            if max_amp < 500:
                print("   ⚠️  Audio too low")
                return False, "too_low"
            
            # Try recognition
            try:
                recognized = r.recognize_google(audio, language=lang)
                print(f"   🤖 Recognized: '{recognized}'")
                
                # Check if recognition matches
                if text_spoken.lower() in recognized.lower() or recognized.lower() in text_spoken.lower():
                    print("   ✅ MATCH!")
                    return True, recognized
                else:
                    print("   ❌ No match")
                    return False, recognized
                    
            except sr.UnknownValueError:
                print("   ❌ Could not understand")
                return False, "no_recognition"
            except sr.RequestError as e:
                print(f"   ❌ Recognition error: {e}")
                return False, f"error_{e}"
                
    except Exception as e:
        print(f"   ❌ STT error: {e}")
        return False, str(e)

def test_feedback_loop():
    """Test complete TTS-STT feedback loop"""
    print("🔄 TTS-STT Feedback Loop Test")
    print("=" * 35)
    
    # Test phrases
    test_phrases = [
        ("hello world", "en-US"),
        ("test one two three", "en-US"),
        ("moi maailma", "fi-FI"),  # Finnish: hello world
        ("testi yksi kaksi", "fi-FI"),  # Finnish: test one two
    ]
    
    success_count = 0
    total_tests = len(test_phrases)
    
    for i, (text, stt_lang) in enumerate(test_phrases):
        print(f"\n🧪 TEST {i+1}/{total_tests}: '{text}'")
        
        # Determine TTS language
        tts_lang = 'fi' if stt_lang == 'fi-FI' else 'en'
        
        # Create TTS audio
        print("   🗣️  Creating TTS...")
        mp3_file = create_tts_audio(text, tts_lang)
        if not mp3_file:
            print("   ❌ TTS creation failed")
            continue
        
        try:
            # Play TTS
            print("   🔊 Playing TTS through speakers...")
            if not play_tts_through_speakers(mp3_file):
                print("   ❌ TTS playback failed")
                continue
            
            # Wait a moment for audio to finish
            time.sleep(1)
            
            # Test STT recognition
            success, result = test_stt_recognition(text, stt_lang)
            
            if success:
                success_count += 1
                print(f"   🎉 SUCCESS! ({success_count}/{i+1})")
            else:
                print(f"   ❌ Failed: {result}")
                
        finally:
            # Clean up temp file
            try:
                os.unlink(mp3_file)
            except:
                pass
    
    print(f"\n📊 FINAL RESULTS: {success_count}/{total_tests} successful")
    
    if success_count == total_tests:
        print("🎉 PERFECT! Complete TTS-STT loop working!")
        return True
    elif success_count > 0:
        print("⚠️  Partial success - system working but needs tuning")
        return True
    else:
        print("❌ No success - system needs debugging")
        return False

if __name__ == "__main__":
    print("🎯 Complete TTS-STT System Test")
    print("=" * 40)
    print("Testing: TTS → Speakers → Microphone → STT")
    print()
    
    if test_feedback_loop():
        print("\n✅ Your Kid Printer audio system is working!")
        print("Ready for voice conversations!")
    else:
        print("\n⚠️  Audio system needs adjustment")
        print("Try adjusting speaker/microphone positioning")