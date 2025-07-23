import pyaudio
import numpy as np
import time
import subprocess
import threading

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
TEST_DURATION_SECONDS = 3
PLAYBACK_FILE = "stereo_boosted_mic_test.wav"

def find_input_device_index(p, device_name):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if device_name in info['name'] and info['maxInputChannels'] > 0:
            return i
    return -1

def measure_rms(p, device_index, duration_seconds):
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration_seconds)):
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except IOError as e:
            if e.errno != pyaudio.paInputOverflowed:
                raise

    stream.stop_stream()
    stream.close()

    np_data = np.frombuffer(b"".join(frames), dtype=np.int16)
    rms = np.sqrt(np.mean(np.square(np_data.astype(float))))
    return rms if not np.isnan(rms) else 0

def play_audio(filename):
    try:
        print(f"🔊 Playing {filename}... Press Ctrl+C to stop playback.")
        subprocess.run(["aplay", "-D", "hw:2,0", filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🔊 Playback finished.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error playing file: {e}")
    except KeyboardInterrupt:
        print("\n🔊 Playback stopped by user.")

def main():
    p = pyaudio.PyAudio()
    mic_name = "mic_boosted"
    input_device_index = find_input_device_index(p, mic_name)

    if input_device_index == -1:
        print(f"❌ Microphone '{mic_name}' not found.")
        p.terminate()
        return

    print("--- Audio Loopback Test ---")

    # 1. Measure ambient noise
    print(f"🎤 Measuring ambient noise for {TEST_DURATION_SECONDS} seconds... (Please be quiet)")
    ambient_rms = measure_rms(p, input_device_index, TEST_DURATION_SECONDS)
    print(f"✅ Ambient RMS: {ambient_rms:.2f}")

    print("\n" + "="*30 + "\n")

    # 2. Play sound and measure simultaneously
    playback_thread = threading.Thread(target=play_audio, args=(PLAYBACK_FILE,))

    print(f"🎤 Measuring microphone while playing sound for {TEST_DURATION_SECONDS} seconds...")

    playback_thread.start()
    time.sleep(0.5) # Give playback a moment to start
    playback_rms = measure_rms(p, input_device_index, TEST_DURATION_SECONDS)
    playback_thread.join()

    print(f"✅ Playback RMS: {playback_rms:.2f}")

    print("\n" + "="*30 + "\n")

    # 3. Compare results
    print("--- Results ---")
    print(f"Ambient Noise RMS: {ambient_rms:.2f}")
    print(f"Playback RMS:      {playback_rms:.2f}")

    if playback_rms > ambient_rms * 1.5:
        print("\n🎉 SUCCESS: Microphone clearly detected the speaker output.")
        print(f"The volume during playback was {playback_rms/ambient_rms:.1f} times louder than ambient noise.")
    else:
        print("\n❌ FAILURE: Microphone did not clearly detect the speaker output.")

    p.terminate()

if __name__ == "__main__":
    main()
