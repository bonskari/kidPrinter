import subprocess
import time
import os

RECORD_SECONDS = 5
OUTPUT_FILENAME = "raw_recorded_test.wav"
MIC_DEVICE = "mic_boosted"
PLAYBACK_DEVICE = "hw:2,0"
SAMPLE_RATE = 48000
CHANNELS = 1

def record_audio_arecord():
    print(f"🎤 Recording from {MIC_DEVICE} for {RECORD_SECONDS} seconds...")
    command = [
        "arecord",
        "-D", MIC_DEVICE,
        "-f", "S16_LE",  # Signed 16-bit Little Endian
        "-r", str(SAMPLE_RATE),
        "-c", str(CHANNELS),
        "-d", str(RECORD_SECONDS),
        OUTPUT_FILENAME
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Saved recording to {OUTPUT_FILENAME}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error recording: {e}")
        return False

from pydub import AudioSegment

def play_audio_mpg123():
    print(f"🔊 Playing {OUTPUT_FILENAME} using mpg123...")
    mp3_filename = OUTPUT_FILENAME.replace(".wav", ".mp3")
    try:
        audio = AudioSegment.from_wav(OUTPUT_FILENAME)
        audio.export(mp3_filename, format="mp3", bitrate="192k")
        print(f"✅ Converted {OUTPUT_FILENAME} to MP3: {mp3_filename}")
        subprocess.run(['mpg123', '-a', PLAYBACK_DEVICE, mp3_filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🔊 Playback finished.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error playing: {e}")
        return False
    except FileNotFoundError:
        print("❌ mpg123 command not found. Please ensure mpg123 is installed.")
        return False
    except Exception as e:
        print(f"❌ Playback error: {e}")
        return False

def main():
    if record_audio_arecord():
        # Give a moment for the file to be written
        time.sleep(0.5)
        play_audio_mpg123()

if __name__ == "__main__":
    main()
