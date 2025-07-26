import 'package:flutter/material.dart';
import 'dart:io' show Platform;
import 'package:wakelock_plus/wakelock_plus.dart';
import 'main_page.dart';
import 'config.dart';
import 'ai_service.dart';
import 'package:provider/provider.dart';

void main() {
  if (Platform.isAndroid) {
    WakelockPlus.enable();
  }
  runApp(
    ChangeNotifierProvider(
      create: (_) => AIService(geminiApiKey, stableDiffusionApiKey),
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
