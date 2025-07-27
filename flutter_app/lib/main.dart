import 'package:flutter/material.dart';
import 'dart:io' show Platform;
import 'package:wakelock_plus/wakelock_plus.dart';
import 'main_page.dart';
import 'window_config.dart';
import 'config.dart';
import 'ai_service.dart';
import 'printer_service.dart';
import 'package:provider/provider.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isAndroid) {
    WakelockPlus.enable();
  }
  // Set desktop window to Android aspect ratio
  // (requires window_size package and window_config.dart)
  try {
    // Set initial window size and aspect ratio
    setAndroidAspectWindow();
    // After a short delay, remove min/max constraints to allow free resizing
    Future.delayed(const Duration(milliseconds: 500), () {
      setWindowMinSizeUnconstrained();
      setWindowMaxSizeUnconstrained();
    });
  } catch (_) {}
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AIService(geminiApiKey)),
        ChangeNotifierProvider(create: (_) => PrinterService()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Colors.black,
        appBarTheme: const AppBarTheme(backgroundColor: Colors.black),
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.dark,
          surface: Colors.black,
        ),
      ),
      home: const MainPage(),
    );
  }
}
