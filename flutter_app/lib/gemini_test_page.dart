import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'ai_service.dart';
import 'generated_images_widget.dart';

class GeminiTestPage extends StatefulWidget {
  const GeminiTestPage({super.key});

  @override
  State<GeminiTestPage> createState() => _GeminiTestPageState();
}

class _GeminiTestPageState extends State<GeminiTestPage> {
  final TextEditingController _controller = TextEditingController(
    text: 'Say hello to the world!',
  );

  @override
  Widget build(BuildContext context) {
    AIService aiService = Provider.of<AIService>(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Gemini Test')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(labelText: 'Prompt'),
              minLines: 1,
              maxLines: 3,
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: aiService.loading
                  ? null
                  : () => aiService.generate(_controller.text),
              child: aiService.loading
                  ? const CircularProgressIndicator()
                  : const Text('Send to AI'),
            ),
            const SizedBox(height: 24),
            if (aiService.lastResult != null)
              Text('Result:', style: Theme.of(context).textTheme.titleMedium),
            if (aiService.lastResult != null)
              Container(
                margin: const EdgeInsets.only(top: 8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.7),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(aiService.lastResult!),
              ),
            if (aiService.lastError != null)
              Text(
                'Error: ${aiService.lastError}',
                style: const TextStyle(color: Colors.red),
              ),
            Consumer<AIService>(
              builder: (context, ai, child) {
                return GeneratedImagesWidget(images: ai.images);
              },
            ),
          ],
        ),
      ),
    );
  }
}
