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

    return AspectRatio(
      aspectRatio: 744 / 1048,
      child: loading
          ? Center(child: CircularProgressIndicator())
          : images.isEmpty || imageBytes == null
          ? Center(
              child: TweenAnimationBuilder<double>(
                tween: Tween(begin: 1.0, end: 1.3),
                duration: const Duration(seconds: 1),
                curve: Curves.easeInOut,
                builder: (context, scale, child) {
                  return Transform.scale(
                    scale: scale,
                    child: Icon(
                      imageBytes == null && images.isNotEmpty
                          ? Icons.error_outline
                          : Icons.image_not_supported,
                      color: Colors.purple,
                      size: 48,
                    ),
                  );
                },
                onEnd: () {},
                // Repeat the animation by rebuilding
                child: SizedBox.shrink(),
              ),
            )
          : GestureDetector(
              onTap: onImageTap,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: Align(
                  alignment: Alignment.topCenter,
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
    );
  }
}
