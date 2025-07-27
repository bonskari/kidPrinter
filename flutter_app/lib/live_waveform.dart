import 'package:flutter/material.dart';
import 'dart:math' as math;

class LiveWaveform extends StatelessWidget {
  final double amplitude;
  final double phase;
  const LiveWaveform({super.key, required this.amplitude, required this.phase});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;

        return CustomPaint(
          size: Size(width, 80),
          painter: _LiveWaveformPainter(amplitude, phase),
        );
      },
    );
  }
}

class _LiveWaveformPainter extends CustomPainter {
  final double amplitude;
  final double phase;
  _LiveWaveformPainter(this.amplitude, this.phase);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.cyanAccent
      ..strokeWidth = 4
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final path = Path();
    final midY = size.height / 2;
    final visualAmp = 2.0 + (amplitude.clamp(0.0, 1.0) * 48.0);
    final waveLength = size.width / 2;

    for (double x = 0; x <= size.width; x += 1) {
      double y =
          midY +
          visualAmp *
              (0.5 * (1 + math.sin(phase + x / waveLength * 2 * math.pi)));
      if (x == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant _LiveWaveformPainter oldDelegate) =>
      oldDelegate.amplitude != amplitude || oldDelegate.phase != phase;
}
