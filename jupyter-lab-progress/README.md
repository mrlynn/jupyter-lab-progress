# Jupyter Lab Progress

[![PyPI version](https://badge.fury.io/py/jupyter-lab-progress.svg)](https://badge.fury.io/py/jupyter-lab-progress)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python library for creating interactive lab exercises in Jupyter notebooks. Designed for educators, workshop leaders, and content creators who want to build engaging, validated learning experiences.

## 🚀 Features

### Core Features
- **📊 Progress Tracking**: Visual progress bars, step completion tracking, persistence support
- **✅ Comprehensive Validation**: Variable, function, output, DataFrame, and custom validation methods
- **🎨 Rich Display Utilities**: Info boxes, warnings, code blocks, tables, tabs, hints, and more
- **💾 Persistence**: Save and restore progress across sessions with smart checkpoint resume
- **🔗 Seamless Integration**: Validators automatically update progress trackers
- **🎓 Education-Focused**: Built specifically for teaching and learning scenarios

### Advanced Features
- **🧠 Session Resume**: Smart checkpoints with automatic session restoration
- **💡 Inline Hints**: Collapsible hints and contextual tips for each step
- **🎯 Auto-Graded Checkpoints**: Weighted scoring system with comprehensive grading reports
- **📈 Progress Analytics**: CSV/JSON export with detailed metrics and performance tracking
- **⏱️ Time Tracking**: Automatic time spent per step monitoring
- **📊 Enhanced DataFrame Validation**: Visual previews with histograms and data analysis
- **🗄️ MongoDB Status Checker**: Live cluster status validation and diagnostic reports
- **🖥️ Integrated Terminal**: Execute shell commands with styled output and validation
- **🎭 Rich Visuals**: Enhanced HTML displays with professional styling

## 📦 Installation

```bash
pip install jupyter-lab-progress
```

For development installation:

```bash
git clone https://github.com/mrlynn/jupyter-lab-progress.git
cd jupyter-lab-progress/jupyter-lab-progress
pip install -e ".[dev]"
```

## 🏃‍♂️ Quick Start

```python
from jupyter_lab_progress import LabProgress, LabValidator, show_info, show_success

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

## 📚 Core Components

### 1. Progress Tracking (`LabProgress`)

Track student progress through lab exercises with visual feedback:

```python
from jupyter_lab_progress import LabProgress

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
```

### 2. Validation Framework (`LabValidator`)

Comprehensive validation methods for checking student work:

```python
from jupyter_lab_progress import LabValidator

validator = LabValidator()

# Variable validation
validator.validate_variable_exists("my_var", globals(), expected_type=list)

# Function validation
validator.validate_function_exists("process_data", globals(), 
                                 expected_params=["data", "method"])

# DataFrame validation
validator.validate_dataframe(df, 
                           expected_shape=(100, 5),
                           expected_columns=["id", "name", "value"])

# Custom validation with auto-progress updates
validator = LabValidator(progress_tracker=progress)
validator.validate_and_mark_complete("Step 1", condition=True)
```

### 3. Display Utilities

Rich display functions for better communication:

```python
from jupyter_lab_progress import *

# Messages
show_info("This is informational")
show_success("Well done!")
show_warning("Be careful")
show_error("Something went wrong")

# Code display
show_code("print('Hello World')", language="python", title="Example")

# Interactive elements
show_hint("Try using pandas read_csv function")
show_progress_bar(3, 10, label="Overall Progress")
show_checklist({"Task 1": True, "Task 2": False})

# Data display 
show_json({"key": "value"}, title="Results")
show_table(headers=["Name", "Score"], rows=[["Alice", "95"]])
```

## 🔧 Advanced Usage

### Session Resume & Smart Checkpoints

```python
# Resume from previous session
progress = LabProgress.resume("My Lab")  # Auto-loads saved progress

# Or resume with custom file
progress = LabProgress.resume("My Lab", persist_file="custom_progress.json")

# Create checkpoints within steps
progress.create_checkpoint("Data Processing", "loaded_data", 
                          {"records": 1000, "status": "validated"})

# Resume from specific checkpoint
progress.resume_from_checkpoint("Data Processing", "loaded_data")
```

### Inline Hints & Contextual Tips

```python
from jupyter_lab_progress import show_info, show_step_guidance

# Collapsible hints
show_info("Main instruction here", 
          title="Step 1: Load Data",
          collapsible=True,
          hint="Try using pd.read_csv() function")

# Comprehensive step guidance
show_step_guidance(
    step_name="Data Cleaning",
    instructions="Remove missing values and outliers",
    tips={
        "Missing Values": "Use df.dropna() or df.fillna()",
        "Outliers": "Consider z-score > 3 as outliers"
    },
    hints=["Check df.info() first", "Use df.describe() for statistics"],
    common_mistakes=["Forgetting to reset index", "Not handling categorical data"]
)
```

### Auto-Graded Checkpoints

```python
# Set up scoring rules
validator = LabValidator()

# Add weighted scoring rules
validator.add_scoring_rule(
    name="data_loaded",
    weight=0.3,
    checker=lambda: 'data' in globals() and len(data) > 0,
    description="Data successfully loaded"
)

validator.add_scoring_rule(
    name="clean_data",
    weight=0.4,
    checker=lambda: data.isnull().sum().sum() == 0,
    description="No missing values remain"
)

validator.add_scoring_rule(
    name="analysis_complete",
    weight=0.3,
    checker=lambda: 'results' in globals(),
    description="Analysis results generated"
)

# Run auto-grading
grading_report = validator.run_auto_grading(globals())
print(f"Final Score: {grading_report['final_score']:.1f}%")
```

### Progress Analytics & Reporting

```python
# Enable analytics tracking
progress = LabProgress(steps, lab_name="Data Science Lab", persist=True)

# Export detailed analytics
csv_file = progress.export_analytics_csv()
json_file = progress.export_analytics_json()

# Display analytics dashboard
progress.display_analytics_dashboard()

# Get summary statistics
summary = progress.get_analytics_summary()
print(f"Total time: {summary['session_duration']} seconds")
print(f"Average score: {summary['average_score']:.1f}")
```

### Enhanced DataFrame Validation

```python
# DataFrame validation with visual feedback
validator.validate_dataframe(
    df,
    expected_shape=(1000, 5),
    expected_columns=['id', 'name', 'value', 'category'],
    show_preview=True,        # Shows df.head() with styling
    show_histograms=True,     # Shows histograms for numeric columns
    histogram_columns=['value', 'price']  # Specific columns only
)

# Comprehensive DataFrame analysis
analysis = validator.analyze_dataframe(df, column_focus=['price', 'category'])
# Returns detailed statistics, shows visual analysis
```

### MongoDB Status Checker

```python
# Validate MongoDB connection
validator.validate_mongodb_connection(
    connection_string="mongodb+srv://user:pass@cluster.mongodb.net/"
)

# Check database and collections
client = MongoClient("mongodb://localhost:27017/")
validator.validate_mongodb_database(client, "myapp")
validator.validate_mongodb_collection(
    client.myapp, 
    "users", 
    min_documents=100,
    expected_fields=['name', 'email', 'created_at']
)

# Comprehensive diagnostic report
report = validator.create_mongodb_diagnostic_report(client, "myapp")

# Atlas cluster health check
validator.check_mongodb_atlas_cluster_status(connection_string)
```

### Integrated Terminal & Shell Commands

```python
# Execute single shell command
success = progress.run_shell_step(
    step_name="Install Dependencies",
    command="pip install pandas numpy matplotlib",
    expected_output="Successfully installed",
    timeout=60
)

# Execute command sequence
commands = [
    "git clone https://github.com/user/repo.git",
    "cd repo",
    "pip install -r requirements.txt",
    "python setup.py test"
]

success = progress.run_shell_sequence(
    step_name="Project Setup",
    commands=commands,
    working_dir="/tmp",
    stop_on_error=True
)
```

### Custom Validators

```python
# Create step-specific validators
validator = LabValidator(progress_tracker=progress)
validate_step1 = validator.create_step_validator("Step 1")

# Use custom validation
result = compute_something()
validate_step1(result == expected_value, 
               success_msg="Perfect calculation!",
               failure_msg="Check your math")
```

### Persistence & Configuration

```python
# Advanced persistence options
progress = LabProgress(
    steps,
    lab_name="Advanced Lab",
    persist=True,
    persist_file="my_lab.json",
    auto_save=True,  # Save after each update
    step_metadata={   # Rich metadata for each step
        "Step 1": {
            "description": "Load and validate data",
            "estimated_time": 300,  # 5 minutes
            "difficulty": "easy",
            "resources": ["pandas_docs.pdf", "data_sample.csv"]
        }
    }
)
```

## 🎯 Complete Workshop Example

Here's a comprehensive example showing all the advanced features working together:

```python
from jupyter_lab_progress import *
from pymongo import MongoClient

# Step 1: Setup advanced progress tracking
steps = [
    "Environment Setup",
    "Database Connection", 
    "Data Analysis",
    "Model Training",
    "Results Export"
]

# Create progress tracker with analytics
progress = LabProgress(
    steps, 
    lab_name="Advanced Data Science Workshop",
    persist=True,
    step_metadata={
        "Environment Setup": {
            "description": "Install dependencies and verify environment",
            "estimated_time": 300
        },
        "Database Connection": {
            "description": "Connect to MongoDB and validate data",
            "estimated_time": 180
        }
    }
)

# Create validator with auto-grading
validator = LabValidator(progress_tracker=progress)

# Add scoring rules for auto-grading
validator.add_scoring_rule("env_ready", 0.2, 
                          lambda: all(lib in globals() for lib in ['pd', 'np']),
                          "Environment properly configured")

validator.add_scoring_rule("data_loaded", 0.3,
                          lambda: 'df' in globals() and len(df) > 0,
                          "Data successfully loaded")

validator.add_scoring_rule("analysis_complete", 0.5,
                          lambda: 'results' in globals(),
                          "Analysis results generated")

# Step 1: Environment Setup with shell commands
show_step_guidance(
    "Environment Setup",
    "Let's set up the Python environment",
    tips={"Virtual Environment": "Use venv or conda"},
    hints=["Check Python version first"]
)

# Execute setup commands
setup_success = progress.run_shell_sequence(
    "Environment Setup",
    [
        "python --version",
        "pip install pandas numpy matplotlib pymongo",
        "pip list | grep pandas"
    ],
    timeout_per_command=60
)

# Step 2: Database validation
show_info("Now let's connect to MongoDB", 
          title="Database Connection",
          collapsible=True,
          hint="Make sure your connection string is correct")

# MongoDB validation
connection_string = "mongodb://localhost:27017/"
validator.validate_mongodb_connection(connection_string)

client = MongoClient(connection_string)
validator.validate_mongodb_database(client, "workshop_db")

# Step 3: Data analysis with enhanced DataFrame validation
import pandas as pd
import numpy as np

# Load sample data
df = pd.DataFrame({
    'price': np.random.normal(100, 20, 1000),
    'category': np.random.choice(['A', 'B', 'C'], 1000),
    'date': pd.date_range('2024-01-01', periods=1000, freq='D')
})

# Enhanced DataFrame validation with visuals
validator.validate_dataframe(
    df,
    expected_shape=(1000, 3),
    expected_columns=['price', 'category', 'date'],
    show_preview=True,
    show_histograms=True
)

# Comprehensive DataFrame analysis
analysis = validator.analyze_dataframe(df)

# Step 4: Auto-grading and analytics
results = {"mean_price": df['price'].mean(), "categories": df['category'].nunique()}

# Run auto-grading
grade_report = validator.run_auto_grading(globals())

# Display analytics dashboard
progress.display_analytics_dashboard()

# Export results
analytics_file = progress.export_analytics_json()
grade_file = validator.export_grading_report()

show_success(f"Workshop completed! Grade: {grade_report['final_score']:.1f}%")
show_info(f"Analytics exported to: {analytics_file}")
```

This example demonstrates:
- ✅ Advanced progress tracking with metadata
- ✅ Auto-graded checkpoints with weighted scoring
- ✅ Shell command execution with validation
- ✅ MongoDB connection and database validation
- ✅ Enhanced DataFrame analysis with visuals
- ✅ Comprehensive analytics and reporting
- ✅ Step guidance with hints and tips
- ✅ Session persistence and resume capability

## 🎯 Use Cases

- **Educational Workshops**: Interactive coding workshops with guided exercises
- **Corporate Training**: Employee training programs with progress tracking
- **Online Courses**: Self-paced learning with automated validation
- **Data Science Bootcamps**: Hands-on exercises with immediate feedback
- **Research Training**: Academic lab exercises with validation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/mrlynn/jupyter-lab-utils.git
cd jupyter-lab-utils/jupyter-lab-progress
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest
pytest --cov=jupyter_lab_progress --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [https://github.com/mrlynn/jupyter-lab-utils#readme](https://github.com/mrlynn/jupyter-lab-utils#readme)
- **Issues**: [GitHub Issues](https://github.com/mrlynn/jupyter-lab-utils/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mrlynn/jupyter-lab-utils/discussions)

## 🏗️ Built by Michael Lynn [https://mlynn.org](https://mlynn.org)

Created with ❤️ by the MongoDB Developer Relations team to enhance the learning experience in data science and development workshops.

---

**Happy Teaching and Learning!** 🎓