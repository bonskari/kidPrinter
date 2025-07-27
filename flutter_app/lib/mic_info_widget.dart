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

    // 2. Device listing
    try {
      diag.writeln('Device listing: (skipped, see main widget)');
    } on TimeoutException {
      diag.writeln('Device listing: TIMEOUT');
    } catch (e) {
      diag.writeln('Device listing: ERROR ($e)');
    }

    // 3. Record plugin test (removed, now using waveform_recorder everywhere)
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
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.mic, color: Colors.cyanAccent),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                'Mic status: ${micError.isNotEmpty ? micError : 'OK'}',
                style: TextStyle(fontSize: 16),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            SizedBox(width: 16),
            IconButton(
              icon: Icon(Icons.info_outline, color: Colors.cyanAccent),
              tooltip: 'Run mic diagnostics',
              onPressed: () {
                showDialog(
                  context: context,
                  barrierDismissible: false,
                  builder: (ctx) {
                    return DiagnosticsDialog(
                      runDiagnostics: () => runDiagnostics(
                        context: context,
                        selectedMicDevice: selectedMicDevice,
                        stt: stt,
                      ),
                    );
                  },
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
