import pyaudio
import numpy as np
import time

# Configuration
CHUNK = 1024  # Record in chunks of 1024 samples
FORMAT = pyaudio.paInt16  # 16-bit samples
CHANNELS = 1  # Mono
RATE = 44100  # Record at 44100 samples per second

# Function to create an ASCII bar graph
def create_bar_graph(rms, max_rms=500, bar_length=50):
    # Normalize RMS to a 0-1 range based on max_rms
    normalized_rms = min(rms / max_rms, 1.0)
    # Calculate the number of filled characters for the bar
    num_filled = int(normalized_rms * bar_length)
    num_empty = bar_length - num_filled
    bar = '█' * num_filled + '-' * num_empty
    return f"[{bar}]"

# Find the correct input device index for "USB PnP Sound Device: Audio (hw:1,0)"
def find_input_device_index(p, device_name):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['name'] == device_name and info['maxInputChannels'] > 0:
            return i
    return -1

print("🎵 Microphone Level Test with Visualizer")
print("=" * 40)
print("Listening for audio input levels (RMS) and displaying a bar graph. Press Ctrl+C to stop.")

p = pyaudio.PyAudio()

mic_name = "mic_boosted"
input_device_index = find_input_device_index(p, mic_name)

if input_device_index == -1:
    print(f"❌ Microphone '{mic_name}' not found or has no input channels.")
    print("Available input devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"  {i}: {info['name']}")
    p.terminate()
    exit()

print(f"🎤 Recording from '{mic_name}' (device_index={input_device_index})...")

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=input_device_index)

start_time = time.time()

try:
    while (time.time() - start_time) < 10:
        data = stream.read(CHUNK, exception_on_overflow=False)
        np_data = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(np_data**2))
        if np.isnan(rms):
            rms = 0
        bar_graph = create_bar_graph(rms)
        print(f"RMS: {rms:7.2f} {bar_graph}")
        time.sleep(0.01) # Small delay to prevent overwhelming the console
except KeyboardInterrupt:
    print("\nStopping microphone test.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()