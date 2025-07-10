# 🚀 Jupyter Lab Utils

[![PyPI version](https://badge.fury.io/py/jupyter-lab-utils-mrlynn.svg)](https://badge.fury.io/py/jupyter-lab-utils-mrlynn)
[![Python Version](https://img.shields.io/pypi/pyversions/jupyter-lab-utils-mrlynn.svg)](https://pypi.org/project/jupyter-lab-utils-mrlynn/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transform your Jupyter notebooks into interactive, professional learning experiences with beautiful progress tracking, instant validation, and stunning visual feedback.

## ✨ Why Jupyter Lab Utils?

Teaching complex technical concepts in Jupyter notebooks can be challenging. Students need clear visual feedback, instructors need reliable progress tracking, and everyone benefits from a more engaging learning experience. 

**Jupyter Lab Utils** bridges this gap by providing:

- 📊 **Visual Progress Tracking** - Beautiful progress bars that show lab completion at a glance
- ✅ **Instant Validation** - Real-time feedback when students complete tasks correctly  
- 🎨 **Stunning Visual Messages** - Eye-catching info and warning boxes that grab attention
- 🎓 **Perfect for Education** - Designed specifically for workshops, tutorials, and technical training

## 🎯 See It In Action

```python
from jupyter_lab_utils import LabProgress, show_info, show_warning

# Create a progress tracker for your lab
progress = LabProgress(total_steps=5)

# Show beautiful, styled messages
show_info("Welcome to the MongoDB Vector Search Lab! 🚀")

# Track progress as students complete tasks
progress.mark_completed("Set up connection")  # ✅ 1/5 completed
progress.mark_completed("Create embeddings")  # ✅ 2/5 completed

# Instant visual feedback
show_warning("Remember to check your index status before querying!")
```

## 📦 Installation

```bash
pip install jupyter-lab-utils-mrlynn
```

## 🛠️ Core Features

### Progress Tracking

Create engaging progress bars that update in real-time as students work through your labs:

```python
from jupyter_lab_utils import LabProgress

# Initialize tracker
progress = LabProgress(
    steps=["Connect to MongoDB", "Load data", "Create embeddings", "Build index", "Run queries"],
    title="Vector Search Lab Progress"
)

# Mark steps complete
progress.mark_completed("Connect to MongoDB")
progress.display()  # Shows beautiful HTML progress bar
```

### Data Validation

Validate student work instantly with helpful feedback:

```python
from jupyter_lab_utils import LabValidator

validator = LabValidator()

# Check if embeddings have correct dimensions
is_valid = validator.check_embedding_shape(embeddings, expected_dim=384)

# Verify data exists in DataFrame
validator.assert_in_dataframe(
    df=student_df, 
    column="product_embeddings",
    values=["embedding_1", "embedding_2"],
    context="Product embeddings should be generated"
)
```

### Visual Messaging

Replace boring print statements with eye-catching styled messages:

```python
from jupyter_lab_utils import show_info, show_warning

# Beautiful blue info boxes
show_info("🎉 Great job! Your vector index is ready to use.")

# Attention-grabbing yellow warnings  
show_warning("⚠️ Make sure your connection string includes credentials!")
```

## 🎓 Perfect For

- **Technical Workshops** - Track student progress in real-time
- **Online Tutorials** - Provide instant feedback and validation
- **University Courses** - Make labs more interactive and engaging
- **Corporate Training** - Professional progress tracking for technical training
- **Self-Paced Learning** - Help learners stay motivated with visual progress

## 🏢 Built for MongoDB Developer Days

Originally created for MongoDB's Developer Days and workshops, this library has been battle-tested with hundreds of developers learning about:
- Vector Search and AI applications
- Atlas cluster management
- Aggregation pipelines
- Index optimization
- And more!

## 📚 Full Example

```python
from jupyter_lab_utils import LabProgress, LabValidator, show_info, show_warning

# Set up the lab
progress = LabProgress(
    steps=["Environment Setup", "Data Import", "Vector Creation", "Index Building", "Similarity Search"]
)
validator = LabValidator()

# Welcome message
show_info("Welcome to the Vector Search Lab! Let's build an AI-powered search engine.")

# Step 1: Environment setup
import pymongo
client = pymongo.MongoClient(connection_string)
progress.mark_completed("Environment Setup")

# Step 2: Data import with validation
data = load_products()
validator.assert_in_dataframe(
    df=data,
    column="name",
    values=["laptop", "headphones"],
    context="Product catalog import"
)
progress.mark_completed("Data Import")

# Continue through the lab...
```

## 🤝 Contributing

We love contributions! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 💡 Feature suggestions

Please check out our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 License

MIT License - feel free to use this in your own workshops and training materials!

## 🙏 Acknowledgments

Special thanks to the MongoDB Developer Relations team and all the workshop participants who provided feedback to make this library better.

---

<p align="center">
  Made with ❤️ for the teaching community by Michael Lynn
</p>