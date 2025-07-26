import 'dart:math';

import 'package:flutter_app/ai_service.dart';
import 'package:flutter_app/kid_printer_widget.dart';
import 'package:flutter/material.dart';
import 'gemini_test_page.dart';
import 'generated_images_widget.dart';
import 'package:provider/provider.dart';

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Consumer<AIService>(
        builder: (context, ai, child) {
          if (ai.loading) {
            // Show only the loading spinner, user prompt, and cancel button
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Expanded(
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        GeneratedImagesWidget(images: ai.images, loading: true),
                        if (ai.awaitingImageDescription &&
                            ai.lastResult != null &&
                            (ai.lastError == null || ai.lastError!.isEmpty))
                          Padding(
                            padding: const EdgeInsets.only(top: 16.0),
                            child: Text(
                              ai.lastResult!,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.black87,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(0, 0, 0, 24),
                  child: ElevatedButton(
                    onPressed: () {
                      Provider.of<AIService>(
                        context,
                        listen: false,
                      ).cancelGeneration();
                    },
                    child: const Text('Cancel'),
                  ),
                ),
              ],
            );
          }
          // ...existing code...
          return Column(
            children: [
              GeneratedImagesWidget(images: ai.images, loading: false),
              const Expanded(child: KidPrinterWidget()),
              Padding(
                padding: const EdgeInsets.fromLTRB(0, 0, 0, 24),
                child: ElevatedButton(
                  onPressed: () {
                    final words = [
                      'megaman',
                      'turtles',
                      'sonic',
                      'superkitties',
                      'zelda',
                      'super mario',
                    ];
                    final randomWord = (words..shuffle(Random())).first;
                    Provider.of<AIService>(
                      context,
                      listen: false,
                    ).generateColoringBookImage(subject: randomWord);
                  },
                  child: const Text('Generate Random Coloring Book Image'),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
