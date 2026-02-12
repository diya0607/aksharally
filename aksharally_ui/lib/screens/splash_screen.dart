import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../widgets/primary_button.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.primaryPink,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Spacer(),
            const Icon(
              Icons.menu_book_rounded,
              size: 120,
              color: Colors.white,
            ),
            const SizedBox(height: 20),
            const Text(
              "AksharAlly",
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const Spacer(),
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: PrimaryButton(
                text: "Get Started",
                onPressed: () {
  Navigator.pushNamed(context, '/login');
},
              ),
            ),
          ],
        ),
      ),
    );
  }
}