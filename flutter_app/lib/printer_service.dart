import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
// Removed printing package and Uint8List import as local printing logic is no longer needed.

class PrinterService extends ChangeNotifier {
  String _lastRemoteResult = '';
  String get lastRemoteResult => _lastRemoteResult;
  bool _printing = false;
  bool get printing => _printing;
  String? _lastError;
  String? get lastError => _lastError;

  /// Print an image by uploading to a remote print server
  Future<void> printImageRemote({
    required Uint8List base64Image,
    String url = 'http://192.168.50.203/print_service/print',
    String filename = 'image.png',
  }) async {
    _printing = true;
    _lastError = null;
    _lastRemoteResult = '';
    notifyListeners();
    try {
      final imageBytes = base64Image;
      final request = http.MultipartRequest('POST', Uri.parse(url))
        ..files.add(
          http.MultipartFile.fromBytes('image', imageBytes, filename: filename),
        );
      final response = await request.send();
      final respStr = await response.stream.bytesToString();
      _lastRemoteResult = respStr;
    } catch (e) {
      _lastError = e.toString();
    } finally {
      _printing = false;
      notifyListeners();
    }
  }
}
