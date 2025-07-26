import 'dart:convert';
import 'package:flutter/material.dart';

class GeneratedImagesWidget extends StatelessWidget {
  final List<String> images;
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
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: AspectRatio(
        aspectRatio: 1,
        child: loading
            ? Center(child: CircularProgressIndicator())
            : images.isEmpty
            ? Center(
                child: Text(
                  'No generated images yet.',
                  style: TextStyle(color: Colors.grey),
                ),
              )
            : GestureDetector(
                onTap: onImageTap,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: Image.memory(
                    base64Decode(images.last),
                    width: double.infinity,
                    height: double.infinity,
                    fit: BoxFit.cover,
                    errorBuilder: (ctx, err, stack) => Container(
                      width: double.infinity,
                      height: double.infinity,
                      color: Colors.grey.shade200,
                      child: Icon(Icons.broken_image, color: Colors.red),
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}
