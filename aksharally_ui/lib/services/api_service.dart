import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // Android emulator → host machine
  static const String baseUrl = 'http://192.168.0.100:5000';

  static Future<String> simplifyTextFromImage(File imageFile) async {
    final uri = Uri.parse('$baseUrl/process/ocr-simplify');

    try {
      final request = http.MultipartRequest('POST', uri);

      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          imageFile.path,
        ),
      );

      final response = await request.send();

      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = json.decode(responseBody);
        return data['simplified_text'] ?? 'No text returned';
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
