"""
Audio Feedback Module

Provides Finnish audio feedback for the child's automatic printer.
"""

import logging
import pygame
import pyttsx3
from pathlib import Path
from typing import Optional


class AudioFeedback:
    """Handles audio feedback in Finnish for user interactions."""
    
    def __init__(self, assets_dir: str = "assets/audio"):
        self.logger = logging.getLogger(__name__)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
            self.logger.info("Pygame mixer initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize pygame mixer: {e}")
        
        # Initialize text-to-speech engine
        try:
            self.tts_engine = pyttsx3.init()
            self._configure_tts()
            self.logger.info("Text-to-speech engine initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS: {e}")
            self.tts_engine = None
    
    def _configure_tts(self) -> None:
        """Configure TTS engine for Finnish."""
        if not self.tts_engine:
            return
        
        # Set Finnish voice if available
        voices = self.tts_engine.getProperty('voices')
        finnish_voice = None
        
        for voice in voices:
            if 'fi' in voice.id.lower() or 'finnish' in voice.name.lower():
                finnish_voice = voice.id
                break
        
        if finnish_voice:
            self.tts_engine.setProperty('voice', finnish_voice)
            self.logger.info(f"Set Finnish voice: {finnish_voice}")
        else:
            self.logger.warning("No Finnish voice found, using default")
        
        # Configure speech rate and volume
        self.tts_engine.setProperty('rate', 150)  # Slower for children
        self.tts_engine.setProperty('volume', 0.8)
    
    def play_audio_file(self, filename: str) -> bool:
        """
        Play an audio file from the assets directory.
        
        Args:
            filename: Name of the audio file
            
        Returns:
            True if playback was successful
        """
        audio_path = self.assets_dir / filename
        
        if not audio_path.exists():
            self.logger.warning(f"Audio file not found: {audio_path}")
            return False
        
        try:
            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            self.logger.debug(f"Played audio file: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error playing audio file {filename}: {e}")
            return False
    
    def speak_text(self, text: str) -> bool:
        """
        Convert text to speech in Finnish.
        
        Args:
            text: Finnish text to speak
            
        Returns:
            True if speech was successful
        """
        if not self.tts_engine:
            self.logger.error("TTS engine not available")
            return False
        
        try:
            self.logger.debug(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {e}")
            return False
    
    def play_welcome_message(self) -> None:
        """Play welcome message."""
        if not self.play_audio_file("welcome.wav"):
            self.speak_text("Tervetuloa! Sano mitä haluat tulostaa.")
    
    def play_success_message(self) -> None:
        """Play success message."""
        if not self.play_audio_file("success.wav"):
            self.speak_text("Hienoa! Tulostus onnistui.")
    
    def play_error_message(self) -> None:
        """Play error message."""
        if not self.play_audio_file("error.wav"):
            self.speak_text("Pahoittelen, tapahtui virhe. Yritä uudelleen.")
    
    def play_limit_reached_message(self) -> None:
        """Play daily limit reached message."""
        if not self.play_audio_file("limit_reached.wav"):
            self.speak_text("Olet jo tulostanut tarpeeksi tänään. Yritä huomenna uudelleen.")
    
    def play_content_warning(self) -> None:
        """Play content not appropriate message."""
        if not self.play_audio_file("content_warning.wav"):
            self.speak_text("Tuo ei ole sopivaa. Voisimme tulostaa jotain mukavampaa?")
    
    def play_listening_prompt(self) -> None:
        """Play listening prompt."""
        if not self.play_audio_file("listening.wav"):
            self.speak_text("Kuuntelen...")
    
    def announce_remaining_prints(self, count: int) -> None:
        """Announce how many prints are remaining today."""
        if count == 1:
            message = "Sinulla on vielä yksi tulostus jäljellä tänään."
        elif count > 1:
            message = f"Sinulla on vielä {count} tulostusta jäljellä tänään."
        else:
            message = "Sinulla ei ole enää tulostuksia jäljellä tänään."
        
        self.speak_text(message)
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
            if self.tts_engine:
                self.tts_engine.stop()
            self.logger.info("Audio feedback cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during audio cleanup: {e}")
