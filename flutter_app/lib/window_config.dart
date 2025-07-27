import 'dart:io';
import 'package:flutter/widgets.dart';
import 'package:window_size/window_size.dart';

void setWindowMinSizeUnconstrained() {
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    setWindowMinSize(const Size(0, 0));
  }
}

void setWindowMaxSizeUnconstrained() {
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    setWindowMaxSize(const Size(double.infinity, double.infinity));
  }
}

void setAndroidAspectWindow() {
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    // Samsung S10e reference resolution: 1080x2280 (aspect ratio ~9:19.0)
    const double baseWidth = 1080;
    const double baseHeight = 2280;
    final double width = baseWidth * 0.8;
    final double height = baseHeight * 0.8;
    setWindowMinSize(Size(width, height));
    setWindowMaxSize(Size(width, height));
    setWindowFrame(Rect.fromLTWH(100, 100, width, height));
  }
}
