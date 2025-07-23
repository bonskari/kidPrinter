import os
import subprocess

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

if __name__ == "__main__":
    print("🎵 Playback Only Test")
    print("=" * 40)

    speaker_device = "hw:2,0"
    test_mp3_file = "assets/audio/finnish_test_sound.mp3"

    print(f"\nStep 1: Playing MP3 sound: '{test_mp3_file}'")
    if play_audio_mpg123(test_mp3_file, device=speaker_device):
        print("   Please confirm manually if you heard the playback.")
    else:
        print("   ❌ Failed to play MP3 sound.")

    print("\nTest complete.")