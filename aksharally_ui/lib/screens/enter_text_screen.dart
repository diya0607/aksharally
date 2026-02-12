import 'package:flutter/material.dart';
import 'reader_screen.dart';

class EnterTextScreen extends StatefulWidget {
  const EnterTextScreen({super.key});

  @override
  State<EnterTextScreen> createState() => _EnterTextScreenState();
}

class _EnterTextScreenState extends State<EnterTextScreen> {
  final TextEditingController controller = TextEditingController();

  void openReader() {
    if (controller.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please enter some text first"),
        ),
      );
      return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ReaderScreen(
          initialText: controller.text.trim(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Enter Text"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            /// TEXT INPUT AREA
            Expanded(
              child: TextField(
                controller: controller,
                maxLines: null,
                expands: true,
                decoration: const InputDecoration(
                  hintText: "Type or paste text here...",
                  border: OutlineInputBorder(),
                ),
              ),
            ),

            const SizedBox(height: 16),

            /// SIMPLIFY BUTTON
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: openReader,
                child: const Text("Simplify Text"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}