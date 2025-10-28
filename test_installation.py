"""
Test script to verify Basketball Shot Analyzer installation and dependencies.
Run this before using the main application to ensure everything is set up correctly.
"""

import sys

def test_imports():
    """Test if all required packages are installed."""
    print("Testing package imports...")
    
    packages = {
        'gradio': 'Gradio',
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'numpy': 'NumPy',
        'PIL': 'Pillow'
    }
    
    failed = []
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - FAILED")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Installation incomplete. Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed correctly!")
        return True


def test_mediapipe():
    """Test MediaPipe functionality."""
    print("\nTesting MediaPipe Pose Detection...")
    
    try:
        import mediapipe as mp
        import numpy as np
        
        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=True,
            min_detection_confidence=0.5
        )
        
        # Create a dummy image (black 640x480)
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Try to process it
        results = pose.process(dummy_image)
        pose.close()
        
        print("✅ MediaPipe Pose - Working correctly")
        return True
    
    except Exception as e:
        print(f"❌ MediaPipe test failed: {str(e)}")
        return False


def test_opencv():
    """Test OpenCV video processing."""
    print("\nTesting OpenCV...")
    
    try:
        import cv2
        import numpy as np
        
        # Create a test video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        print("✅ OpenCV - Working correctly")
        return True
    
    except Exception as e:
        print(f"❌ OpenCV test failed: {str(e)}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Incompatible")
        print("Required: Python 3.8 or higher")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Basketball Shot Analyzer - Installation Test")
    print("=" * 60)
    print()
    
    tests = [
        check_python_version(),
        test_imports(),
        test_mediapipe(),
        test_opencv()
    ]
    
    print()
    print("=" * 60)
    
    if all(tests):
        print("✅ All tests passed! You're ready to use the application.")
        print()
        print("To start the application, run:")
        print("    python app.py")
        print()
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()
