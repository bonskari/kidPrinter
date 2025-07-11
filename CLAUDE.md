# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kid-friendly automatic printer application designed to run on Raspberry Pi. The application uses Finnish voice recognition to accept print requests from children with built-in safety controls and daily print limits.

## Essential Commands

### Dependency Management
```bash
# Install dependencies
pip install -r requirements.txt

# Check if dependencies are installed
python3 check_dependencies.py
```

### Running the Application
```bash
# Main application
python3 src/main.py

# Test microphone functionality
python3 test_microphone.py

# Simple microphone test
python3 simple_mic_test.py

# Debug audio issues
python3 debug_audio.py
```

## Architecture

### Core Components
- **Voice Recognition**: Uses SpeechRecognition library with Finnish (fi-FI) language support
- **Content Safety**: Strict filtering for kid-friendly content
- **Print Control**: Daily print limits (5 prints/day, max 3 pages per print)
- **Configuration**: JSON-based settings in `config/settings.json`

### Key Dependencies
- `speechrecognition==3.10.0` - Voice recognition
- `pyttsx3==2.90` - Text-to-speech
- `pyaudio==0.2.11` - Audio input/output
- `transformers==4.30.0` - NLP models
- `torch==2.0.1` - Machine learning backend

### Directory Structure
- `src/` - Main application logic
- `assets/` - Images, audio files, and other resources
  - `assets/images/` - Kid-friendly images
  - `assets/audio/` - Audio prompts and feedback
- `config/` - Configuration files
- Root level testing scripts for microphone and audio debugging

## Development Notes

### Platform Considerations
- Primary target: Raspberry Pi
- Application detects Raspberry Pi hardware via `/proc/device-tree/model`
- Uses local lightweight models for Finnish speech recognition

### Safety Features
- Content safety filtering enabled by default
- Strict filter level for kid-friendly content
- Daily print limits to prevent overuse
- Page limits per print job

### Current Implementation Status
The main application (`src/main.py`) is in early development with TODO items for:
- Voice recognition initialization
- Printer control implementation
- Daily print limit system