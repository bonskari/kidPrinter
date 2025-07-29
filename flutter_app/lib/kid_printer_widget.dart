import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_app/generated_images_widget.dart';
import 'package:flutter_app/printer_service.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'log.dart';
import 'package:provider/provider.dart';
import 'ai_service.dart';

import 'kid_printer_button.dart';
import 'mic_info_widget.dart';
import 'package:stts/stts.dart';

class KidPrinterWidget extends StatefulWidget {
  const KidPrinterWidget({super.key});

  @override
  State<KidPrinterWidget> createState() => _KidPrinterWidgetState();
}

class _KidPrinterWidgetState extends State<KidPrinterWidget>
    with SingleTickerProviderStateMixin {
  bool _awaitingImageApproval = false;
  double _soundLevel = 0.0;
  bool _isRecording = false;
  String? _micError;
  late stt.SpeechToText _speech;
  String _recognizedWords = '';
  String selectedLang = 'fi-FI';
  Timer? _timer;
  String? _lastSpokenGeminiResult;
  final Tts _tts = Tts();

  void _toggleRecording() async {
    try {
      if (_isRecording) {
        _stopSpeechRecognition();
      } else {
        _startSpeechRecognition();
      }
      setState(() {
        _isRecording = !_isRecording;
      });
    } catch (e) {
      setState(() {
        _micError = 'Speech recognition error: $e';
      });
    }
  }

  /// Cleans Gemini response for TTS: removes __IMAGE__ prefix if present, and trims.
  String cleanGeminiResponseForTTS(String response) {
    final trimmed = response.trim();
    if (trimmed.startsWith('__IMAGE__')) {
      return trimmed.replaceFirst('__IMAGE__', '').trim();
    }
    return trimmed;
  }

  Future<void> _initMicName() async {
    LOG.DEBUG('_initMicName called');
    setState(() {
      _micError = null;
    });
    _speech = stt.SpeechToText();
    bool available = await _speech.initialize(
      onStatus: (status) => LOG.DEBUG('Speech status: $status'),
      onError: (error) {
        LOG.ERROR('Speech error: $error');
        setState(() {
          _micError = 'Speech recognition error: $error';
        });
      },
    );
    if (!available) {
      setState(() {
        _micError = 'Speech recognition not available';
      });
    }
  }

  Future<void> _startSpeechRecognition() async {
    try {
      bool available = await _speech.initialize(
        onStatus: (status) {
          LOG.DEBUG('Speech status: $status');
          // Restart listening if stopped due to timeout or done
          if (status == 'notListening' || status == 'done') {
            Future.delayed(const Duration(milliseconds: 500), () {
              if (_isRecording) _startSpeechRecognition();
            });
          }
        },
        onError: (error) {
          LOG.ERROR('Speech error: $error');
          setState(() {
            _micError = 'Speech recognition error: $error';
          });
          // Restart listening on error if still recording
          Future.delayed(const Duration(milliseconds: 500), () {
            if (_isRecording) _startSpeechRecognition();
          });
        },
      );
      if (!available) {
        setState(() {
          _micError = 'Speech recognition not available';
        });
        return;
      }
      _speech.listen(
        onResult: (result) {
          setupResultChanged(result.recognizedWords, result.finalResult);
        },
        onSoundLevelChange: (level) {
          LOG.DEBUG('Sound level changed: $level');
          setState(() {
            // Normalize level: -2.0 (silence) to ~12.0 (loud)
            _soundLevel = ((level + 2.0) / 14.0).clamp(0.0, 1.0);
          });
        },
        localeId: selectedLang,
        listenFor: const Duration(hours: 1), // Effectively 'forever'
        pauseFor: const Duration(seconds: 10), // Allow longer pauses
      );
      LOG.DEBUG('Speech recognition started with language: $selectedLang');
    } catch (e) {
      LOG.ERROR('Error starting speech recognition: $e');
      setState(() {
        _micError = 'Speech recognition error: $e';
      });
    }
  }

  Future<void> _stopSpeechRecognition() async {
    await _speech.stop();
    // Do not clear recognized words on stop
  }

  void setupResultChanged(String recognizedText, bool isFinal) {
    LOG.DEBUG('Recognized words: $recognizedText');
    AIService aiService = Provider.of<AIService>(context, listen: false);
    if (!isFinal) return;
    PrinterService printerService = Provider.of<PrinterService>(
      context,
      listen: false,
    );
    setState(() {
      _recognizedWords += recognizedText;
      _timer?.cancel();
      _timer = Timer(const Duration(seconds: 2), () async {
        if (mounted) {
          if (_awaitingImageApproval) {
            final answer = _recognizedWords.trim().toLowerCase();
            final aiService = Provider.of<AIService>(context, listen: false);
            if (answer == 'yes' || answer == 'kyllä') {
              if (aiService.images.isNotEmpty) {
                await printerService.printImageRemote(
                  base64Image: aiService.images.last,
                );
                await _tts.start('Kuva lähetetty tulostimeen.');
              }
              setState(() {
                // Only clear __IMAGE__ result if approved
                if (aiService.lastResult != null &&
                    aiService.lastResult!.trim().startsWith('__IMAGE__')) {
                  aiService.clearLastResult();
                }
              });
            }
            setState(() {
              _awaitingImageApproval = false;
              _recognizedWords = '';
              _micError = null;
            });
            return;
          }
          // Normal flow: generate response
          await aiService.generate(_recognizedWords.trim());
          setState(() {
            _recognizedWords = '';
            _micError = null;
          });
        }
      });
      LOG.DEBUG('Recognized words: $recognizedText');
    });
  }

  @override
  void initState() {
    super.initState();
    _initMicName();
  }

  @override
  void dispose() {
    _tts.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    AIService aiService = Provider.of<AIService>(context, listen: true);
    PrinterService printerService = Provider.of<PrinterService>(
      context,
      listen: true,
    );
    final ttsTextRaw = aiService.getTtsTextForResponse(_lastSpokenGeminiResult);
    final ttsText = ttsTextRaw == null
        ? null
        : cleanGeminiResponseForTTS(ttsTextRaw);
    if (ttsText != null && ttsText.isNotEmpty && !_awaitingImageApproval) {
      _lastSpokenGeminiResult = aiService.lastResult;
      if (aiService.lastResult != null &&
          aiService.lastResult!.trim().startsWith('__IMAGE__')) {
        setState(() {
          _awaitingImageApproval = true;
        });
        _tts.start('Onko tämä kuva hyvä?').then((_) {
          if (_isRecording) {
            _startSpeechRecognition();
          }
        });
      } else {
        _tts.start(ttsText).then((_) {
          if (_isRecording) {
            _startSpeechRecognition();
          }
        });
      }
    }

    return Column(
      children: [
        Flexible(
          child: GeneratedImagesWidget(
            images: aiService.images,
            loading: aiService.generatingImage,
          ),
        ),

        MicInfoWidget(micError: _micError ?? '', selectedMicDevice: null),

        // --- Sound level bar visualization ---
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 12.0, horizontal: 32.0),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 100),
            height: 18,
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.black,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Align(
              alignment: Alignment.centerLeft,
              child: FractionallySizedBox(
                widthFactor: _soundLevel,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.cyan,
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ),
          ),
        ),

        if (_recognizedWords.isNotEmpty || _micError != null)
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.7),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _micError ?? _recognizedWords.trim(),
                  style: const TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
            ],
          ),
        if (aiService.lastResult == null && (aiService.lastError != null))
          Padding(
            padding: const EdgeInsets.only(top: 16.0),
            child: SizedBox(
              width: 250,
              child: Text(
                aiService.lastError!,
                textAlign: TextAlign.center,
                maxLines: 1,
                style: const TextStyle(fontSize: 16, color: Colors.redAccent),
              ),
            ),
          ),
        if (aiService.lastResult != null && (aiService.lastError == null))
          Padding(
            padding: const EdgeInsets.only(top: 16.0),
            child: Text(
              aiService.lastResult!,
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 16, color: Colors.redAccent),
            ),
          ),
        SizedBox(height: 50),
        Padding(
          padding: const EdgeInsets.only(bottom: 24, top: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              KidPrinterButton(
                onPressed: _toggleRecording,
                icon: _isRecording ? Icons.stop : Icons.mic,
                loading: false,
                disabled: false,
              ),
              if (aiService.images.isNotEmpty)
                KidPrinterButton(
                  onPressed: () async {
                    try {
                      final base64Image = aiService.images.last;
                      await printerService.printImageRemote(
                        base64Image: base64Image,
                      );
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Image sent to printer!')),
                      );
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Failed to print: $e')),
                      );
                    }
                  },
                  icon: Icons.print,
                  loading: false,
                  disabled: false,
                ),
              KidPrinterButton(
                onPressed: () {
                  final words = [
                    'megaman',
                    'turtles',
                    'sonic',
                    'superkitties',
                    'zelda',
                    'super mario',
                  ];
                  final randomWord = (words..shuffle()).first;
                  Provider.of<AIService>(
                    context,
                    listen: false,
                  ).generateColoringBookImage(subject: randomWord);
                },
                icon: Icons.auto_awesome,
                loading: false,
                disabled: false,
              ),
            ],
          ),
        ),
        SizedBox(height: 50),
      ],
    );
  }
}
