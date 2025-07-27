import 'package:flutter/material.dart';
import 'waveform_test_widget.dart';

class DiagnosticsDialog extends StatefulWidget {
  final Future<String> Function() runDiagnostics;
  const DiagnosticsDialog({Key? key, required this.runDiagnostics})
    : super(key: key);

  @override
  State<DiagnosticsDialog> createState() => DiagnosticsDialogState();
}

class DiagnosticsDialogState extends State<DiagnosticsDialog> {
  String? result;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    widget.runDiagnostics().then((value) {
      if (mounted) {
        setState(() {
          result = value;
          loading = false;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Microphone Diagnostics'),
      content: SizedBox(
        width: 350,
        height: 340,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: loading
                  ? Center(child: CircularProgressIndicator())
                  : Scrollbar(
                      child: SingleChildScrollView(
                        child: Text(
                          result ?? '',
                          style: const TextStyle(fontSize: 14),
                        ),
                      ),
                    ),
            ),
            const Divider(height: 24),
            const Text(
              'Waveform Test:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 140, child: WaveformTestWidget()),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Close'),
        ),
      ],
    );
  }
}
