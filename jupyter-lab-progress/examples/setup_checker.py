"""
Setup checker utility for jupyter-lab-progress examples.
Run this cell at the start of any example notebook to ensure all dependencies are available.
"""

import sys
import subprocess
import importlib.util
from IPython.display import display, HTML


def check_and_install_package(package_name, import_name=None, pip_name=None):
    """
    Check if a package is installed, and install it if not.
    
    Args:
        package_name: Name to display to user
        import_name: Name used for importing (defaults to package_name)
        pip_name: Name used for pip install (defaults to package_name)
    """
    if import_name is None:
        import_name = package_name
    if pip_name is None:
        pip_name = package_name.replace('_', '-')
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} is available")
        return True
    except ImportError:
        print(f"❌ {package_name} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False


def setup_environment():
    """Check and install all required packages for examples."""
    
    display(HTML("""
    <div style="background: #f0f7ff; border: 1px solid #0066cc; border-radius: 5px; padding: 15px; margin: 10px 0;">
        <h3 style="color: #0066cc; margin: 0 0 10px 0;">🔧 Environment Setup</h3>
        <p>Checking and installing required packages...</p>
    </div>
    """))
    
    # Core packages
    packages = [
        ("jupyter-lab-progress", "jupyter_lab_progress", "jupyter-lab-progress"),
        ("pandas", "pandas", "pandas"),
        ("numpy", "numpy", "numpy"),
        ("matplotlib", "matplotlib", "matplotlib"),
        ("seaborn", "seaborn", "seaborn"),
        ("plotly", "plotly", "plotly"),
        ("pymongo", "pymongo", "pymongo"),
        ("dnspython", "dns", "dnspython"),
    ]
    
    failed_packages = []
    
    for package_name, import_name, pip_name in packages:
        if not check_and_install_package(package_name, import_name, pip_name):
            failed_packages.append(package_name)
    
    if failed_packages:
        display(HTML(f"""
        <div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 5px; padding: 15px; margin: 10px 0;">
            <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ Installation Issues</h4>
            <p>Failed to install: {', '.join(failed_packages)}</p>
            <p>Please install manually:</p>
            <pre>pip install {' '.join(failed_packages)}</pre>
        </div>
        """))
    else:
        display(HTML("""
        <div style="background: #d4edda; border: 1px solid #28a745; border-radius: 5px; padding: 15px; margin: 10px 0;">
            <h4 style="color: #155724; margin: 0 0 10px 0;">✅ Environment Ready</h4>
            <p>All required packages are installed and ready to use!</p>
        </div>
        """))


def create_setup_cell():
    """Return the code that should be placed in the first cell of notebooks."""
    return '''
# Run this cell to ensure all required packages are installed
import sys
import subprocess

# Install jupyter-lab-progress if not available
try:
    import jupyter_lab_progress
except ImportError:
    print("Installing jupyter-lab-progress...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyter-lab-progress"])
    print("✅ jupyter-lab-progress installed!")

# Import everything we need
from jupyter_lab_progress import *
import pandas as pd
import numpy as np

# Try to import optional packages
try:
    import matplotlib.pyplot as plt
    print("✅ matplotlib available")
except ImportError:
    print("⚠️ matplotlib not available - some examples may not work")

try:
    import seaborn as sns
    print("✅ seaborn available")
except ImportError:
    print("⚠️ seaborn not available - some examples may not work")

try:
    import plotly.graph_objects as go
    print("✅ plotly available")
except ImportError:
    print("⚠️ plotly not available - some examples may not work")

print("\\n🎉 Setup complete! You can now run the examples.")
'''


if __name__ == "__main__":
    setup_environment()