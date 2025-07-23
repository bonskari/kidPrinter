import gtts
import tempfile
import os
import subprocess
import time
import speech_recognition as sr
import wave
from pydub import AudioSegment
import threading

# --- Configuration ---
# Use the stable, custom ALSA device names created by our setup script.
SPEAKER_DEVICE = "kidprinter_playback"
# We use the custom name for the microphone as well for consistency.
MIC_DEVICE_NAME = "kidprinter_mic"
# For speech_recognition, we still need to find the mic by its system name to get the index.
MIC_SEARCH_NAME = "USB PnP Sound Device"


def play_audio_mpg123(file_path, device=SPEAKER_DEVICE):
    """Plays an audio file using mpg123 with our custom device name."""
    try:
        subprocess.run(['mpg123', '-q', '-a', device, file_path], check=True, timeout=15)
        return True
    except Exception as e:
        print(f"   ❌ Playback error with mpg123: {e}")
        return False

def play_audio_aplay(file_path, device=SPEAKER_DEVICE, sample_rate=None):
    """Plays an audio file using aplay with our custom device name."""
    try:
        command = ['aplay', '-D', device, file_path]
        if sample_rate:
            command.extend(['--rate', str(sample_rate)])
        subprocess.run(command, check=True, timeout=15)
        return True
    except Exception as e:
        print(f"   ❌ Playback error with aplay: {e}")
        return False

def create_tts_audio(text, lang='en'):
    """Creates a temporary MP3 file from text using gTTS."""
    try:
        tts = gtts.gTTS(text=text, lang=lang, slow=False)
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        tts.save(mp3_file)
        return mp3_file
    except Exception as e:
        print(f"❌ TTS creation failed: {e}")
        return None

def record_audio(search_name, duration=3):
    """Records audio from the specified microphone."""
    r = sr.Recognizer()
    mic_index = -1
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        if search_name in name:
            mic_index = index
            break
    
    if mic_index == -1:
        print(f"   ❌ Microphone containing '{search_name}' not found.")
        return None, None, None

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print(f"   🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print(f"   🎤 Recording from {mic_list[mic_index]} for {duration:.2f} seconds... (Sample Rate: {source.SAMPLE_RATE}, Sample Width: {source.SAMPLE_WIDTH})")
            audio = r.listen(source, timeout=duration + 2, phrase_time_limit=duration + 1)
            return audio.frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH
    except Exception as e:
        print(f"   ❌ Recording failed: {e}")
        return None, None, None

def record_audio_threaded(search_name, duration, result_list):
    """Records audio from the specified microphone in a separate thread."""
    recorded_data, sample_rate, sample_width = record_audio(search_name, duration)
    result_list.extend([recorded_data, sample_rate, sample_width])

def process_and_play_wav(wav_data, sample_rate, sample_width, device=SPEAKER_DEVICE):
    """Processes recorded audio and plays it back using mpg123."""
    tmp_wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    try:
        # Write raw audio data to a temporary WAV file
        with wave.open(tmp_wav_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(wav_data)

        # Load the WAV with pydub to process it (gain, resample)
        audio = AudioSegment.from_wav(tmp_wav_file)
        audio += 15  # Apply 15dB gain
        # audio = audio.set_frame_rate(48000) # Resample for compatibility
        
        # Export to a new WAV file for playback
        processed_wav_file = tempfile.NamedTemporaryFile(suffix='_processed.wav', delete=False).name
        audio.export(processed_wav_file, format="wav")

        print(f"   🔊 Playing back recorded audio on device {device}...")
        success = play_audio_aplay(processed_wav_file, device=device, sample_rate=sample_rate)
        return success

    except Exception as e:
        print(f"   ❌ Playback of recorded audio failed: {e}")
        return False
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_wav_file):
            os.unlink(tmp_wav_file)
        # The processed_wav_file is created within the try block, so check if it exists before trying to unlink
        if 'processed_wav_file' in locals() and os.path.exists(processed_wav_file):
            os.unlink(processed_wav_file)

if __name__ == "__main__":
    print("🎵 Robust Audio Test with Stable Device Names")
    print("=" * 50)

    # --- Step 1: Concurrent Recording and Playback ---
    print("\nStep 1: Recording from microphone while playing TTS sound.")
    print("   Please make some noise (speak, clap, etc.) during the recording.")

    tts_text = "Hello, this is a test using the stable playback device name."
    tts_mp3_file = create_tts_audio(tts_text, lang='en')

    recorded_audio_results = []
    record_duration = 5 # Increased duration to ensure capture of TTS and some ambient sound
    record_thread = threading.Thread(target=record_audio_threaded, args=(MIC_SEARCH_NAME, record_duration, recorded_audio_results))

    record_thread.start()
    time.sleep(0.5) # Give a moment for the recording thread to start

    if tts_mp3_file:
        print(f"   ℹ️ TTS MP3 file created at: {tts_mp3_file}")
        if os.path.exists(tts_mp3_file):
            print("   ✅ TTS MP3 file exists.")
        else:
            print("   ❌ TTS MP3 file does NOT exist.")

        if play_audio_mpg123(tts_mp3_file):
            print("   ✅ TTS sound played successfully.")
            time.sleep(1) # Give time for playback to finish
        else:
            print("   ❌ Failed to play TTS sound.")
        os.unlink(tts_mp3_file)
    else:
        print("   ❌ Failed to create TTS audio file.")

    record_thread.join() # Wait for the recording thread to complete

    if recorded_audio_results:
        recorded_data, sample_rate, sample_width = recorded_audio_results
        if recorded_data:
            print(f"   ✅ Recorded data captured. Size: {len(recorded_data)} bytes.")
            if process_and_play_wav(recorded_data, sample_rate, sample_width):
                print("   ✅ Recorded audio played back successfully.")
                time.sleep(2) # Give time for playback

                # Perform Speech-to-Text
                print("\n   🗣️ Attempting Speech-to-Text recognition...")
                r = sr.Recognizer()
                try:
                    # Create an AudioData object from the raw recorded data
                    audio_data_for_stt = sr.AudioData(recorded_data, sample_rate, sample_width)
                    text = r.recognize_google(audio_data_for_stt, language="en-US")
                    print(f"   ✅ Recognized text: \"{text}\"")
                except sr.UnknownValueError:
                    print("   ❌ Speech Recognition could not understand audio.")
                except sr.RequestError as e:
                    print(f"   ❌ Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    print(f"   ❌ An unexpected error occurred during STT: {e}")

            else:
                print("   ❌ Failed to play back recorded audio.")
        else:
            print("   ❌ Failed to record audio. recorded_data is empty.")
    else:
        print("   ❌ Recording thread did not return any data.")

    print("\nTest complete.")