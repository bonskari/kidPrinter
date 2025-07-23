import speech_recognition as sr
import subprocess
import tempfile
import time
import os
import numpy as np
import wave
import gtts
import random
from mutagen.mp3 import MP3

def create_tts_audio(text, lang='en'):
    try:
        tts = gtts.gTTS(text=text, lang=lang, slow=False)
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        tts.save(mp3_file)
        return mp3_file
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return None

def get_mp3_duration(file_path):
    try:
        audio = MP3(file_path)
        return audio.info.length
    except Exception as e:
        print(f"❌ Could not get MP3 duration: {e}")
        return 0

def play_audio_mpg123(file_path, device='hw:2,0'):
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

def record_audio(mic_name, duration):
    r = sr.Recognizer()
    mic_index = -1
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if name == mic_name:
            mic_index = index
            break
    
    if mic_index == -1:
        print(f"   ❌ Microphone '{mic_name}' not found.")
        return None, None, None

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print(f"   🎤 Recording from {mic_name} (device_index={mic_index}) for {duration:.2f} seconds...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=duration + 2, phrase_time_limit=duration + 1)
            return audio.frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH
    except Exception as e:
        print(f"   ❌ Recording failed: {e}")
        return None, None, None

def play_wav_data(wav_data, sample_rate, sample_width, device='hw:2,0'):
    recorded_wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    try:
        with wave.open(recorded_wav_file, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(wav_data)

        # Convert WAV to MP3 for mpg123 playback
        recorded_mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        subprocess.run(['ffmpeg', '-i', recorded_wav_file, '-q:a', '2', recorded_mp3_file],
                       capture_output=True, check=True, timeout=10)

        print(f"   🔊 Playing back recorded audio from {recorded_mp3_file}...")
        return play_audio_mpg123(recorded_mp3_file, device=device)
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
        if os.path.exists(recorded_wav_file):
            os.unlink(recorded_wav_file)
        if os.path.exists(recorded_mp3_file):
            os.unlink(recorded_mp3_file)

if __name__ == "__main__":
    print("🎵 Full Audio Loopback Test")
    print("=" * 40)

    mic_name = "USB PnP Sound Device: Audio (hw:1,0)"
    speaker_device = "hw:2,0"

    test_sentences = [
        "Hello, this is a test sentence.",
        "Can you hear me now?",
        "Testing one two three.",
        "Tämä on testilause.", # Finnish
        "Kuuluuko ääni?", # Finnish
    ]

    sentence = random.choice(test_sentences)
    tts_lang = 'fi' if "Tämä" in sentence or "Kuuluuko" in sentence else 'en'

    tts_mp3_file = create_tts_audio(sentence, lang=tts_lang)
    if not tts_mp3_file:
        exit()

    tts_duration = get_mp3_duration(tts_mp3_file)
    if tts_duration == 0:
        print("❌ Could not determine TTS duration. Exiting.")
        os.unlink(tts_mp3_file)
        exit()

    print(f"\nStep 1: Playing TTS sound: '{sentence}' (Duration: {tts_duration:.2f}s)")
    play_audio_mpg123(tts_mp3_file, device=speaker_device)
    os.unlink(tts_mp3_file) # Clean up TTS mp3

    time.sleep(0.5) # Small pause before recording

    print("\nStep 2: Recording from microphone.")
    # Record for slightly longer than TTS duration to capture full phrase
    recorded_data, sample_rate, sample_width = record_audio(mic_name, duration=tts_duration + 1.0)

    if recorded_data is not None:
        print("\nStep 3: Playing back recorded audio.")
        if play_wav_data(recorded_data, sample_rate, sample_width, device=speaker_device):
            heard_recorded = input("   Did you hear the TTS phrase in the playback? (yes/no): ").lower()
            if heard_recorded != 'yes':
                print("   ❌ User did not confirm hearing the recorded audio. Test failed.")
            else:
                print("   ✅ User confirmed hearing the recorded audio. Test successful!")
        else:
            print("   ❌ Failed to play back recorded audio. Test failed.")
    else:
        print("   ❌ Failed to record audio. Test failed.")

    print("\nTest complete.")
