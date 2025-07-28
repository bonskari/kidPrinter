import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:stts/stts.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:async';
import 'diagnostics_dialog.dart';

class MicInfoWidget extends StatelessWidget {
  final String micError;
  final InputDevice? selectedMicDevice;
  final Stt stt;

  const MicInfoWidget({
    Key? key,
    required this.micError,
    required this.selectedMicDevice,
    required this.stt,
  }) : super(key: key);

  static Future<String> runDiagnostics({
    required BuildContext context,
    required InputDevice? selectedMicDevice,
    required Stt stt,
  }) async {
    StringBuffer diag = StringBuffer();
    diag.writeln('--- Microphone Diagnostics ---');
    diag.writeln('Microphone selection is not supported.');
    diag.writeln('Using default system microphone.');
    diag.writeln('Device listing: Not available.');
    // 1. Microphone permission (before mic tests)
    try {
      final micStatus = await Permission.microphone.request().timeout(
        const Duration(seconds: 2),
      );
      diag.writeln(
        'Microphone permission: ${micStatus.isGranted ? 'GRANTED' : 'DENIED'}',
      );
      if (!micStatus.isGranted) {
        diag.writeln(
          'Microphone permission not granted, skipping mic diagnostics.',
        );
        return diag.toString();
      }
    } on TimeoutException {
      diag.writeln('Microphone permission: TIMEOUT');
      return diag.toString();
    } catch (e) {
      diag.writeln('Microphone permission: ERROR ($e)');
      return diag.toString();
    }

    diag.writeln('Record plugin: replaced by waveform_recorder');

    // 4. STTS plugin test
    try {
      await stt.stop().timeout(const Duration(seconds: 2));
      await stt
          .start(
            SttRecognitionOptions(
              offline: true,
              punctuation: true,
              contextualStrings: const [],
              android: const SttRecognitionAndroidOptions(),
              ios: const SttRecognitionIosOptions(),
              macos: const SttRecognitionMacosOptions(),
            ),
          )
          .timeout(const Duration(seconds: 2));
      await Future.delayed(const Duration(milliseconds: 500));
      await stt.stop().timeout(const Duration(seconds: 2));
      diag.writeln('STTS plugin: OK (started and stopped)');
    } on TimeoutException {
      diag.writeln('STTS plugin: TIMEOUT');
    } catch (e) {
      diag.writeln('STTS plugin: ERROR ($e)');
    }
    return diag.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.08),
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (micError.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Text(
                  micError,
                  style: const TextStyle(color: Colors.redAccent),
                ),
              ),

            // ...existing code...
          ],
        ),
      ),
    );
  }
}
