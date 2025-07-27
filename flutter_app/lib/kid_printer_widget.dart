import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_app/generated_images_widget.dart';
import 'package:flutter_app/printer_service.dart';
import 'package:stts/stts.dart';
import 'log.dart';
import 'package:provider/provider.dart';
import 'ai_service.dart';
import 'kid_printer_button.dart';
import 'mic_info_widget.dart';
import 'package:waveform_recorder/waveform_recorder.dart';

class KidPrinterWidget extends StatefulWidget {
  const KidPrinterWidget({super.key});

  @override
  State<KidPrinterWidget> createState() => _KidPrinterWidgetState();
}

class _KidPrinterWidgetState extends State<KidPrinterWidget>
    with SingleTickerProviderStateMixin {
  final WaveformRecorderController _waveformController =
      WaveformRecorderController();
  bool _isRecording = false;
  String? _micError;
  InputDevice? _selectedMicDevice;
  final Stt _stt = Stt();
  String _recognizedWords = '';
  List<InputDevice> _micDevices = [];
  String? _micName;
  List<String> _availableLanguages = [];
  String selectedLang = '';
  Timer? _timer;
  String? _lastSpokenGeminiResult;
  final Tts _tts = Tts();

  void _toggleRecording() async {
    try {
      if (_isRecording) {
        await _waveformController.stopRecording();
        _stopSpeechRecognition();
      } else {
        await _waveformController.startRecording();
        _startSpeechRecognition();
      }
      setState(() {
        _isRecording = !_isRecording;
      });
    } catch (e) {
      setState(() {
        _micError = 'WaveformRecorder error: $e';
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
    // Remove _recorder usage, as device listing should be handled elsewhere or by waveform_recorder if needed
    setState(() {
      _micDevices = [];
      _micError = null;
      _micName = 'No mic found';
      _selectedMicDevice = null;
      LOG.DEBUG('No mic found');
    });
  }

  Future<void> _startSpeechRecognition() async {
    try {
      // Start listening with stts, set language to Finnish
      String languageCode = 'fi-FI';
      // Check if the available languages contain the desired languageCode
      final languages = await _stt.getLanguages();
      LOG.DEBUG('Available languages: $languages');
      _availableLanguages = languages;
      if (!languages.contains(languageCode)) {
        // If not available, fallback to the first available language
        languageCode = languages.isNotEmpty ? languages.first : languageCode;
        print(
          'ERROR: Desired language $languageCode not available. Using fallback: $languageCode',
        );
      }
      selectedLang = languageCode;
      await _stt.setLanguage(languageCode);

      await _stt.stop();
      _stt.onResultChanged.listen((result) {
        setupResultChanged(result);
      });

      await _stt.start(
        SttRecognitionOptions(
          offline: true,
          punctuation: true,
          contextualStrings: const [],
          android: const SttRecognitionAndroidOptions(),
          ios: const SttRecognitionIosOptions(),
          macos: const SttRecognitionMacosOptions(),
        ),
      );
      LOG.DEBUG('STT started with language: $languageCode');
    } catch (e) {
      LOG.ERROR('Error starting speech recognition: $e');
      setState(() {
        _micError = 'Speech recognition error: $e';
      });
    }
  }

  Future<void> _stopSpeechRecognition() async {
    await _stt.stop();
    // Do not clear recognized words on stop
  }

  void setupResultChanged(SttRecognition result) {
    LOG.DEBUG('Recognized words: ${result.text}');
    // Stop TTS whenever user starts to speak
    _tts.stop();
    AIService aiService = Provider.of<AIService>(context, listen: false);
    if (!result.isFinal) return;
    setState(() {
      _recognizedWords += result.text;
      // Start/reset a timer that gets cancelled if this callback is called again
      _timer?.cancel();
      _timer = Timer(const Duration(seconds: 2), () {
        // Timer action: clear recognized words after 2 seconds
        if (mounted) {
          aiService.generate(_recognizedWords.trim());
          setState(() {
            _recognizedWords = '';
            // send the result
          });
        }
      });

      LOG.DEBUG('Recognized words: ${result.text}');
    });

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _stt.stop();
      _stt.start(
        SttRecognitionOptions(
          offline: true,
          punctuation: true,
          contextualStrings: const [],

          android: const SttRecognitionAndroidOptions(),
          ios: const SttRecognitionIosOptions(),
          macos: const SttRecognitionMacosOptions(),
        ),
      );
    });
  }

  @override
  void initState() {
    super.initState();
    _initMicName();
    _stt.onResultChanged.listen((result) {
      setupResultChanged(result);
    });
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
    final ttsText = aiService.getTtsTextForResponse(_lastSpokenGeminiResult);
    if (ttsText != null) {
      _lastSpokenGeminiResult = aiService.lastResult;
      _tts.start(ttsText);
    }
    return Column(
      children: [
        Flexible(
          child: GeneratedImagesWidget(
            images: aiService.images,
            loading: aiService.generatingImage,
          ),
        ),

        SizedBox(
          height: 200,
          child: Center(
            child: _isRecording
                ? WaveformRecorder(
                    controller: _waveformController,
                    height: 120,
                    waveColor: Colors.cyan,
                  )
                : SizedBox(),
          ),
        ),
        MicInfoWidget(
          micError: _micError ?? '',
          selectedMicDevice: _selectedMicDevice,
          stt: _stt,
        ),
        if (Theme.of(context).platform == TargetPlatform.windows)
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                child: DropdownButton<InputDevice>(
                  value: _selectedMicDevice,
                  items: _micDevices
                      .map(
                        (device) => DropdownMenuItem<InputDevice>(
                          value: device,
                          child: SizedBox(
                            width: MediaQuery.sizeOf(context).width * 0.6,
                            child: Text(
                              device.label,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ),
                      )
                      .toList(),
                  onChanged: (device) {
                    setState(() {
                      _selectedMicDevice = device;
                      _micName = device?.label;
                    });
                  },
                  hint: const Text('Select microphone'),
                ),
              ),
            ],
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
                  _micError ?? _recognizedWords.trim().split(' ').last,
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
