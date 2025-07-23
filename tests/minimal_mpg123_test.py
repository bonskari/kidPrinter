import subprocess
import tempfile
import os
import gtts

def create_tts_audio(text, lang='en'):
    try:
        tts = gtts.gTTS(text=text, lang=lang, slow=False)
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        tts.save(mp3_file)
        return mp3_file
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return None

def play_audio_mpg123(file_path, device='hw:2,0'):
    try:
        print(f"Attempting to play {file_path} on {device}...")
        subprocess.run(['mpg123', '-a', device, file_path], check=True, timeout=10)
        print("✅ Playback successful.")
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

if __name__ == "__main__":
    print("🎵 Minimal mpg123 Test")
    print("=" * 40)

    speaker_device = "hw:2,0"
    tts_text = "Hello, this is a minimal test sound."
    tts_mp3_file = create_tts_audio(tts_text, lang='en')

    if tts_mp3_file:
        play_audio_mpg123(tts_mp3_file, device=speaker_device)
        os.unlink(tts_mp3_file)

    print("\nTest complete.")
