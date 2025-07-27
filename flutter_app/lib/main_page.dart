import 'dart:math';
import 'dart:convert';

import 'package:flutter_app/ai_service.dart';
import 'package:flutter_app/kid_printer_widget.dart';
import 'package:flutter/material.dart';
import 'printer_service.dart';
import 'generated_images_widget.dart';
import 'package:provider/provider.dart';

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Consumer2<AIService, PrinterService>(
        builder: (context, ai, printer, child) {
          return KidPrinterWidget();

          // ...existing code...
          /*
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
              if (ai.images.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(bottom: 24.0),
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.print),
                    label: const Text('Print Image'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size.fromHeight(48),
                    ),
                    onPressed: printer.printing
                        ? null
                        : () async {
                            final base64Image = ai.images.last;
                            try {
                              await printer.printImageRemote(
                                base64Image: base64Image,
                              );
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Image sent to printer!'),
                                ),
                              );
                            } catch (e) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text('Failed to print: $e')),
                              );
                            }
                          },
                  ),
                ),
            ],
          );*/
        },
      ),
    );
  }
}
