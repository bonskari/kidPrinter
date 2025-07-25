import 'package:flutter/material.dart';
import 'package:audio_waveforms/audio_waveforms.dart';

class FullscreenWaveform extends StatelessWidget {
  final bool isListening;
  final RecorderController recorderController;

  const FullscreenWaveform({
    Key? key,
    required this.isListening,
    required this.recorderController,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (!isListening) return const SizedBox.shrink();
    return Container(
      color: Colors.transparent,
      child: Center(
        child: AudioWaveforms(
          enableGesture: false,
          size: Size(double.infinity, 200),
          recorderController: recorderController,
          waveStyle: const WaveStyle(
            waveColor: Colors.blueAccent,
            extendWaveform: true,
            showMiddleLine: false,
            spacing: 6,
            showBottom: false,
            showTop: false,
          ),
        ),
      ),
    );
  }
}
