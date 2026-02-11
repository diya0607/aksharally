import 'package:flutter/material.dart';

class TextDisplayWidget extends StatelessWidget {
  final String text;

  const TextDisplayWidget({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      width: double.infinity,
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
      ),
      child: SingleChildScrollView(
        child: Text(
          text.isEmpty
              ? 'Simplified text will appear here...'
              : text,
          style: const TextStyle(fontSize: 16),
        ),
      ),
    );
  }
}
