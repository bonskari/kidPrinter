#!/usr/bin/env python3
"""
Kid-friendly automatic printer application
Main entry point for the application
"""

import os
import sys
import json
import time
import math
import subprocess
import tempfile
from pathlib import Path
import speech_recognition as sr
import pyttsx3

class KidPrinter:
    """Main application class for Kid Printer"""
    
    def __init__(self):
        """Initialize the Kid Printer application"""
        self.config = self.load_config()
        self.recognizer = sr.Recognizer()
        self.daily_print_count = 0
        
        # Try to initialize TTS, fallback to Google TTS if not available
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_enabled = True
            self.setup_voice_settings()
        except Exception as e:
            print(f"⚠️  pyttsx3 TTS not available: {e}")
            print("⚠️  Will use alternative TTS method")
            self.tts_engine = None
            self.tts_enabled = False
        
    def load_config(self):
        """Load configuration from settings.json"""
        config_path = Path(__file__).parent.parent / 'config' / 'settings.json'
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: Config file not found, using defaults")
            return {
                "voice_recognition": {"language": "fi-FI", "timeout": 10},
                "printer": {"daily_print_limit": 5, "max_pages_per_print": 3},
                "content_safety": {"enabled": True, "filter_level": "strict"}
            }
    
    def setup_voice_settings(self):
        """Setup text-to-speech voice settings"""
        if not self.tts_enabled:
            return
            
        voices = self.tts_engine.getProperty('voices')
        # Try to find Finnish voice, fallback to default
        for voice in voices:
            if 'fi' in voice.id.lower() or 'finnish' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        self.tts_engine.setProperty('rate', 150)  # Slower speech for kids
        self.tts_engine.setProperty('volume', 0.8)
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"🗣️  {text}")
        if self.tts_enabled:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        else:
            # Use alternative TTS method with Google TTS
            self.speak_with_google_tts(text)
    
    def speak_with_google_tts(self, text):
        """Alternative TTS using Google Translate's TTS API"""
        try:
            # Install gTTS if not available
            try:
                import gtts
            except ImportError:
                print("Installing gTTS...")
                subprocess.run([sys.executable, "-m", "pip", "install", "gtts"], 
                             capture_output=True, check=True)
                import gtts
            
            # Create TTS object for Finnish - slow=True for kid-friendly speech
            tts = gtts.gTTS(text=text, lang='fi', slow=True)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tts.save(tmp_file.name)
                
                # Play MP3 through ROG Hive speakers using mpg123
                try:
                    # Use mpg123 to play directly to hw:2,0 (ROG Hive speakers)
                    subprocess.run(['mpg123', '-a', 'hw:2,0', tmp_file.name], 
                                 capture_output=True, timeout=15)
                    
                except subprocess.TimeoutExpired:
                    print("⚠️  TTS playback timeout")
                except FileNotFoundError:
                    print("⚠️  mpg123 not found, trying pygame fallback")
                    # Fallback to pygame
                    try:
                        import pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load(tmp_file.name)
                        pygame.mixer.music.play()
                        
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                            
                        pygame.mixer.quit()
                    except:
                        print("⚠️  All audio methods failed")
                except Exception as e:
                    print(f"⚠️  TTS playback error: {e}")
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"⚠️  Alternative TTS failed: {e}")
            print("⚠️  Continuing with text-only mode")
        
    def play_listening_sound(self):
        """Play a sound to indicate listening has started"""
        try:
            # Create a higher pitch beep for "listening"
            beep_file = "/tmp/listening_beep.wav"
            
            # Create a 1200Hz tone for 0.2 seconds at reduced volume
            sample_rate = 44100
            duration = 0.2
            frequency = 1200
            volume = 0.4
            
            # Generate sine wave
            samples = []
            for i in range(int(sample_rate * duration)):
                sample = int(32767 * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
                samples.append(sample)
            
            # Write to WAV file
            import wave
            with wave.open(beep_file, 'w') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                for sample in samples:
                    wav_file.writeframes(sample.to_bytes(2, byteorder='little', signed=True))
                    wav_file.writeframes(sample.to_bytes(2, byteorder='little', signed=True))  # Duplicate for stereo
            
            # Play the beep through speakers
            subprocess.run(["aplay", "-D", "hw:2,0", beep_file], capture_output=True, timeout=3)
            
            # Clean up
            os.unlink(beep_file)
            
        except Exception as e:
            print(f"Listening sound failed: {e}")
    
    def listen_for_speech(self):
        """Listen for speech input and return recognized text"""
        try:
            # Use the USB microphone device (device 0 from our tests)
            with sr.Microphone(device_index=0) as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Play listening sound
                self.play_listening_sound()
                
                # Listen for speech
                timeout = self.config["voice_recognition"]["timeout"]
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("🔄 Processing speech...")
                
                # Try Finnish first
                try:
                    text = self.recognizer.recognize_google(
                        audio, 
                        language=self.config["voice_recognition"]["language"]
                    )
                    print(f"🇫🇮 Recognized (Finnish): {text}")
                    return text
                except sr.UnknownValueError:
                    # Try English as fallback
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        print(f"🇺🇸 Recognized (English): {text}")
                        return text
                    except sr.UnknownValueError:
                        return None
                        
        except sr.WaitTimeoutError:
            return "timeout"
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            return None
            
    def check_daily_limit(self):
        """Check if daily print limit has been reached"""
        limit = self.config["printer"]["daily_print_limit"]
        return self.daily_print_count < limit
        
    def process_print_request(self, text):
        """Process a print request from speech"""
        if not text:
            return False
            
        # Check for print keywords in Finnish and English
        print_keywords = ['tulosta', 'print', 'printtaa', 'kirjoita']
        text_lower = text.lower()
        
        is_print_request = any(keyword in text_lower for keyword in print_keywords)
        
        if is_print_request:
            if not self.check_daily_limit():
                self.speak("Pahoillani, päivän tulostusmäärä on täynnä!")
                return False
                
            # TODO: Implement content safety filtering
            # TODO: Implement actual printing
            print(f"📄 Print request: {text}")
            self.speak(f"Tulostan: {text}")
            self.daily_print_count += 1
            return True
        
        return False
        
    def run(self):
        """Main application loop"""
        self.speak("Hei! Olen tulostinrobotti. Sano mitä haluat tulostaa!")
        
        while True:
            try:
                # Listen for speech
                speech_text = self.listen_for_speech()
                
                if speech_text == "timeout":
                    print("⏰ Listening timeout, continuing...")
                    continue
                elif speech_text is None:
                    print("❓ Could not understand speech, trying again...")
                    continue
                    
                # Process the speech
                if self.process_print_request(speech_text):
                    self.speak("Tulostus valmis!")
                else:
                    self.speak("En ymmärrä. Sano 'tulosta' ja sitten mitä haluat tulostaa.")
                    
            except KeyboardInterrupt:
                print("\n👋 Shutting down Kid Printer...")
                self.speak("Nähdään taas!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)

def main():
    """Main application entry point"""
    print("Kid Printer - Automatic Printer for Kids")
    print("Starting application...")
    
    # Check if running on Raspberry Pi
    if Path('/proc/device-tree/model').exists():
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            if 'Raspberry Pi' in model:
                print(f"Running on: {model}")
    
    # Initialize and run the application
    try:
        app = KidPrinter()
        print("Application ready!")
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()