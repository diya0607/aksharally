import 'package:flutter/material.dart';
import 'screens/reader_screen.dart';

void main() {
  runApp(const AksharAllyApp());
}

class AksharAllyApp extends StatelessWidget {
  const AksharAllyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AksharAlly',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.deepPurple,
      ),
      home: const ReaderScreen(),
    );
  }
}
