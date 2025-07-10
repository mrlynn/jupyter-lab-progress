# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python utility library designed for MongoDB Developer Days workshops and labs. It provides visual progress tracking, validation, and display utilities for Jupyter notebooks.

## Common Development Commands

### Installation
```bash
# Install package in development mode
cd lab_utils && pip install -e .

# Build the package
cd lab_utils && python -m build
```

### Testing
Currently no test framework is configured. The `tests/` directory exists but is empty.

## Architecture

The library is organized into three core modules within `lab_utils/lab_utils/`:

### `progress.py` - Lab Progress Tracking
- `LabProgress` class tracks multi-step lab completion
- Visual progress display using HTML in Jupyter cells
- Shows completion status with colored icons (✅/⏳)

### `validator.py` - Data Validation
- `LabValidator` class for checking data integrity
- Methods:
  - `check_embedding_shape()` - Validates embedding dimensions
  - `assert_in_dataframe()` - Checks if values exist in dataframe columns

### `display.py` - Visual Messaging
- `show_info()` - Blue information boxes
- `show_warning()` - Yellow warning boxes with ⚠️ icon
- Both render as styled HTML divs in Jupyter

## Import Pattern
Since `__init__.py` is empty, imports must be explicit:
```python
from lab_utils.progress import LabProgress
from lab_utils.validator import LabValidator
from lab_utils.display import show_info, show_warning
```