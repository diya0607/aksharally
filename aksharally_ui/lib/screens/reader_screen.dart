import 'dart:io';
import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../widgets/image_picker_widget.dart';
import '../widgets/text_display_widget.dart';

class ReaderScreen extends StatefulWidget {
  const ReaderScreen({super.key});

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  File? selectedImage;
  String simplifiedText = '';
  bool isLoading = false;

  // Called when an image is picked
  void onImageSelected(File image) {
    setState(() {
      selectedImage = image;
      simplifiedText = '';
    });
  }

  // Called when "Simplify Text" button is pressed
  Future<void> onSimplifyPressed() async {
    if (selectedImage == null) return;

    setState(() {
      isLoading = true;
      simplifiedText = '';
    });

    try {
      final result =
          await ApiService.simplifyTextFromImage(selectedImage!);

      setState(() {
        simplifiedText = result;
      });
    } catch (e) {
      setState(() {
        simplifiedText = 'Error connecting to backend.';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
            ImagePickerWidget(onImageSelected: onImageSelected),
            const SizedBox(height: 16),

            ElevatedButton(
              onPressed:
                  selectedImage == null || isLoading ? null : onSimplifyPressed,
              child: const Text('Simplify Text'),
            ),

            const SizedBox(height: 16),

            Expanded(
              child: isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : TextDisplayWidget(
                      text: simplifiedText.isEmpty
                          ? 'Simplified text will appear here...'
                          : simplifiedText,
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
