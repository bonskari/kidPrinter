#!/usr/bin/env python3
"""
Child's Automatic Printer - Main Application

A Finnish voice-controlled printing system for children.
"""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from voice_recognition import FinnishVoiceRecognizer
from printer_controller import PrinterController
from content_filter import ContentFilter
from daily_limits import DailyLimitManager
from audio_feedback import AudioFeedback


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('kidprinter.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Child's Automatic Printer")
    
    try:
        # Initialize components
        voice_recognizer = FinnishVoiceRecognizer()
        printer_controller = PrinterController()
        content_filter = ContentFilter()
        limit_manager = DailyLimitManager()
        audio_feedback = AudioFeedback()
        
        logger.info("All components initialized successfully")
        
        # Main application loop
        audio_feedback.play_welcome_message()
        
        while True:
            try:
                # Listen for voice commands
                command = voice_recognizer.listen()
                
                if command:
                    logger.info(f"Voice command received: {command}")
                    
                    # Check daily limits
                    if not limit_manager.can_print():
                        audio_feedback.play_limit_reached_message()
                        continue
                    
                    # Filter content for kid-friendliness
                    if not content_filter.is_safe(command):
                        audio_feedback.play_content_warning()
                        continue
                    
                    # Process print request
                    success = printer_controller.print_content(command)
                    
                    if success:
                        limit_manager.record_print()
                        audio_feedback.play_success_message()
                    else:
                        audio_feedback.play_error_message()
                
            except KeyboardInterrupt:
                logger.info("Shutting down gracefully...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                audio_feedback.play_error_message()
    
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
