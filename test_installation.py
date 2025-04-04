import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is 3.7 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ FFmpeg is installed")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg is not installed")
        return False

def check_mediamtx():
    """Check if MediaMTX is installed."""
    try:
        subprocess.run(['mediamtx', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ MediaMTX is installed")
        return True
    except FileNotFoundError:
        print("❌ MediaMTX is not installed")
        return False

def check_python_dependencies():
    """Check if all Python dependencies are installed."""
    try:
        import click
        import cv2
        import yaml
        import requests
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        return False

def check_directory_structure():
    """Check if the required directories exist."""
    required_dirs = ['src', 'videos']
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    print("✅ Directory structure is correct")
    return True

def main():
    """Run all installation checks."""
    print("Running installation checks...\n")
    
    checks = [
        check_python_version(),
        check_ffmpeg(),
        check_mediamtx(),
        check_python_dependencies(),
        check_directory_structure()
    ]
    
    if all(checks):
        print("\n✅ All checks passed! Installation is complete.")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")

if __name__ == '__main__':
    main() 