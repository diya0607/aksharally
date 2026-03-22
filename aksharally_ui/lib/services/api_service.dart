import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // For REAL PHONE (same WiFi)
  static const String baseUrl = "http://192.168.1.11:5000";

  static Future<String> processImage(File imageFile) async {
    final uri = Uri.parse('$baseUrl/process/ocr-format');

    try {
      final request = http.MultipartRequest('POST', uri);

      // Attach image
      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          imageFile.path,
        ),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      final responseBody = response.body;

      if (response.statusCode == 200) {
        final data = json.decode(responseBody);

        if (data['success'] == true) {
          return data['formatted_text'] ?? 'No text returned';
        } else {
          throw Exception(data['error']);
        }
      } else {
        throw Exception(
          'Backend error ${response.statusCode}: $responseBody',
        );
      }
    } catch (e) {
      throw Exception('Connection failed: $e');
    }
  }
}