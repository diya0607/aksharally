import 'package:flutter/material.dart';

class AppTheme {
  static const Color primaryPink = Color(0xFFE7B5C3);
  static const Color peachButton = Color(0xFFF5A77A);
  static const Color background = Color(0xFFFDF7F9);
  static const Color textDark = Color(0xFF2E2E2E);

  static ThemeData lightTheme = ThemeData(
    scaffoldBackgroundColor: background,
    fontFamily: 'Roboto',
    textTheme: const TextTheme(
      headlineMedium: TextStyle(
        fontSize: 26,
        fontWeight: FontWeight.bold,
        color: textDark,
      ),
      bodyMedium: TextStyle(
        fontSize: 16,
        color: textDark,
      ),
    ),
  );
}