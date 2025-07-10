# Upload Guide for jupyter-lab-utils

## Troubleshooting the 403 Forbidden Error

### 1. Authentication Setup

Create or update your `~/.pypirc` file:

```bash
# Create the file
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
EOF
```

### 2. Alternative Upload Methods

#### Method A: Use API tokens directly

```bash
# For TestPyPI
python -m twine upload --repository testpypi dist/* --username __token__ --password pypi-YOUR_TESTPYPI_TOKEN

# For PyPI
python -m twine upload dist/* --username __token__ --password pypi-YOUR_PYPI_TOKEN
```

#### Method B: Use keyring (recommended)

```bash
# Install keyring
pip install keyring

# Set up keyring for TestPyPI
keyring set https://test.pypi.org/legacy/ __token__

# Set up keyring for PyPI
keyring set https://upload.pypi.org/legacy/ __token__
```

### 3. Check Package Name Availability

The package name might already exist. Try these alternatives:

1. **Current unique name**: `jupyter-lab-utils-mrlynn`
2. **Alternative names**:
   - `jupyter-lab-validation-utils`
   - `jupyter-exercise-utils`
   - `notebook-lab-utils`
   - `michael-jupyter-lab-utils`

### 4. Rebuild and Upload

After changing the package name:

```bash
# Clean previous build
rm -rf dist/ build/ *.egg-info/

# Rebuild
python -m build

# Check the build
python -m twine check dist/*

# Upload to TestPyPI with unique name
python -m twine upload --repository testpypi dist/*
```

### 5. Verify Upload

After successful upload, test installation:

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ jupyter-lab-utils-mrlynn

# Test it works
python -c "import jupyter_lab_utils; print('Success!')"
```

### 6. Final PyPI Upload

Once TestPyPI works:

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

## Common Issues and Solutions

### Issue: Package name already exists
**Solution**: Use a unique name like `jupyter-lab-utils-mrlynn` (already done above)

### Issue: Authentication failed
**Solution**: 
- Check your API token is valid
- Ensure token has correct permissions
- Try the direct token method above

### Issue: Network/timeout errors
**Solution**:
- Use `--verbose` flag for more details
- Try uploading again
- Check internet connection

### Issue: Package too large
**Solution**: 
- Check dist/ folder size
- Remove unnecessary files
- Use MANIFEST.in to exclude files

## Success Workflow

1. ✅ Fixed package name to `jupyter-lab-utils-mrlynn`
2. ✅ Set up authentication
3. ✅ Rebuild package
4. ✅ Upload to TestPyPI
5. ✅ Test installation
6. ✅ Upload to PyPI

## Quick Commands

```bash
# Complete upload sequence
rm -rf dist/ build/ *.egg-info/
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
```

The package is now ready with a unique name that should upload successfully!