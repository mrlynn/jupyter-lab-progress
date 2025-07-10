# Deployment Guide for jupyter-lab-utils

This guide walks through testing, building, and publishing the jupyter-lab-utils package.

## Prerequisites

- Python 3.8 or higher
- pip and virtual environment tools

## 1. Local Development Setup

### Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
# Install the package in development mode with dependencies
pip install -e .

# Install development tools
pip install build twine pytest black flake8 mypy
```

## 2. Testing the Package

### Run Basic Tests

```bash
# Test the installation
python scripts/test_install.py

# Run unit tests
pytest tests/

# Test import functionality
python -c "from jupyter_lab_utils import LabProgress, LabValidator; print('✅ Package works!')"
```

### Validate Package Structure

```bash
# Check that all files are in place
find . -name "*.py" | head -10
ls -la jupyter_lab_utils/
```

## 3. Building the Package

### Clean Previous Builds

```bash
# Remove old builds
rm -rf build/ dist/ *.egg-info/
```

### Build Distribution

```bash
# Build source and wheel distributions
python -m build

# Verify the build
python -m twine check dist/*
```

Expected output:
```
dist/
├── jupyter_lab_utils-1.0.0-py3-none-any.whl
└── jupyter-lab-utils-1.0.0.tar.gz
```

## 4. Local Testing of Built Package

### Test in Clean Environment

```bash
# Create a new virtual environment for testing
python3 -m venv test_env
source test_env/bin/activate

# Install from the built wheel
pip install dist/jupyter_lab_utils-1.0.0-py3-none-any.whl

# Test it works
python -c "from jupyter_lab_utils import LabProgress; print('✅ Installation successful!')"

# Deactivate test environment
deactivate
```

## 5. Publishing to PyPI

### Test on TestPyPI First

```bash
# Upload to TestPyPI (recommended first step)
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ jupyter-lab-utils
```

### Publish to Production PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

You'll need PyPI credentials. Set them up with:

```bash
# Create ~/.pypirc with your credentials
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = <your-api-token>
```

## 6. Verification After Publishing

### Install from PyPI

```bash
# Create fresh environment
python3 -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install jupyter-lab-utils

# Test functionality
python -c "
from jupyter_lab_utils import LabProgress, LabValidator, show_info
print('✅ PyPI installation successful!')
print(f'Version: {LabProgress.__module__.split('.')[0]}')
"
```

### Test in Jupyter

```bash
# Install jupyter
pip install jupyter pandas numpy

# Launch Jupyter and test
jupyter notebook examples/getting_started.ipynb
```

## 7. GitHub Release

### Create GitHub Release

1. Go to https://github.com/mrlynn/jupyter-lab-utils/releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `jupyter-lab-utils v1.0.0`
5. Description: Copy from CHANGELOG.md
6. Attach the distribution files from `dist/`

## 8. Post-Publication

### Update Documentation

- Update README badges with PyPI version
- Update installation instructions
- Create documentation site (optional)

### Monitor

- Watch for GitHub issues
- Monitor PyPI download statistics
- Respond to user feedback

## Common Issues and Solutions

### Build Errors

```bash
# If build fails, check:
python -m pip install --upgrade build setuptools wheel

# Validate pyproject.toml
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

### Import Errors

```bash
# Check package structure
python -c "import sys; sys.path.insert(0, '.'); import jupyter_lab_utils; print('OK')"
```

### Permission Errors on PyPI

- Ensure you have maintainer access to the package name
- Check API token permissions
- Verify package name isn't already taken

## Quick Reference Commands

```bash
# Full build and test sequence
rm -rf build/ dist/ *.egg-info/
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*  # Test first
python -m twine upload dist/*  # Production release
```

## Success Checklist

- [ ] Package builds without errors
- [ ] All tests pass
- [ ] Twine check passes
- [ ] TestPyPI upload works
- [ ] Installation from TestPyPI works
- [ ] Production PyPI upload successful
- [ ] GitHub release created
- [ ] Documentation updated

The package is now ready for the world! 🚀