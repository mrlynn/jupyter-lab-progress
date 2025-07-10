#!/bin/bash
"""
Build script for jupyter-lab-utils package.
"""

set -e

echo "🔧 Building jupyter-lab-utils package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "🏗️ Building package..."
python -m build

# Verify the build
echo "✅ Verifying build..."
python -m twine check dist/*

echo "🎉 Build completed successfully!"
echo "📄 Files created:"
ls -la dist/

echo ""
echo "To install locally:"
echo "  pip install dist/jupyter_lab_utils-*.whl"
echo ""
echo "To publish to PyPI:"
echo "  python -m twine upload dist/*"