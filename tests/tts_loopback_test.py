import pyaudio
import wave
import numpy as np
import time
import subprocess
import threading
import os
from gtts import gTTS
from pydub import AudioSegment

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 7

TTS_TEXT = "Testing the microphone loopback with text to speech. This is a test."
TTS_FILENAME = "tts_test_audio.mp3"
RECORDED_FILENAME = "recorded_tts.wav"

def generate_tts(text, filename):
    """Generates TTS audio and saves it to a file, then resamples it to 44100 Hz."""
    print(f"Generating TTS: '{text}' to {filename}...")
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        print(f"✅ Generated {filename}")

        # Resample to 44100 Hz
        audio = AudioSegment.from_mp3(filename)
        audio = audio.set_frame_rate(44100)
        audio.export(filename, format="mp3")
        print(f"✅ Resampled {filename} to 44100 Hz.")
        return True
    except Exception as e:
        print(f"❌ Error generating or resampling TTS: {e}")
        return False

def record_audio_arecord(device_name, output_filename, duration):
    """Records audio from a specified device using arecord and saves it to a WAV file."""
    print(f"🎤 Recording from {device_name} for {duration} seconds using arecord...")
    command = [
        "arecord",
        "-D", device_name,
        "-f", "S16_LE",  # Signed 16-bit Little Endian
        "-r", str(RATE),
        "-c", str(CHANNELS),
        "-d", str(duration),
        output_filename
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Saved recording to {output_filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error recording with arecord: {e}")
        return False

def play_audio_mpg123(file_path, device='hw:2,0'):
    """Plays an MP3 audio file using mpg123."""
    try:
        print(f"🔊 Playing {file_path}...")
        subprocess.run(['mpg123', '-a', device, file_path], check=True, timeout=RECORD_SECONDS + 5) # Add buffer for playback
        print("🔊 Playback finished.")
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

def convert_wav_to_stereo_mp3(input_wav, output_mp3):
    """Converts a WAV file to stereo MP3."""
    try:
        audio = AudioSegment.from_wav(input_wav)
        stereo_audio = audio.set_channels(2)
        stereo_audio.export(output_mp3, format="mp3", bitrate="192k")
        print(f"✅ Converted {input_wav} to stereo MP3: {output_mp3}")
        return True
    except Exception as e:
        print(f"❌ Error converting {input_wav} to MP3: {e}")
        return False

def main():
    # 1. Generate TTS audio
    if not generate_tts(TTS_TEXT, TTS_FILENAME):
        return

    # 2. Play TTS and record microphone simultaneously
    mic_boosted_name = "mic_boosted"
    record_thread = threading.Thread(target=record_audio_arecord, args=(mic_boosted_name, RECORDED_FILENAME, RECORD_SECONDS))

    record_thread.start()
    time.sleep(0.5) # Give recording a moment to start
    play_audio_mpg123(TTS_FILENAME)
    record_thread.join()

    print("\n" + "="*40 + "\n")

    # 3. Play back recorded microphone audio
    recorded_mp3_filename = RECORDED_FILENAME.replace(".wav", ".mp3")
    if convert_wav_to_stereo_mp3(RECORDED_FILENAME, recorded_mp3_filename):
        play_audio_mpg123(recorded_mp3_filename)

if __name__ == "__main__":
    main()
