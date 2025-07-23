import pyaudio
import wave
import time
import subprocess

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Standard sample rate
RECORD_SECONDS = 5
OUTPUT_FILENAME = "simple_recorded_test.wav"

def find_input_device_index(p, device_name):
    """Finds the index of the audio device with the given name."""
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if device_name in info['name'] and info['maxInputChannels'] > 0:
            return i
    return -1

def record_audio(p, device_name, output_filename, duration):
    """Records audio from a specified device and saves it to a WAV file."""
    device_index = find_input_device_index(p, device_name)
    if device_index == -1:
        print(f"❌ Microphone '{device_name}' not found.")
        return False

    print(f"🎤 Recording from '{device_name}' for {duration} seconds...")

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"✅ Saved recording to {output_filename}")
    return True

def play_audio_aplay(file_path, device='hw:2,0'):
    """Plays a WAV audio file using aplay."""
    try:
        print(f"🔊 Playing {file_path} using aplay...")
        subprocess.run(['aplay', '-D', device, file_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🔊 Playback finished.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Playback failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ aplay command not found. Please ensure alsa-utils is installed.")
        return False
    except Exception as e:
        print(f"❌ Playback error: {e}")
        return False

def main():
    p = pyaudio.PyAudio()
    mic_name = "mic_boosted"

    if record_audio(p, mic_name, OUTPUT_FILENAME, RECORD_SECONDS):
        play_audio_aplay(OUTPUT_FILENAME)

    p.terminate()

if __name__ == "__main__":
    main()
