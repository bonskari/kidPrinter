"""
Finnish Voice Recognition Module

Handles voice recognition specifically for Finnish language using local LLM.
"""

import logging
import speech_recognition as sr
import pyaudio
from typing import Optional


class FinnishVoiceRecognizer:
    """Finnish voice recognition handler optimized for Raspberry Pi."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        self.logger.info("Finnish voice recognizer initialized")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for voice input and return recognized Finnish text.
        
        Args:
            timeout: Maximum time to wait for input
            
        Returns:
            Recognized text or None if no speech detected
        """
        try:
            with self.microphone as source:
                self.logger.debug("Listening for voice input...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            # Use Google's speech recognition with Finnish language
            text = self.recognizer.recognize_google(audio, language="fi-FI")
            self.logger.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            self.logger.debug("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in voice recognition: {e}")
            return None
    
    def is_wake_word(self, text: str) -> bool:
        """Check if the recognized text contains Finnish wake words."""
        wake_words = ["tulosta", "kirjoita", "piirtää", "kuva"]
        return any(word in text for word in wake_words)
