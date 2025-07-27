import 'package:flutter/material.dart';
import 'dart:math' as math;

class IdleWaveform extends StatelessWidget {
  final double phase;
  const IdleWaveform({Key? key, required this.phase}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;
        return CustomPaint(
          size: Size(width, 80),
          painter: _IdleWaveformPainter(phase),
        );
      },
    );
  }
}

class _IdleWaveformPainter extends CustomPainter {
  final double phase;
  _IdleWaveformPainter(this.phase);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blueAccent
      ..strokeWidth = 4
      ..style = PaintingStyle.stroke;

    final path = Path();
    final midY = size.height / 2;
    final amplitude = 25.0;
    final waveLength = size.width / 2;

    for (double x = 0; x <= size.width; x += 1) {
      double y =
          midY +
          amplitude *
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
  bool shouldRepaint(covariant _IdleWaveformPainter oldDelegate) =>
      oldDelegate.phase != phase;
}
