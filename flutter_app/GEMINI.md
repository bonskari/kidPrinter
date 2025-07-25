# Project: Kid's Voice Assistant & AI Image Printer

## Description

This is a Flutter-based voice assistant application designed for children. The app actively listens for a wake word or a button press, captures the child's speech in Finnish, and sends it to Google's Gemini API for processing. The application then speaks the response back to the child using a Text-to-Speech (TTS) engine.

A key feature of this app is the ability to generate images based on the user's voice description. The user can ask the assistant to "draw a picture of a blue dog" and the app will use the Gemini API to generate the image and display it. The user can then choose to print the generated image.

## Core Features

*   **Voice Recognition (Finnish):** Captures voice commands from the user in Finnish.
*   **Conversational AI:** Engages in a spoken conversation with the user through the Gemini API.
*   **AI Image Generation:** Generates images based on user's voice descriptions using the Gemini API.
*   **Image Display & Printing:** Displays the generated image and provides an option to print it.
*   **Parental Controls:** (Future) Will include features for parents to monitor usage and set limits.

## Tech Stack

*   **Frontend:** Flutter
*   **Language:** Dart
*   **AI Services:** Google Gemini API (for conversation and image generation)
*   **Voice Recognition:** `speech_to_text` (or similar)
*   **Text-to-Speech:** `flutter_tts` (or similar)
*   **Printing:** `printing` (or similar)

## Configuration

*   **API Keys:** The application will require a Google Gemini API key. This will be stored in a configuration file (`config.dart`) and will not be checked into version control.
*   **Printer Settings:** Basic printer configuration will be handled through the app's settings.