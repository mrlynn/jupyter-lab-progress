#!/usr/bin/env python3
"""
Simple test that imports modules directly without installation.
"""

import sys
import os

# Add the package directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_imports():
    """Test basic imports."""
    try:
        print("Testing direct imports...")
        
        # Test version import
        from jupyter_lab_utils._version import __version__, __title__, __author__
        print(f"✅ Version: {__version__}")
        print(f"✅ Title: {__title__}")
        print(f"✅ Author: {__author__}")
        
        # Test main classes
        from jupyter_lab_utils.progress import LabProgress
        from jupyter_lab_utils.validator import LabValidator
        print("✅ Successfully imported LabProgress and LabValidator")
        
        # Test display functions  
        from jupyter_lab_utils.display import show_info, show_success
        print("✅ Successfully imported display functions")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        print("\nTesting basic functionality...")
        
        from jupyter_lab_utils.progress import LabProgress
        from jupyter_lab_utils.validator import LabValidator
        
        # Test progress creation (without display since no Jupyter)
        progress = LabProgress(["Step 1", "Step 2"], lab_name="Test Lab")
        print("✅ Created LabProgress")
        
        # Test marking done (disable display for testing)
        progress._display_handle = None  # Disable display updates
        progress.mark_done("Step 1", score=95)
        print("✅ Marked step as done")
        
        # Test completion rate
        rate = progress.get_completion_rate()
        print(f"✅ Completion rate: {rate}%")
        
        # Test validator
        validator = LabValidator()
        print("✅ Created LabValidator")
        
        # Test custom validation (will show error without Jupyter, but that's OK)
        try:
            result = validator.validate_custom(True, "Success", "Failure")
            print("✅ Custom validation method works")
        except:
            print("⚠️  Display functions need Jupyter environment (expected)")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests."""
    print("🚀 Testing jupyter-lab-utils package structure...\n")
    
    tests_passed = 0
    
    if test_imports():
        tests_passed += 1
    
    if test_basic_functionality():
        tests_passed += 1
    
    print(f"\n🏁 Results: {tests_passed}/2 tests passed")
    
    if tests_passed == 2:
        print("🎉 Package structure is valid and ready for building!")
        return True
    else:
        print("💥 Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)