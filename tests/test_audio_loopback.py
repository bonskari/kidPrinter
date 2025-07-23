#!/usr/bin/env python3

import speech_recognition as sr
import subprocess
import tempfile
import time
import os
import numpy as np
import wave
import gtts

def create_tts_audio(text, lang='en'):
    try:
        tts = gtts.gTTS(text=text, lang=lang, slow=True)
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        tts.save(mp3_file)
        return mp3_file
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return None

def play_audio(file_path, device='hw:2,0'):
    try:
        subprocess.run(['mpg123', '-a', device, file_path], check=True, timeout=10)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Playback failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ mpg123 command not found. Please ensure mpg123 is installed.")
        return False
    except Exception as e:
        print(f"❌ Playback error: {e}")
        return False

def record_and_playback_test(phrase, tts_lang, mic_name="USB PnP Sound Device: Audio (hw:1,0)"):
    print(f"\n🧪 Testing phrase: '{phrase}'")
    
    # 1. Create TTS audio
    tts_mp3_file = create_tts_audio(phrase, tts_lang)
    if not tts_mp3_file:
        return False

    # 2. Play TTS audio
    print("   🔊 Playing TTS through speakers...")
    if not play_audio(tts_mp3_file):
        os.unlink(tts_mp3_file)
        return False
    os.unlink(tts_mp3_file) # Clean up TTS mp3

    time.sleep(1) # Give some time for sound to settle

    # 3. Record audio from microphone
    r = sr.Recognizer()
    mic_index = -1
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if name == mic_name:
            mic_index = index
            break
    
    if mic_index == -1:
        print(f"   ❌ Microphone '{mic_name}' not found.")
        return False

    recorded_wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print(f"   🎤 Recording from {mic_name} (device_index={mic_index})...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            with wave.open(recorded_wav_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(source.SAMPLE_WIDTH)
                wf.setframerate(source.SAMPLE_RATE)
                wf.writeframes(audio.frame_data)
        print("   ✅ Recording complete.")
    except Exception as e:
        print(f"   ❌ Recording failed: {e}")
        if os.path.exists(recorded_wav_file):
            os.unlink(recorded_wav_file)
        return False

    # 4. Play back recorded audio
    recorded_mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
    try:
        subprocess.run(['ffmpeg', '-i', recorded_wav_file, '-q:a', '2', recorded_mp3_file],
                       capture_output=True, check=True, timeout=10)
        print(f"   🔊 Playing back recorded audio from {recorded_mp3_file}...")
        if not play_audio(recorded_mp3_file):
            return False
        print("   ✅ Playback of recorded audio complete.")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ ffmpeg conversion failed: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("❌ ffmpeg command not found. Please ensure ffmpeg is installed.")
        return False
    except Exception as e:
        print(f"   ❌ Playback of recorded audio failed: {e}")
        return False
    finally:
        os.unlink(recorded_wav_file)
        if os.path.exists(recorded_mp3_file):
            os.unlink(recorded_mp3_file)

    # 5. User confirmation
    heard_playback = input("   Did you hear the recorded audio playback? (yes/no): ").lower()
    if heard_playback == 'yes':
        print("   ✅ User confirmed playback.")
        return True
    else:
        print("   ❌ User did not confirm playback.")
        return False

if __name__ == "__main__":
    print("🎵 Audio Loopback Test with User Confirmation")
    print("=" * 40)

    test_phrases = [
        ("Hello world", "en"),
        ("Tämä on testi", "fi"),
    ]

    all_tests_passed = True
    for phrase, lang in test_phrases:
        if not record_and_playback_test(phrase, lang):
            all_tests_passed = False
            break
    
    if all_tests_passed:
        print("\n🎉 All audio loopback tests passed!")
    else:
        print("\n⚠️  Some audio loopback tests failed. Please check your audio setup.")
