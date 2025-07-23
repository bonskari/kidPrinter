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
*   `tests/`: Dedicated directory for all test scripts.

## Current Development Focus:

*   Implementing local Finnish voice recognition.

*   Integrating with printer control.
*   Developing the daily print limit and feedback system.

## Testing Guidelines:

*   **Test Location:** All test scripts should reside in the `tests/` directory.
*   **User Confirmation:** When performing tests that involve audio playback or other sensory outputs, always include clear prompts for user confirmation to verify the output.
*   **Isolation:** Strive to create isolated tests that focus on a single piece of functionality to simplify debugging.
*   **Cleanup:** Ensure test scripts clean up any temporary files or resources they create.
*   **No User Input in Python Files:** Never include `input()` calls or other direct user input mechanisms within Python test scripts. All user interaction should occur through the CLI agent.

## Audio Configuration:

*   **Playback Device:** `hw:2,0` (AUREON XFIRE8.0 HD) has been confirmed to work for audio playback using `mpg123`.
*   **Working Playback Example:** The `tests/playback_test.py` script demonstrates a working audio playback setup.