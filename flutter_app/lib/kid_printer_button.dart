import 'package:flutter/material.dart';

class KidPrinterButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final IconData icon;
  final bool loading;
  final bool disabled;

  const KidPrinterButton({
    super.key,
    required this.onPressed,
    required this.icon,
    this.loading = false,
    this.disabled = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(6),
      child: SizedBox(
        width: 56,
        height: 56,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            shape: const CircleBorder(),
            padding: EdgeInsets.zero,
          ),
          onPressed: (disabled || loading) ? null : onPressed,
          child: loading
              ? const SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : Icon(icon, size: 32),
        ),
      ),
    );
  }
}
