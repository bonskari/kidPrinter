#!/usr/bin/env python3
"""
Check if required dependencies are installed
"""

def check_dependency(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        pkg = package_name or module_name
        print(f"✗ {module_name} is NOT installed. Install with: pip install {pkg}")
        return False

def main():
    print("Checking dependencies for microphone test...")
    print("=" * 50)
    
    dependencies = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "pyaudio"),
    ]
    
    all_installed = True
    for module, package in dependencies:
        if not check_dependency(module, package):
            all_installed = False
    
    print()
    if all_installed:
        print("✓ All dependencies are installed!")
        print("You can now run: python3 test_microphone.py")
    else:
        print("✗ Some dependencies are missing.")
        print("Install them with: pip install -r requirements.txt")
        print("Or individually:")
        print("  pip install SpeechRecognition pyaudio")

if __name__ == "__main__":
    main()