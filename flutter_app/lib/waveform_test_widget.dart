import 'package:flutter/material.dart';
import 'package:waveform_recorder/waveform_recorder.dart';

class WaveformTestWidget extends StatefulWidget {
  const WaveformTestWidget({Key? key}) : super(key: key);

  @override
  State<WaveformTestWidget> createState() => _WaveformTestWidgetState();
}

class _WaveformTestWidgetState extends State<WaveformTestWidget> {
  final _recorderController =
      WaveformRecorderController(); // API may have changed, but keep for now
  bool _isRecording = false;
  String? _error;

  @override
  void dispose() {
    _recorderController.dispose();
    super.dispose();
  }

  void _toggleRecording() async {
    try {
      if (_isRecording) {
        await _recorderController.stopRecording();
      } else {
        await _recorderController.startRecording();
      }
      setState(() {
        _isRecording = !_isRecording;
        _error = null;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(_isRecording ? 'Recording...' : 'Tap to record'),
        if (_error != null)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text(
              'Error: $_error',
              style: const TextStyle(color: Colors.red),
            ),
          ),
        SizedBox(height: 16),
        if (_isRecording)
          SizedBox(
            height: 120,
            child: WaveformRecorder(
              controller: _recorderController,
              height: 120,
              waveColor: Colors.cyan,
            ),
          ),
        SizedBox(height: 16),
        ElevatedButton(
          onPressed: _toggleRecording,
          child: Text(_isRecording ? 'Stop' : 'Start'),
        ),
      ],
    );
  }
}
