import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // Use this for REAL PHONE (same WiFi)
  static const String baseUrl = "http://192.168.1.11:5000";

  // Use this for emulator (if needed)
  // static const String baseUrl = "http://10.0.2.2:5000";

  static Future<String> processImage(File imageFile) async {
    final uri = Uri.parse('$baseUrl/process');

    try {
      final request = http.MultipartRequest('POST', uri);

      // Send image
      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          imageFile.path,
        ),
      );

      // Send language
      request.fields['language'] = 'eng';

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);
      final responseBody = response.body;
      if (response.statusCode == 200) {
        final data = json.decode(responseBody);

        if (data['success'] == true) {
          return data['simplified_text'] ?? 'No text returned';
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