import pyaudio
import wave
import numpy as np
import time
import sys
from pydub import AudioSegment

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

def find_input_device_index(p, device_name):
    """Finds the index of the audio device with the given name."""
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if device_name in info['name'] and info['maxInputChannels'] > 0:
            return i
    return -1

def record_audio(p, device_name, output_filename):
    """Records audio from a specified device and saves it to a WAV file."""
    device_index = find_input_device_index(p, device_name)
    if device_index == -1:
        print(f"❌ Microphone '{device_name}' not found.")
        return False

    print(f"🎤 Recording from '{device_name}' for {RECORD_SECONDS} seconds...")

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
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

def analyze_audio(filename):
    """Analyzes the given WAV file and prints its RMS value."""
    if not filename:
        return
    print(f"🔍 Analyzing {filename}...")
    try:
        audio = AudioSegment.from_wav(filename)
        print(f"  - RMS: {audio.rms}")
    except Exception as e:
        print(f"  - Error analyzing file: {e}")

def main():
    p = pyaudio.PyAudio()

    # --- Unboosted Mic ---
    unboosted_mic_name = "hw:1,0"
    unboosted_filename = "unboosted_mic_test.wav"
    if record_audio(p, unboosted_mic_name, unboosted_filename):
        analyze_audio(unboosted_filename)
    else:
        print("Could not test unboosted microphone.")


    print("\n" + "="*40 + "\n")

    # --- Boosted Mic ---
    boosted_mic_name = "mic_boosted"
    boosted_filename = "boosted_mic_test.wav"
    if record_audio(p, boosted_mic_name, boosted_filename):
        analyze_audio(boosted_filename)
    else:
        print("Could not test boosted microphone.")


    p.terminate()

if __name__ == "__main__":
    main()
