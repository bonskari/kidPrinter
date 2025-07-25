#!/usr/bin/env python3
"""
Development setup and testing script for Child's Automatic Printer
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n📦 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    """Main setup script."""
    print("🚀 Child's Automatic Printer - Development Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Install dependencies
    run_command("pip install -r requirements.txt", "Installing Python dependencies")
    
    # Install development dependencies
    run_command("pip install black flake8 pytest pytest-cov", "Installing development tools")
    
    # Create necessary directories
    print("\n📁 Creating project directories")
    directories = [
        "assets/audio",
        "assets/images", 
        "config",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Run tests
    if Path("tests").exists():
        run_command("python -m pytest tests/ -v", "Running unit tests")
    
    # Check code formatting
    run_command("python -m black --check src/", "Checking code formatting")
    
    # Run linting
    run_command("python -m flake8 src/", "Running code linting")
    
    print("\n🎉 Setup complete!")
    print("\n🔧 Development Commands:")
    print("  Format code: python -m black src/")
    print("  Run tests: python -m pytest tests/")
    print("  Start app: python src/main.py")
    print("\n📝 Next steps:")
    print("  1. Install system dependencies for Raspberry Pi:")
    print("     - sudo apt install portaudio19-dev python3-pyaudio")
    print("     - sudo apt install espeak espeak-data")
    print("  2. Configure your printer in CUPS")
    print("  3. Add Finnish audio files to assets/audio/")
    print("  4. Test voice recognition with: python src/main.py")


if __name__ == "__main__":
    main()
