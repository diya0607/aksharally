import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'reader_screen.dart';
import 'library_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.background,

      appBar: AppBar(
        backgroundColor: AppTheme.primaryPink,
        elevation: 0,
        title: const Text("AksharAlly"),
        centerTitle: true,
      ),

      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 420),
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: _getScreenForIndex(context),
            ),
          ),
        ),
      ),

      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        selectedItemColor: AppTheme.primaryGreen,
        onTap: (index) {
          setState(() {
            currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            label: "Home",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.book_outlined),
            label: "Library",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings_outlined),
            label: "Settings",
          ),
        ],
      ),
    );
  }

  /// SCREEN SWITCHING LOGIC
  Widget _getScreenForIndex(BuildContext context) {
    switch (currentIndex) {
      case 0:
        return _buildHomeContent(context);
      case 1:
        return const LibraryScreen();
      case 2:
        return const SettingsScreen();
      default:
        return _buildHomeContent(context);
    }
  }

  /// HOME DASHBOARD UI
  Widget _buildHomeContent(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 10),

        Text(
          "Welcome Back!",
          style: AppTheme.headingStyle,
        ),

        const SizedBox(height: 30),

        _actionCard(
          context,
          icon: Icons.document_scanner_outlined,
          title: "Scan the Image",
          subtitle: "Capture text using camera",
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const ReaderScreen(),
              ),
            );
          },
        ),

        const SizedBox(height: 15),

        _actionCard(
          context,
          icon: Icons.edit_outlined,
          title: "Enter Text",
          subtitle: "Type text manually",
          onTap: () {},
        ),

        const SizedBox(height: 15),

        _actionCard(
          context,
          icon: Icons.upload_file_outlined,
          title: "Upload File",
          subtitle: "Import image or document",
          onTap: () {},
        ),

        const SizedBox(height: 15),

        _actionCard(
          context,
          icon: Icons.menu_book_outlined,
          title: "Continue Reading",
          subtitle: "Resume previous session",
          onTap: () {},
        ),
      ],
    );
  }

  Widget _actionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return InkWell(
      borderRadius: BorderRadius.circular(20),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(18),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 8,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(icon, size: 30, color: AppTheme.primaryGreen),
            const SizedBox(width: 15),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  subtitle,
                  style: const TextStyle(color: Colors.grey),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}