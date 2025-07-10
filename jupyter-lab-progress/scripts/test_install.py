#!/usr/bin/env python3
"""
Test script to verify jupyter-lab-utils installation and basic functionality.
"""

def test_import():
    """Test basic import functionality."""
    print("🔍 Testing imports...")
    
    try:
        import jupyter_lab_utils
        print(f"✅ Successfully imported jupyter_lab_utils v{jupyter_lab_utils.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import jupyter_lab_utils: {e}")
        return False
    
    try:
        from jupyter_lab_utils import LabProgress, LabValidator
        print("✅ Successfully imported LabProgress and LabValidator")
    except ImportError as e:
        print(f"❌ Failed to import main classes: {e}")
        return False
    
    try:
        from jupyter_lab_utils import show_info, show_success, show_warning, show_error
        print("✅ Successfully imported display functions")
    except ImportError as e:
        print(f"❌ Failed to import display functions: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without Jupyter display."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from jupyter_lab_utils import LabProgress, LabValidator
        
        # Test progress creation
        progress = LabProgress(["Step 1", "Step 2", "Step 3"], lab_name="Test Lab")
        print("✅ Created LabProgress instance")
        
        # Test marking done
        progress.mark_done("Step 1", score=95)
        print("✅ Marked step as done")
        
        # Test completion rate
        rate = progress.get_completion_rate()
        assert abs(rate - 33.33) < 0.1, f"Expected ~33.33%, got {rate}%"
        print(f"✅ Completion rate calculation: {rate:.1f}%")
        
        # Test validator creation
        validator = LabValidator(progress_tracker=progress)
        print("✅ Created LabValidator instance")
        
        # Test custom validation
        result = validator.validate_custom(
            condition=True,
            success_msg="Test validation passed",
            failure_msg="Test validation failed"
        )
        assert result is True, "Custom validation should return True"
        print("✅ Custom validation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_version_info():
    """Test version information availability."""
    print("\n📋 Testing version information...")
    
    try:
        import jupyter_lab_utils
        
        attrs = ['__version__', '__title__', '__description__', '__author__']
        for attr in attrs:
            value = getattr(jupyter_lab_utils, attr, None)
            if value:
                print(f"✅ {attr}: {value}")
            else:
                print(f"⚠️  {attr}: Not available")
        
        return True
        
    except Exception as e:
        print(f"❌ Version info test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting jupyter-lab-utils installation test...\n")
    
    tests = [
        ("Import Test", test_import),
        ("Basic Functionality Test", test_basic_functionality),
        ("Version Info Test", test_version_info),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! jupyter-lab-utils is ready to use.")
        return True
    else:
        print("💥 Some tests failed. Please check the installation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)