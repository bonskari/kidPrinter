import 'dart:math';

import 'package:flutter_app/generated_images_widget.dart';
import 'package:flutter_app/printer_service.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:record/record.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'dart:async';
import 'idle_waveform.dart';
import 'live_waveform.dart';
import 'package:stts/stts.dart';
import 'log.dart';
import 'package:provider/provider.dart';
import 'ai_service.dart';
import 'kid_printer_button.dart';

class KidPrinterWidget extends StatefulWidget {
  const KidPrinterWidget({super.key});

  @override
  State<KidPrinterWidget> createState() => _KidPrinterWidgetState();
}

class _KidPrinterWidgetState extends State<KidPrinterWidget>
    with SingleTickerProviderStateMixin {
  bool _imageLoading = false;

  /// Cleans Gemini response for TTS: removes __IMAGE__ prefix if present, and trims.
  String cleanGeminiResponseForTTS(String response) {
    final trimmed = response.trim();
    if (trimmed.startsWith('__IMAGE__')) {
      return trimmed.replaceFirst('__IMAGE__', '').trim();
    }
    return trimmed;
  }

  // Removed TTS (text-to-speech) related code
  String _recognizedWords = '';
  String? _micName;
  String? _micError;
  List<InputDevice> _micDevices = [];
  InputDevice? _selectedMicDevice;
  final AudioRecorder _recorder = AudioRecorder();
  StreamSubscription<Amplitude>? _amplitudeSub;
  // Removed _speechResultSub, using stts
  late final Ticker _ticker;
  double _phase = 0.0;
  bool isListening = false;
  double _amplitude = 0.0;
  String selectedLang = ''; // Default language
  final Stt _stt = Stt();
  Timer? _timer;
  List<String> _availableLanguages = [];
  final Tts _tts = Tts();
  String? _lastSpokenGeminiResult;

  void _stopRecording() async {
    await _recorder.stop();
    await _amplitudeSub?.cancel();
    setState(() {
      _amplitude = 0.0;
    });
  }

  Future<void> _startRecording() async {
    final status = await Permission.microphone.request();
    if (!status.isGranted) {
      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Microphone Permission'),
            content: const Text(
              'Microphone permission is required to record audio.',
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
      return;
    }
    // Refresh mic list after permission granted
    try {} catch (e, st) {
      LOG.ERROR('Exception in _initMicName: $e\n$st');
      setState(() {
        _micError = 'Mic device listing failed: $e';
      });
      return;
    }
    if (_selectedMicDevice == null) {
      LOG.ERROR(
        'No microphone device selected. Please select a device from the dropdown. $_selectedMicDevice',
      );
    }
    LOG.DEBUG('Starting recording. Selected device:');
    LOG.DEBUG('  label: ${_selectedMicDevice?.label}');
    LOG.DEBUG('  id: ${_selectedMicDevice?.id}');
    LOG.DEBUG('  toString: ${_selectedMicDevice?.toString()}');

    try {
      await _recorder.start(
        RecordConfig(
          encoder: AudioEncoder.wav,
          numChannels: 1,
          bitRate: 16000,
          sampleRate: 44100,
          device: _selectedMicDevice, // Use default device
        ),
        path: 'temp_record.wav',
      );
    } catch (e, st) {
      LOG.ERROR('Exception in _recorder.start: $e\n$st');
      setState(() {
        _micError = 'Recording failed: $e';
      });
      return;
    }
    _amplitudeSub?.cancel();
    _amplitudeSub = _recorder
        .onAmplitudeChanged(const Duration(milliseconds: 50))
        .listen((amp) {
          setState(() {
            final db = amp.current;
            // Non-linear scaling for sharper, higher peaks
            double norm = ((db + 60) / 60).clamp(0.0, 1.0);
            // Exaggerate high values: quadratic scaling and boost
            _amplitude = (norm * norm * 4.0).clamp(0.0, 2.5);
          });
        });
  }

  void _toggleListening() {
    setState(() {
      isListening = !isListening;
      _recognizedWords = "";
      if (isListening) {
        _startRecording();
        _startSpeechRecognition();
      } else {
        _stopRecording();
        _stopSpeechRecognition();
        _tts.stop(); // Ensure TTS stops when listening is stopped
      }
    });
  }

  Future<void> _initMicName() async {
    LOG.DEBUG('_initMicName called');
    try {
      final devices = await _recorder.listInputDevices();
      LOG.DEBUG('Devices found: ${devices.map((d) => d.label).toList()}');
      setState(() {
        _micDevices = devices;
        _micError = null;
        if (devices.isNotEmpty) {
          _selectedMicDevice = devices.first;
          _micName = devices.first.label;
          LOG.DEBUG('Mic name set to: $_micName');
        } else {
          _micName = 'No mic found';
          _selectedMicDevice = null;
          LOG.DEBUG('No mic found');
        }
      });
    } catch (e, st) {
      LOG.ERROR('Mic info error: $e\n$st');
      setState(() {
        _micName = 'Mic info error';
        _selectedMicDevice = null;
        _micError = 'Mic device listing failed: $e';
      });
      rethrow;
    }
  }

  Future<void> _startSpeechRecognition() async {
    // Start listening with stts, set language to Finnish
    String languageCode = 'fi-FI';
    // Check if the available languages contain the desired languageCode
    final languages = await _stt.getLanguages();
    _availableLanguages = languages;
    if (!languages.contains(languageCode)) {
      // If not available, fallback to the first available language
      languageCode = languages.isNotEmpty ? languages.first : languageCode;
      print(
        'ERROR: Desired language $languageCode not available. Using fallback: $languageCode',
      );
    }
    selectedLang = languageCode;
    _stt.setLanguage(languageCode);

    _stt.stop();
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
  }

  Future<void> _stopSpeechRecognition() async {
    await _stt.stop();
    // Do not clear recognized words on stop
  }

  void setupResultChanged(SttRecognition result) {
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
    _ticker = createTicker((elapsed) {
      setState(() {
        _phase += 0.03;
      });
    })..start();

    // Get the current microphone name on init
    _initMicName();

    // Listen to stts result changes and update recognized words or image prompt
    _stt.onResultChanged.listen((result) {
      setupResultChanged(result);
    });
  }

  @override
  void dispose() {
    _ticker.dispose();
    _amplitudeSub?.cancel();
    _tts.dispose();
    // Removed vosk SpeechService dispose logic, using stts
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    AIService aiService = Provider.of<AIService>(context, listen: true);
    PrinterService printerService = Provider.of<PrinterService>(
      context,
      listen: true,
    );
    // Speak AI response if new and not already spoken
    final ttsText = aiService.getTtsTextForResponse(_lastSpokenGeminiResult);
    if (ttsText != null) {
      _lastSpokenGeminiResult = aiService.lastResult;
      _tts.start(ttsText);
    }

    if (aiService.loading) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                GeneratedImagesWidget(images: aiService.images, loading: true),
              ],
            ),
          ),

          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 0, 24),
            child: ElevatedButton(
              onPressed: () {
                Provider.of<AIService>(
                  context,
                  listen: false,
                ).cancelGeneration();
              },
              child: const Text('Cancel'),
            ),
          ),
        ],
      );
    } else {
      // Main page content
      return Column(
        children: [
          Spacer(),
          Expanded(
            child: GeneratedImagesWidget(
              images: aiService.images,
              loading: false,
            ),
          ),
          Spacer(),
          // Wave animation row
          SizedBox(
            height: 200,
            child: Stack(
              children: [
                isListening
                    ? Center(
                        child: LiveWaveform(
                          amplitude: _amplitude.clamp(0.0, 1.5),
                          phase: _phase,
                        ),
                      )
                    : Center(child: IdleWaveform(phase: _phase)),
              ],
            ),
          ),
          Spacer(),
          // Microphone dropdown row
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: DropdownButton<InputDevice>(
              value: _selectedMicDevice,
              items: _micDevices
                  .map(
                    (device) => DropdownMenuItem<InputDevice>(
                      value: device,
                      child: Text(device.label),
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
          // TEXT FIELD
          if (_recognizedWords.isNotEmpty || _micError != null)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 4,
                  ),
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
              child: Text(
                aiService.lastError!,
                textAlign: TextAlign.center,
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
                  onPressed: _toggleListening,
                  icon: isListening ? Icons.stop : Icons.mic,
                  loading: false,
                  disabled: false,
                ),
                if (aiService.images.isNotEmpty)
                  KidPrinterButton(
                    onPressed: () async {
                      try {
                        // Implement your print logic here
                        final base64Image = aiService.images.last;

                        await printerService.printImageRemote(
                          base64Image: base64Image,
                        );
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Image sent to printer!'),
                          ),
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
    /*
    return Column(
      mainAxisSize: MainAxisSize.max,
      children: [
        Consumer2<AIService, PrinterService>(
          builder: (context, ai, printer, child) {
            return Padding(
              padding: const EdgeInsets.fromLTRB(0, 0, 0, 24),
              child: ElevatedButton(
                onPressed: () {
                  Provider.of<AIService>(
                    context,
                    listen: false,
                  ).cancelGeneration();
                },
                child: const Text('Cancel'),
              ),
            );
          },
        ),
  
         if (ai.loading) {
            // Show only the loading spinner, user prompt, and cancel button
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Expanded(
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        GeneratedImagesWidget(images: ai.images, loading: true),
                        if (ai.awaitingImageDescription &&
                            ai.lastResult != null &&
                            (ai.lastError == null || ai.lastError!.isEmpty))
                          Padding(
                            padding: const EdgeInsets.only(top: 16.0),
                            child: Text(
                              ai.lastResult!,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.black87,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(0, 0, 0, 24),
                  child: ElevatedButton(
                    onPressed: () {
                      Provider.of<AIService>(
                        context,
                        listen: false,
                      ).cancelGeneration();
                    },
                    child: const Text('Cancel'),
                  ),
                ),
              ],
            );
          }]),
        // Image row (top)
        if (_imageLoading)
          const Padding(
            padding: EdgeInsets.all(8),
            child: CircularProgressIndicator(),
          ),
        if (_geminiImages.isNotEmpty)
          // TEST COMMENT: This is a test for git status visibility
          Expanded(
            child: Center(
              child: Image.memory(
                Uri.parse(
                  'data:image/png;base64,${_geminiImages[0]}',
                ).data!.contentAsBytes(),
                fit: BoxFit.contain,
                width: double.infinity,
                height: double.infinity,
              ),
            ),
          ),
        // Wave animation row
        SizedBox(
          height: 200,
          child: Stack(
            children: [
              isListening
                  ? Center(
                      child: LiveWaveform(
                        amplitude: _amplitude.clamp(0.0, 1.5),
                        phase: _phase,
                      ),
                    )
                  : Center(child: IdleWaveform(phase: _phase)),
            ],
          ),
        ),
        // Microphone dropdown row
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: DropdownButton<InputDevice>(
            value: _selectedMicDevice,
            items: _micDevices
                .map(
                  (device) => DropdownMenuItem<InputDevice>(
                    value: device,
                    child: Text(device.label),
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
        // Message/error field row
        if (_recognizedWords.isNotEmpty || _micError != null)
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
    );
    */
  }
}
