# Debug Cell for mark_partial Issue

Copy and paste this cell into your Jupyter notebook:

```python
# Cell 1: Diagnose the issue
import sys
import inspect

# Check where Python is looking for modules
print("Python is looking for modules in:")
for i, path in enumerate(sys.path[:5]):
    print(f"{i}: {path}")

# Check which version of the module is loaded
try:
    import jupyter_lab_progress
    print(f"\nCurrently loaded module from: {jupyter_lab_progress.__file__}")
    
    from jupyter_lab_progress.progress import LabProgress
    print("\nChecking mark_partial signature:")
    sig = inspect.signature(LabProgress.mark_partial)
    print(f"Signature: {sig}")
    
    # Get the parameters
    params = list(sig.parameters.keys())
    if 'checkpoint_name' in params:
        print("✅ checkpoint_name parameter is present in the signature")
    else:
        print("❌ checkpoint_name parameter is NOT in the signature")
        print(f"Available parameters: {params}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
```

```python
# Cell 2: Force reload and test
# This cell forces Python to reload the module from disk
import importlib
import sys

# Remove the module from cache if it exists
if 'jupyter_lab_progress' in sys.modules:
    del sys.modules['jupyter_lab_progress']
if 'jupyter_lab_progress.progress' in sys.modules:
    del sys.modules['jupyter_lab_progress.progress']

# Reimport
from jupyter_lab_progress.progress import LabProgress

# Test the method
print("Testing mark_partial with checkpoint_name...")
progress = LabProgress(["Step 1", "Step 2"], "Test Lab")
try:
    progress.mark_partial("Step 1", 0.5, checkpoint_name="Halfway checkpoint")
    print("✅ Success! The checkpoint_name parameter works.")
    print("\nCheckpoints stored:", progress.steps["Step 1"]["checkpoints"])
except TypeError as e:
    print(f"❌ Error: {e}")
    print("\nThis means the installed version doesn't have the checkpoint_name parameter.")
    print("To fix:")
    print("1. Exit Jupyter")
    print("2. In terminal: cd /Users/michael.lynn/code/mongodb/developer-days/jupyter-utils/jupyter-lab-progress")
    print("3. Run: pip install -e .")
    print("4. Restart Jupyter and try again")
```

```python
# Cell 3: Alternative - Use the source directly (temporary fix)
# If the above doesn't work, you can load the module directly from source
import sys
sys.path.insert(0, '/Users/michael.lynn/code/mongodb/developer-days/jupyter-utils/jupyter-lab-progress')

# Force reload
if 'jupyter_lab_progress' in sys.modules:
    del sys.modules['jupyter_lab_progress']
if 'jupyter_lab_progress.progress' in sys.modules:
    del sys.modules['jupyter_lab_progress.progress']

from jupyter_lab_progress.progress import LabProgress

# Now test
progress = LabProgress(["Step 1", "Step 2"], "Test Lab")
progress.mark_partial("Step 1", 0.5, checkpoint_name="Direct load test")
print("✅ Successfully loaded from source!")
print("Checkpoints:", progress.steps["Step 1"]["checkpoints"])
```