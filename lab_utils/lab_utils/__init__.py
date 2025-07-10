"""
Lab Utils - A comprehensive Jupyter notebook lab exercise validation package.

Provides progress tracking, validation methods, and display utilities for 
creating interactive lab exercises in Jupyter notebooks.
"""

from .progress import LabProgress
from .validator import LabValidator
from .display import (
    show_info,
    show_warning,
    show_error,
    show_success,
    show_code,
    show_hint,
    show_progress_bar,
    show_json,
    show_table,
    show_checklist,
    show_tabs,
    clear
)

__version__ = "0.2.0"
__author__ = "Your Name"

__all__ = [
    # Progress tracking
    "LabProgress",
    
    # Validation
    "LabValidator",
    
    # Display functions
    "show_info",
    "show_warning",
    "show_error",
    "show_success",
    "show_code",
    "show_hint",
    "show_progress_bar",
    "show_json",
    "show_table",
    "show_checklist",
    "show_tabs",
    "clear"
]