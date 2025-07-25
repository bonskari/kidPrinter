import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

print("--- PyAudio Devices ---")
for i in range(0, num_devices):
    if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    if p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
        print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

p.terminate()