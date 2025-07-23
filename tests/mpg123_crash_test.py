import subprocess
import os

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
    print("🎵 mpg123 Crash Test")
    print("=" * 40)

    test_mp3_file = "assets/audio/finnish_test_sound.mp3"
    speaker_device = "hw:2,0"

    if not os.path.exists(test_mp3_file):
        print(f"❌ Test MP3 file not found: {test_mp3_file}")
    else:
        play_audio_mpg123(test_mp3_file, device=speaker_device)

    print("\nTest complete.")
