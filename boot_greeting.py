import os
import subprocess
import gtts

BOOT_GREETING_TEXT = "Tulostinrobotti on valmiina toimintaan."
AUDIO_FILE_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'audio', 'boot_greeting.mp3')

def create_tts_audio(text, lang='fi'):
    """Creates an MP3 file from text using gTTS."""
    try:
        tts = gtts.gTTS(text=text, lang=lang, slow=False)
        tts.save(AUDIO_FILE_PATH)
        print(f"Generated TTS audio to {AUDIO_FILE_PATH}")
        return True
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return False

def play_greeting():
    if not os.path.exists(AUDIO_FILE_PATH):
        print("Boot greeting audio not found. Generating...")
        if not create_tts_audio(BOOT_GREETING_TEXT, lang='fi'):
            print("Failed to generate boot greeting audio. Aborting playback.")
            return

    try:
        subprocess.run(['mpg123', '-a', 'kidprinter_playback', AUDIO_FILE_PATH], check=True)
    except FileNotFoundError:
        print("Error: mpg123 not found. Please install it.")
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")

if __name__ == "__main__":
    play_greeting()