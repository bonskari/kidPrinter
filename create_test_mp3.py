from gtts import gTTS
import os

text = "Hello, this is a test sound."
language = 'en'

output_dir = "assets/audio"
output_file = os.path.join(output_dir, "test_sound.mp3")

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

mytxt = gTTS(text=text, lang=language, slow=False)
mytxt.save(output_file)

print(f"Generated {output_file}")