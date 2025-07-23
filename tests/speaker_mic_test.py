
import pyaudio
import numpy as np
import time
import threading
import subprocess

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# --- Microphone Monitoring Thread ---
class MicMonitor(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        p = pyaudio.PyAudio()

        def find_input_device_index(p, device_name):
            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)
                if device_name in info['name'] and info['maxInputChannels'] > 0:
                    return i
            return -1

        mic_name = "mic_boosted"
        input_device_index = find_input_device_index(p, mic_name)

        if input_device_index == -1:
            print(f"❌ Microphone '{mic_name}' not found.")
            return

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=input_device_index)

        print("🎤 Monitoring microphone...")
        while not self._stop_event.is_set():
            data = stream.read(CHUNK, exception_on_overflow=False)
            np_data = np.frombuffer(data, dtype=np.int16)
            rms = np.sqrt(np.mean(np_data**2))
            if not np.isnan(rms):
                print(f"RMS: {rms:7.2f}")
            time.sleep(0.01)

        stream.stop_stream()
        stream.close()
        p.terminate()
        print("🎤 Microphone monitoring stopped.")

# --- Main Execution ---
def main():
    monitor_thread = MicMonitor()
    monitor_thread.start()

    print("🔊 Starting speaker test...")
    try:
        subprocess.run(["speaker-test", "-t", "wav", "-c", "2", "-D", "hw:2,0"], timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Run for 10 seconds
    except subprocess.TimeoutExpired:
        print("🔊 Speaker test finished.")
    except Exception as e:
        print(f"🔊 Speaker test failed: {e}")
    finally:
        monitor_thread.stop()
        monitor_thread.join()

if __name__ == "__main__":
    main()
