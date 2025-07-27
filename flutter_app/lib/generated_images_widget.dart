import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_app/log.dart';

class GeneratedImagesWidget extends StatelessWidget {
  final List<Uint8List> images;
  final bool loading;
  final void Function()? onImageTap;

  const GeneratedImagesWidget({
    super.key,
    required this.images,
    this.loading = false,
    this.onImageTap,
  });

  @override
  Widget build(BuildContext context) {
    Uint8List? imageBytes;
    if (images.isNotEmpty) {
      try {
        imageBytes = images.last;
        // imageBytes = base64Decode(images.last);
      } catch (e) {
        LOG.ERROR('Base64 decode failed: $e');
        imageBytes = null;
      }
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: AspectRatio(
        aspectRatio: 720 / 1280,
        child: loading
            ? Center(child: CircularProgressIndicator())
            : images.isEmpty || imageBytes == null
            ? Center(
                child: Text(
                  imageBytes == null
                      ? 'Image decode error.'
                      : 'No generated images yet.',
                  style: TextStyle(color: Colors.grey),
                ),
              )
            : GestureDetector(
                onTap: onImageTap,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: Align(
                    alignment: Alignment.topCenter,
                    child: Container(
                      padding: const EdgeInsets.all(8),
                      color: Colors.red,
                      child: Image.memory(
                        imageBytes,
                        width: double.infinity,
                        height: double.infinity,
                        errorBuilder: (ctx, err, stack) => Container(
                          width: double.infinity,
                          height: double.infinity,
                          color: Colors.grey.shade200,
                          child: Icon(Icons.broken_image, color: Colors.purple),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}
