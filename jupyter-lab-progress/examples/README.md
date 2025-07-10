# 📚 jupyter-lab-progress Examples

This directory contains comprehensive examples demonstrating all features of the `jupyter-lab-progress` library. These notebooks are designed to help educators create engaging, interactive lab experiences.

## 📓 Example Notebooks

### 1. [Progress Tracking](01_progress_tracking.ipynb)
**Complete guide to the `LabProgress` class**

Learn how to:
- Create progress trackers with custom steps
- Mark steps as completed
- Display beautiful progress bars
- Get completion statistics
- Reset and manage progress
- Best practices for lab structure

**Perfect for:** Understanding the core progress tracking functionality

---

### 2. [Display Utilities](02_display_utilities.ipynb)
**Master the `show_info` and `show_warning` functions**

Discover how to:
- Create eye-catching info messages
- Display important warnings
- Structure lab instructions
- Guide students through complex tasks
- Handle errors gracefully
- Create interactive tutorials

**Perfect for:** Creating polished, professional lab experiences

---

### 3. [Validation Utilities](03_validation_utilities.ipynb)
**Deep dive into the `LabValidator` class**

Explore how to:
- Validate embedding dimensions
- Check DataFrame contents
- Ensure data integrity
- Create custom validators
- Generate validation reports
- Catch common student mistakes

**Perfect for:** Data science and ML workshops

---

### 4. [Complete MongoDB Lab](04_complete_mongodb_lab.ipynb)
**Full-featured workshop combining all features**

Experience a real-world lab that covers:
- Building a vector search system
- E-commerce product search
- MongoDB Atlas integration
- Comprehensive validation
- Performance testing
- Professional lab structure

**Perfect for:** Seeing everything work together in practice

## 🚀 Getting Started

### Method 1: Quick Start (Recommended)
1. **Install jupyter-lab-progress:**
   ```bash
   pip install jupyter-lab-progress
   ```

2. **Run the notebooks:**
   ```bash
   jupyter lab
   ```
   Open any notebook to start exploring!

### Method 2: Complete Environment Setup
For a full environment with all optional dependencies:

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using conda:**
```bash
conda env create -f environment.yml
conda activate jupyter-lab-progress-examples
```

### Method 3: Automatic Setup (In Notebooks)
Each notebook includes an automatic setup cell that will install missing packages:
```python
# First cell in each notebook handles dependencies automatically
import sys
import subprocess

try:
    import jupyter_lab_progress
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyter-lab-progress"])
```

## 📦 Dependencies

### Core Dependencies (automatically installed)
- `jupyter-lab-progress` - The main package
- `pandas>=1.0.0` - Data manipulation
- `numpy>=1.18.0` - Numerical computing
- `ipython>=7.0.0` - Interactive Python

### Optional Dependencies (for specific examples)
- `matplotlib>=3.0.0` - Plotting and visualization
- `seaborn>=0.11.0` - Statistical data visualization
- `plotly>=5.0.0` - Interactive visualizations
- `pymongo>=4.0.0` - MongoDB driver (for MongoDB examples)
- `dnspython>=2.0.0` - DNS support for MongoDB

## 🛠️ Troubleshooting

### Common Issues

**"Module not found" errors:**
- Run the first cell in any notebook - it will auto-install missing packages
- Or manually install: `pip install jupyter-lab-progress matplotlib seaborn plotly pymongo`

**Import errors in Jupyter:**
- Restart your kernel: `Kernel` → `Restart Kernel`
- Or run: `%pip install jupyter-lab-progress` in a notebook cell

**Package version conflicts:**
- Create a fresh environment: `conda create -n jupyter-examples python=3.9`
- Install from requirements: `pip install -r requirements.txt`

## 📋 How to Use These Examples

### For Educators:
- **Start with notebook 1** to understand basic progress tracking
- **Use notebook 2** to learn message styling
- **Study notebook 3** for data validation patterns
- **Reference notebook 4** for complete workshop structure

### For Workshop Participants:
- Follow along with the notebooks during workshops
- Experiment with different parameters
- Try your own data and use cases
- Use as templates for your own projects

## 🎯 Example Use Cases

These notebooks demonstrate patterns for:

### Technical Workshops
```python
from jupyter_lab_progress import LabProgress, show_info

# MongoDB workshops
progress = LabProgress([
    "Set up Atlas account",
    "Create cluster", 
    "Connect with Python",
    "Insert documents",
    "Create indexes"
])

show_info("Welcome to MongoDB Essentials! 🍃")
```

### Data Science Labs
```python
from jupyter_lab_progress import LabValidator, show_warning

validator = LabValidator()

# Validate embeddings before training
if validator.check_embedding_shape(embeddings, 384):
    show_info("✅ Embeddings ready for model training!")
else:
    show_warning("❌ Check your embedding dimensions")
```

### ML/AI Workshops
```python
# Track complex ML pipeline
ml_progress = LabProgress([
    "Data Collection",
    "Feature Engineering", 
    "Model Training",
    "Evaluation",
    "Deployment"
], title="🤖 ML Pipeline Progress")
```

## 🛠️ Customization

All examples can be customized for your specific needs:

- **Change the steps** to match your workshop content
- **Modify validation rules** for your data requirements  
- **Update messages** with your branding
- **Add custom progress trackers** for complex workflows

## 💡 Best Practices from Examples

### Progress Tracking
- Use descriptive step names
- Group related tasks
- Add checkpoints for long labs
- Show progress after each major step

### Display Messages
- Use `show_info()` for tips and success messages
- Use `show_warning()` for important notices
- Include emojis for visual appeal
- Keep messages concise but helpful

### Validation
- Validate early and often
- Provide clear error messages
- Use context parameters for debugging
- Create custom validators for complex checks

## 📖 Additional Resources

- **Package Documentation:** [PyPI - jupyter-lab-progress](https://pypi.org/project/jupyter-lab-progress/)
- **GitHub Repository:** [jupyter-lab-progress](https://github.com/mrlynn/jupyter-lab-utils)
- **MongoDB Resources:** [MongoDB Developer Hub](https://developer.mongodb.com/)

## 🤝 Contributing

Found these examples helpful? Consider:

- ⭐ Starring the repository
- 🐛 Reporting issues
- 💡 Suggesting improvements
- 📖 Contributing more examples

## 📄 License

These examples are provided under the MIT License - feel free to use them in your own workshops and training materials!

---

<p align="center">
  Made with ❤️ for the teaching community by Michael Lynn
</p>