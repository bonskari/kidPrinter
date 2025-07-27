import 'dart:convert';
import 'dart:io';
import 'package:flutter_app/log.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'config.dart';
import 'dart:io';

class AIService extends ChangeNotifier {
  bool get awaitingImageDescription => _awaitingImageDescription;
  bool _cancelRequested = false;
  int _currentTokenIndex = 0;

  /// Generate a perfected coloring book image using Stable Diffusion XL (Hugging Face)
  Future<Uint8List?> generateColoringBookImage({
    required String subject,
    int width = 744,
    int height = 1048,
  }) async {
    try {
      _cancelRequested = false;
      _images.clear();
      _loading = true;
      notifyListeners();
      final prompt =
          "black and white line art coloring book page of $subject, "
          "full body visible, pure line drawing only, thick black outlines on pure white background, "
          "NO SHADING, NO FILLED AREAS, NO GRAY, empty areas inside lines, outline only, "
          "kids coloring book style, simple cartoon, friendly expression, complete character visible, "
          "NO BACKGROUND, plain white background, character only, isolated character, a few pixels of white margin around the character, character fully visible and centered, do not crop, do not overflow, do not touch the edges, hands in fists";

      final negativePrompt =
          "shading, shadows, filled areas, gray areas, gradients, color, colored, "
          "dark areas, black fill, solid fill, realistic shading, cell shading, tonal variation, "
          "grayscale fill, photographic, realistic, complex details, watermark, text, blurry, "
          "partial body, cropped, cut off, sketchy lines, crosshatching, hatching, stippling, "
          "background, scenery, landscape, objects, furniture, buildings, trees, grass, sky, "
          "clouds, ground, floor, environment, props, items, decorations";

      final url = Uri.parse(
        'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0',
      );
      final body = jsonEncode({
        'inputs': prompt,
        'parameters': {
          'negative_prompt': negativePrompt,
          'width': width,
          'height': height,
          'guidance_scale': 7.5,
          'num_inference_steps': 30,
        },
      });

      for (int i = 0; i < stableDiffusionApiKeys.length; i++) {
        final token = stableDiffusionApiKeys[i];
        final headers = {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        };
        try {
          if (_cancelRequested) {
            _loading = false;
            notifyListeners();
            return null;
          }
          final response = await http.post(url, headers: headers, body: body);
          if (_cancelRequested) {
            _loading = false;
            notifyListeners();
            return null;
          }
          if (response.statusCode == 200) {
            _lastError = null;
            _images.add(response.bodyBytes);
            // Write image to tmp/generated_image.png for inspection
            try {
              final tmpFile = File('tmp/generated_image.png');
              tmpFile.createSync(recursive: true);
              tmpFile.writeAsBytesSync(response.bodyBytes);
              print(
                'Image bytes written to tmp/generated_image.png, length: ${response.bodyBytes.length}',
              );
            } catch (e) {
              print('Failed to write image file: $e');
            }
            _loading = false;
            notifyListeners();
            return response.bodyBytes;
          } else {
            String apiError = '';
            try {
              final errorJson = jsonDecode(response.body);
              if (errorJson is Map && errorJson.containsKey('error')) {
                apiError = errorJson['error'].toString();
              }
            } catch (_) {
              apiError = response.body;
            }
            _lastError =
                'Failed to generate coloring book image with token $i: ${response.statusCode} - $apiError';
            // Try next token
          }
        } catch (e) {
          _lastError = 'Error with token $i: $e';
        }
      }

      _loading = false;
      notifyListeners();
      if (_lastError != null) {
        throw Exception(_lastError);
      }
      return null;
    } catch (e) {
      _lastError = 'Unexpected error in generateColoringBookImage: $e';
      LOG.ERROR(_lastError);
      _loading = false;
      notifyListeners();
      return null;
    }
  }

  void cancelGeneration() {
    _cancelRequested = true;
    _loading = false;
    notifyListeners();
  }

  /// If true, use Gemini image generation; if false, use Hugging Face.
  bool useGeminiImageGeneration = true;

  /// Generates images using the Gemini (Google) API, returns both text and image (base64) if available.
  Future<Map<String, dynamic>> generateGeminiImage(String prompt) async {
    _images.clear();
    _loading = true;
    notifyListeners();
    try {
      final url = Uri.parse(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key=$apiKey',
      );
      final headers = {'Content-Type': 'application/json'};
      final body = jsonEncode({
        'contents': [
          {
            'parts': [
              {'text': prompt},
            ],
          },
        ],
        'generationConfig': {
          'responseModalities': ['TEXT', 'IMAGE'],
        },
      });

      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // Gemini returns candidates, each may have text and/or image
        final candidates = data['candidates'] as List?;
        String? text;
        String? imageBase64;
        if (candidates != null && candidates.isNotEmpty) {
          final parts = candidates[0]['content']['parts'] as List?;
          if (parts != null && parts.isNotEmpty) {
            for (var part in parts) {
              if (part.containsKey('text')) {
                text = part['text'];
              }
              if (part.containsKey('inlineData')) {
                // Gemini returns image as base64 in inlineData
                imageBase64 = part['inlineData']['data'];
              }
            }
          }
        }
        _lastError = null;
        _loading = false;
        notifyListeners();
        return {'text': text, 'image': imageBase64};
      }
      throw Exception(
        'Failed to generate Gemini image: ${response.statusCode} ${response.body}',
      );
    } catch (e) {
      _lastError = e.toString();
      _loading = false;
      notifyListeners();
      return {};
    }
  }

  final String apiKey;
  // Use the list from config.dart
  // Uses the global stableDiffusionApiKeys from config.dart
  // Use the flash model for faster responses
  final String _baseUrl =
      'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent';

  String? _lastResult;
  String? get lastResult => _lastResult;
  String? _lastError;
  String? get lastError => _lastError;
  bool _loading = false;
  bool get loading => _loading;

  bool _awaitingImageDescription = false;
  final List<Uint8List> _images = [];
  List<Uint8List> get images => List.unmodifiable(_images);
  AIService(this.apiKey);

  /// Checks if the response contains an image command and updates state accordingly.
  void checkForImageCommand(String response) {
    if (response.isNotEmpty && response.trim().startsWith('__IMAGE__')) {
      _awaitingImageDescription = true;
    } else {
      _awaitingImageDescription = false;
    }
  }

  /// Sends a prompt to Gemini and notifies listeners on result or error.
  Future<void> _generateContent(String prompt) async {
    _loading = true;
    _lastResult = null;
    _lastError = null;
    notifyListeners();
    try {
      // Add extra context helpers
      final contextPrefix =
          'Vastaa aina suomeksi ja lapselle sopivalla tavalla. Jos käyttäjä haluaa kuvan, vastaa ensin __IMAGE__ ja sen perään kysy että minkälainen kuva. Jos ei halua kuvaa, älä käytä __IMAGE__. Vastaa korkeintaan viidellä sanalla.\n';
      final fullPrompt = contextPrefix + prompt;
      final url = Uri.parse('$_baseUrl?key=$apiKey');
      final headers = {'Content-Type': 'application/json'};
      final body = jsonEncode({
        'contents': [
          {
            'parts': [
              {'text': fullPrompt},
            ],
          },
        ],
      });

      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // Gemini returns candidates, take the first one
        final candidates = data['candidates'] as List?;
        if (candidates != null && candidates.isNotEmpty) {
          final text = candidates[0]['content']['parts'][0]['text'];
          _lastResult = text;
          checkForImageCommand(text);
        } else {
          _lastResult = null;
          checkForImageCommand("");
        }
        _lastError = null;
      } else {
        _lastResult = null;
        _lastError =
            'Failed to generate content: \n${response.statusCode} ${response.body}';
        checkForImageCommand("");
      }
    } catch (e) {
      _lastResult = null;
      _lastError = e.toString();
      checkForImageCommand("");
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  /// Generates images from a prompt using Hugging Face Inference API.
  Future<List<Uint8List>> _generateImages(String prompt) async {
    _images.clear();
    _awaitingImageDescription = false;
    _loading = true;
    notifyListeners();
    try {
      final coloringPrompt =
          'A children coloring book image, simple lines, black and white, suitable for kids. $prompt';
      final url = Uri.parse(
        'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0',
      );
      final headers = {
        'Authorization':
            'Bearer ${stableDiffusionApiKeys.isNotEmpty ? stableDiffusionApiKeys[0] : ''}',
        'Content-Type': 'application/json',
      };
      final body = jsonEncode({'inputs': coloringPrompt});

      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        final bytes = response.bodyBytes;

        _lastError = null;
        _images.add(bytes);
        _loading = false;
        notifyListeners();
        return [bytes];
      }
      throw Exception(
        'Failed to generate image: ${response.statusCode} ${response.body}',
      );
    } catch (e) {
      _lastError = e.toString();
      _loading = false;
      notifyListeners();
      return [];
    }
  }

  /// Unified entry point: decides whether to generate text or image based on prompt and context.
  Future<dynamic> generate(String prompt) async {
    if (_awaitingImageDescription) {
      // If awaiting image description, generate image
      // Always use generateColoringBookImage for image generation
      return await generateColoringBookImage(subject: prompt);
    } else {
      // Otherwise, generate text
      await _generateContent(prompt);
      return lastResult;
    }
  }

  /// Returns the TTS text for a new response, or null if not needed.
  String? getTtsTextForResponse(String? lastSpokenResult) {
    if (lastResult == null || lastResult == lastSpokenResult) return null;
    final trimmed = lastResult!.trim();
    if (trimmed.startsWith('__IMAGE__')) {
      final promptMsg = _cleanGeminiResponseForTTS(trimmed);
      return promptMsg.isNotEmpty ? promptMsg : 'Minkälaisen kuvan haluat?';
    } else {
      final cleanText = _cleanGeminiResponseForTTS(trimmed).replaceAll(
        RegExp(
          r'[^\u0000-\u007FäöåÄÖÅ.,!?\u0000-\u007F ]',
          caseSensitive: false,
        ),
        '',
      );
      return cleanText.isNotEmpty ? cleanText : null;
    }
  }

  /// Internal helper for cleaning Gemini response for TTS.
  String _cleanGeminiResponseForTTS(String response) {
    final trimmed = response.trim();
    if (trimmed.startsWith('__IMAGE__')) {
      return trimmed.replaceFirst('__IMAGE__', '').trim();
    }
    return trimmed;
  }
}
