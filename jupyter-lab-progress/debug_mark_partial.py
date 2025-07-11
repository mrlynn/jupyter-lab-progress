#!/usr/bin/env python3
"""
Debug script to check mark_partial method signature
"""

# Check current module
try:
    from jupyter_lab_progress.progress import LabProgress
    import inspect
    
    print("Current module signature:")
    print(inspect.signature(LabProgress.mark_partial))
    print("\nParameters:", inspect.getfullargspec(LabProgress.mark_partial).args)
    
    # Test it
    progress = LabProgress(["Step 1"], "Test")
    progress.mark_partial("Step 1", 0.5, checkpoint_name="test checkpoint")
    print("\n✅ checkpoint_name parameter works correctly!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTo fix this issue:")
    print("1. Make sure you're in the project directory")
    print("2. Run: pip install -e .")
    print("3. Restart your Jupyter kernel")
    print("4. Import the module again")