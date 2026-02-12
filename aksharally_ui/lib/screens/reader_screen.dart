import 'dart:io';
import 'package:flutter/material.dart';
import '../services/library_storage.dart';
import '../models/library_item.dart';
import '../widgets/image_picker_widget.dart';
import '../widgets/text_display_widget.dart';
import '../theme/app_settings.dart';

class ReaderScreen extends StatefulWidget {
  /// NEW: allows text to be passed from Enter Text screen
  final String? initialText;

  const ReaderScreen({super.key, this.initialText});

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  File? selectedImage;
  String simplifiedText = '';
  bool isLoading = false;

  /// Runs when screen opens
  @override
  void initState() {
    super.initState();

    /// If text is passed from Enter Text screen
    if (widget.initialText != null) {
      simplifiedText = widget.initialText!;
    }
  }

  /// BACKGROUND COLOR BASED ON SETTINGS
  Color getBackgroundColor() {
    if (AppSettings.themeMode == 1) {
      return const Color(0xFF1E1E1E); // Dark
    }
    if (AppSettings.themeMode == 2) {
      return const Color(0xFFF4ECD8); // Sepia
    }
    return Colors.white;
  }

  /// TEXT COLOR BASED ON SETTINGS
  Color getTextColor() {
    return AppSettings.themeMode == 1
        ? Colors.white
        : Colors.black;
  }

  void onImageSelected(File image) {
    setState(() {
      selectedImage = image;
      simplifiedText = '';
    });
  }

  /// Backend logic remains untouched
  Future<void> onSimplifyPressed() async {
    setState(() {
      isLoading = true;
    });

    await Future.delayed(const Duration(seconds: 1));

    setState(() {
      simplifiedText =
          "Simplified text will appear here after backend integration.";
      isLoading = false;
      LibraryStorage.addItem(
  LibraryItem(
    title: "Reading ${DateTime.now().hour}:${DateTime.now().minute}",
    content: simplifiedText,
    date: DateTime.now(),
  ),
);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: getBackgroundColor(),
      appBar: AppBar(
        title: const Text(
          'AksharAlly',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            /// IMAGE PICKER
            ImagePickerWidget(onImageSelected: onImageSelected),

            const SizedBox(height: 16),

            /// SIMPLIFY BUTTON
            ElevatedButton(
              onPressed: isLoading ? null : onSimplifyPressed,
              child: const Text('Simplify Text'),
            ),

            const SizedBox(height: 16),

            /// TEXT DISPLAY
            Expanded(
              child: isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : TextDisplayWidget(
                      text: simplifiedText.isEmpty
                          ? 'Simplified text will appear here...'
                          : simplifiedText,
                      fontSize: AppSettings.fontSize,
                      lineSpacing: AppSettings.lineSpacing,
                      textColor: getTextColor(),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}