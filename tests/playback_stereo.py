
import wave
import sys
from pydub import AudioSegment

def convert_to_stereo(input_filename, output_filename):
    """Converts a mono WAV file to stereo."""
    try:
        mono_audio = AudioSegment.from_wav(input_filename)
        stereo_audio = mono_audio.set_channels(2)
        stereo_audio.export(output_filename, format="wav")
        print(f"✅ Converted {input_filename} to stereo: {output_filename}")
        return True
    except Exception as e:
        print(f"❌ Error converting to stereo: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 playback_stereo.py <input_filename>")
        return

    input_filename = sys.argv[1]
    stereo_filename = "stereo_" + input_filename

    if convert_to_stereo(input_filename, stereo_filename):
        mp3_filename = stereo_filename.replace(".wav", ".mp3")
        try:
            AudioSegment.from_wav(stereo_filename).export(mp3_filename, format="mp3")
            print(f"✅ Converted {stereo_filename} to MP3: {mp3_filename}")
            import os
            os.system(f"mpg123 -a hw:2,0 {mp3_filename}")
        except Exception as e:
            print(f"❌ Error converting to MP3 or playing: {e}")

if __name__ == "__main__":
    main()
