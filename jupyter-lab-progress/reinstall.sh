#!/bin/bash

# Script to reinstall jupyter-lab-progress in development mode

echo "🔧 Reinstalling jupyter-lab-progress in development mode..."

# Uninstall any existing version
echo "📦 Uninstalling existing package..."
pip uninstall -y jupyter-lab-progress

# Install in development mode
echo "📦 Installing in development mode..."
pip install -e .

echo "✅ Done! Please restart your Jupyter kernel to use the updated version."
echo ""
echo "In Jupyter: Kernel → Restart"