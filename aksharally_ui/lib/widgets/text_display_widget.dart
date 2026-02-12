import 'package:flutter/material.dart';

class TextDisplayWidget extends StatelessWidget {
  final String text;
  final double fontSize;
  final double lineSpacing;

  const TextDisplayWidget({
    super.key,
    required this.text,
    required this.fontSize,
    required this.lineSpacing,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Text(
        text,
        style: TextStyle(
          fontSize: fontSize,
          height: lineSpacing,
        ),
      ),
    );
  }
}