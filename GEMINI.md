# Project-Specific Guidelines for Gemini

This `GEMINI.md` file provides context and preferences for the Gemini AI agent when working on the `childs-automatic-printer` project.

## General Preferences:

*   **Language:** Finnish for voice recognition and prompts.
*   **Voice Recognition:** Prefer a local, lightweight LLM for Finnish speech-to-text, suitable for Raspberry Pi.
*   **Content Safety:** Prioritize kid-friendly content.
*   **Asset Location:** All project assets (images, audio files, etc.) should be placed in the `assets/` directory, with subdirectories for organization (e.g., `assets/images/`, `assets/audio/`).
*   **Code Style:** Adhere to standard Python formatting (e.g., Black, Flake8).
*   **Commit Messages:** Aim for clear, concise, and descriptive commit messages.

## Project Structure:

*   `src/`: Main application logic.
*   `assets/`: Directory for all project resources.
    *   `assets/images/`: Curated kid-friendly images.
    *   `assets/audio/`: Audio prompts and feedback.
*   `config/`: Configuration files (e.g., print limits, LLM settings).

## Current Development Focus:

*   Implementing local Finnish voice recognition.

*   Integrating with printer control.
*   Developing the daily print limit and feedback system.
