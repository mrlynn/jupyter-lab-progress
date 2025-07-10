# Lab Utils

A comprehensive Python library for creating interactive lab exercises in Jupyter notebooks. Provides progress tracking, validation methods, and rich display utilities to enhance the learning experience.

## Features

- 📊 **Progress Tracking**: Visual progress bars, step completion tracking, persistence support
- ✅ **Validation Framework**: Comprehensive validation methods for variables, functions, outputs, and more
- 🎨 **Rich Display Utilities**: Info boxes, warnings, errors, code blocks, tables, tabs, and more
- 💾 **Persistence**: Save and restore progress across sessions
- 🔗 **Integration**: Validators can automatically update progress trackers

## Installation

```bash
pip install -e lab_utils/
```

## Quick Start

```python
from lab_utils import LabProgress, LabValidator, show_info, show_success

# Create a progress tracker
progress = LabProgress(["Load Data", "Process Data", "Analyze Results"], 
                      lab_name="Data Science Lab")

# Create a validator linked to progress
validator = LabValidator(progress_tracker=progress)

# Show instructions
show_info("Let's start by loading the dataset", title="Step 1")

# Validate and mark progress
data_loaded = True  # Your actual condition
validator.validate_and_mark_complete("Load Data", data_loaded)

# Display success message
show_success("Great job! Data loaded successfully")
```

## Components

### 1. Progress Tracking (LabProgress)

Track student progress through lab exercises with visual feedback.

```python
from lab_utils import LabProgress

# Basic usage
progress = LabProgress(["Step 1", "Step 2", "Step 3"])
progress.mark_done("Step 1")

# Advanced features
progress = LabProgress(
    steps=["Load Data", "Clean Data", "Analyze"],
    lab_name="Data Analysis Lab",
    persist=True  # Save progress to file
)

# Mark with score and notes
progress.mark_done("Load Data", score=95, notes="Excellent work!")

# Partial progress
progress.mark_partial("Clean Data", 0.75)  # 75% complete

# Get statistics
print(f"Completion: {progress.get_completion_rate()}%")
print(f"Average Score: {progress.get_average_score()}")

# Export report
report = progress.export_report()
```

### 2. Validation (LabValidator)

Comprehensive validation methods for checking student work.

```python
from lab_utils import LabValidator

validator = LabValidator()

# Variable validation
validator.validate_variable_exists("my_var", globals(), expected_type=list)

# Function validation
validator.validate_function_exists("process_data", globals(), 
                                 expected_params=["data", "method"])

# Output validation
result = 42
validator.validate_output(result, expected=42)

# DataFrame validation
validator.validate_dataframe(df, 
                           expected_shape=(100, 5),
                           expected_columns=["id", "name", "value"])

# Custom validation
validator.validate_custom(
    condition=(len(data) > 0),
    success_msg="Data loaded successfully",
    failure_msg="No data found"
)

# Linked with progress tracker
validator = LabValidator(progress_tracker=progress)
validator.validate_and_mark_complete("Step 1", condition=True)
```

### 3. Display Utilities

Rich display functions for better communication with students.

```python
from lab_utils import *

# Basic messages
show_info("This is informational text")
show_warning("Be careful with this operation", title="Warning")
show_error("Something went wrong", title="Error")
show_success("Well done!", title="Success")

# Code display
show_code("""
def hello_world():
    print("Hello, World!")
""", language="python", title="Example Code")

# Hints (collapsible)
show_hint("Try using pandas read_csv function", title="Need help?")

# Progress bars
show_progress_bar(3, 10, label="Overall Progress")

# JSON data
data = {"name": "Lab 1", "score": 95}
show_json(data, title="Results", collapsed=True)

# Tables
show_table(
    headers=["Name", "Score", "Status"],
    rows=[
        ["Alice", "95", "Pass"],
        ["Bob", "87", "Pass"],
        ["Charlie", "72", "Pass"]
    ],
    title="Lab Results"
)

# Checklists
show_checklist({
    "Load data": True,
    "Clean data": True,
    "Analyze data": False,
    "Create visualization": False
}, title="Progress Checklist")

# Tabs
show_tabs({
    "Instructions": "Complete the following steps...",
    "Hints": "Remember to check your data types",
    "Solution": "Here's one way to solve it..."
})
```

## Advanced Usage

### Creating Custom Validators

```python
# Create step-specific validators
validator = LabValidator(progress_tracker=progress)
validate_step1 = validator.create_step_validator("Step 1")

# Use the custom validator
result = compute_something()
validate_step1(result == expected_value, 
               success_msg="Step 1 completed perfectly!",
               failure_msg="Check your calculation")
```

### Persistence

```python
# Progress is automatically saved
progress = LabProgress(steps, persist=True, persist_file="my_lab_progress.json")

# On next run, previous progress is loaded automatically
```

### Integration Example

```python
from lab_utils import LabProgress, LabValidator, show_info, show_hint

# Setup
steps = ["Import Libraries", "Load Data", "Preprocess", "Train Model", "Evaluate"]
progress = LabProgress(steps, lab_name="ML Workshop", persist=True)
validator = LabValidator(progress_tracker=progress)

# Step 1: Import Libraries
show_info("First, import the required libraries", title="Step 1: Imports")
show_code("import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split")

# Validation
try:
    import pandas as pd
    import numpy as np
    validator.validate_and_mark_complete("Import Libraries", True)
except ImportError:
    show_error("Missing required libraries. Run: pip install pandas numpy scikit-learn")
    show_hint("Make sure you're in the correct environment")
```

## Best Practices

1. **Clear Instructions**: Use `show_info()` at the start of each step
2. **Helpful Hints**: Provide hints without giving away the solution
3. **Progressive Validation**: Validate early and often
4. **Visual Feedback**: Use colors and icons to guide students
5. **Persistence**: Enable persistence for long labs
6. **Scores and Notes**: Track performance for assessment

## License

MIT License - see LICENSE file for details