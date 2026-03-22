import 'dart:io';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/api_service.dart';
import '../services/library_storage.dart';
import '../models/library_item.dart';
import '../services/tts_service.dart';
import '../theme/app_settings.dart';

class ReaderScreen extends StatefulWidget {
  final String? initialText;

  const ReaderScreen({super.key, this.initialText});

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  File? selectedImage;
  String simplifiedText = '';
  bool isLoading = false;

  final TTSService _tts = TTSService();

  double speechRate = 0.4;
  bool autoRead = true;

  List<String> words = [];
  int currentIndex = -1;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _tts.init();

    if (widget.initialText != null) {
      simplifiedText = widget.initialText!;
      words = simplifiedText.split(" ");
    }
  }

  Color getBackgroundColor() {
    if (AppSettings.themeMode == 1) {
      return const Color(0xFF1E1E1E);
    }
    if (AppSettings.themeMode == 2) {
      return const Color(0xFFF4ECD8);
    }
    return Colors.white;
  }

  Color getTextColor() {
    return AppSettings.themeMode == 1 ? Colors.white : Colors.black;
  }

  Future<void> pickImage() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);

    if (picked != null) {
      setState(() {
        selectedImage = File(picked.path);
        simplifiedText = '';
        words = [];
      });
    }
  }

  Future<void> onSimplifyPressed() async {
    if (selectedImage == null) {
      setState(() {
        simplifiedText = "⚠️ Please select an image first.";
      });
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      final result = await ApiService.processImage(selectedImage!);

      setState(() {
        simplifiedText = result;
        words = result.split(" ");

        LibraryStorage.addItem(
          LibraryItem(
            title: "Reading ${DateTime.now().hour}:${DateTime.now().minute}",
            content: simplifiedText,
            date: DateTime.now(),
          ),
        );
      });

      if (autoRead) {
        await _tts.setRate(speechRate);
        startReading();
      }

    } catch (e) {
      setState(() {
        simplifiedText = "❌ Error: $e";
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void startReading() async {
    if (simplifiedText.isEmpty) return;

    await _tts.setRate(speechRate);
    currentIndex = 0;

    await _tts.speak(simplifiedText);

    _timer?.cancel();
    _timer = Timer.periodic(const Duration(milliseconds: 400), (timer) {
      if (currentIndex < words.length - 1) {
        setState(() {
          currentIndex++;
        });
      } else {
        timer.cancel();
      }
    });
  }

  void stopReading() async {
    await _tts.stop();
    _timer?.cancel();

    setState(() {
      currentIndex = -1;
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _tts.stop();
    super.dispose();
  }

  Widget buildHighlightedText() {
    if (simplifiedText.isEmpty) {
      return Text(
        'Simplified text will appear here...',
        style: TextStyle(
          fontSize: AppSettings.fontSize,
          color: getTextColor(),
        ),
      );
    }

    return Wrap(
      spacing: 6,
      runSpacing: 10,
      children: List.generate(words.length, (index) {
        return Text(
          words[index],
          style: TextStyle(
            fontSize: AppSettings.fontSize,
            height: AppSettings.lineSpacing,
            color: index == currentIndex ? Colors.red : getTextColor(),
            fontWeight:
                index == currentIndex ? FontWeight.bold : FontWeight.normal,
          ),
        );
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: getBackgroundColor(),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        title: const Text(
          'AksharAlly',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            /// IMAGE CARD
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                color: Colors.grey.shade100,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 8,
                    offset: Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                children: [
                  Container(
                    height: 180,
                    width: double.infinity,
                    child: selectedImage == null
                        ? const Center(child: Text("📷 No image selected"))
                        : ClipRRect(
                            borderRadius: BorderRadius.circular(16),
                            child: Image.file(selectedImage!, fit: BoxFit.cover),
                          ),
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton.icon(
                    onPressed: pickImage,
                    icon: const Icon(Icons.image),
                    label: const Text("Choose Image"),
                  ),
                  const SizedBox(height: 10),
                ],
              ),
            ),

            const SizedBox(height: 20),

            /// SIMPLIFY BUTTON
            ElevatedButton(
              onPressed: isLoading ? null : onSimplifyPressed,
              child: isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Simplify Text"),
            ),

            const SizedBox(height: 20),

            /// CONTROLS CARD
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                color: Colors.grey.shade100,
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton(
                          onPressed: simplifiedText.isEmpty ? null : startReading,
                          child: const Text("▶ Start"),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: stopReading,
                          child: const Text("⏹ Stop"),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 10),

                  SwitchListTile(
                    title: const Text("Auto Read"),
                    value: autoRead,
                    onChanged: (value) {
                      setState(() {
                        autoRead = value;
                      });
                    },
                  ),

                  const Text("Speech Speed"),
                  Slider(
                    value: speechRate,
                    min: 0.2,
                    max: 0.8,
                    divisions: 6,
                    label: speechRate.toStringAsFixed(1),
                    onChanged: (value) {
                      setState(() {
                        speechRate = value;
                      });
                      _tts.setRate(value);
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            /// OUTPUT CARD
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                color: Colors.grey.shade100,
                boxShadow: [
                  BoxShadow(color: Colors.black12, blurRadius: 6),
                ],
              ),
              child: buildHighlightedText(),
            ),
          ],
        ),
      ),
    );
  }
}