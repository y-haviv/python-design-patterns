# Getting Started with Python Design Patterns

Welcome! This guide will help you get up and running with the Python Design Patterns repository.

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Clone the Repository

```bash
# Clone the repository
git clone https://github.com/y-haviv/python-design-patterns.git
cd python-design-patterns

# (Optional) Fork first, then clone your fork
git clone https://github.com/y-haviv/python-design-patterns.git
cd python-design-patterns
```

### Set Up Your Development Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Your First Pattern

### 1. Choose a Pattern

Let's start with **Singleton** - it's the simplest:

```bash
cd creational/singleton
```

### 2. Read the Documentation

```bash
# Read the pattern description
cat README.md

# Or open in your editor
code README.md  # VS Code
nano README.md  # Terminal
```

### 3. Study the Implementation

```bash
# Look at the core pattern
cat pattern.py

# See how it's used in real-world scenarios
cat real_world_example.py
```

### 4. Run the Tests

```bash
# Run tests for this pattern
pytest test_pattern.py -v

# Run tests with coverage
pytest test_pattern.py --cov=. --cov-report=term-missing
```

### 5. Experiment!

```python
# Create a Python file to experiment
# example.py

from creational.singleton import Singleton

# Create instances
instance1 = Singleton()
instance2 = Singleton()

# They're the same object!
assert instance1 is instance2
print(f"Same instance: {instance1 is instance2}")
```

Then run it:

```bash
python example.py
```

---

## 📚 Learning Paths

### Path 1: Beginner (2-3 hours)
1. [Singleton](../creational/singleton/) - Learn the basics
2. [Factory Method](../creational/factory/) - Understand object creation
3. [Observer](../behavioral/observer/) - See loose coupling in action

**Outcome:** Understand why patterns matter

### Path 2: Intermediate (5-7 hours)
1. All Creational patterns
2. Key Structural patterns: Adapter, Composite, Decorator
3. Key Behavioral patterns: Strategy, Command, State

**Outcome:** Know when and how to apply patterns

### Path 3: Advanced (10+ hours)
1. Complete study of all 21 patterns
2. Pattern combinations and interactions
3. Real-world application design

**Outcome:** Mastery of design patterns for production systems

---

## 🔍 Understanding the File Structure

```
python-design-patterns/
├── creational/           # Object creation patterns (5)
│   ├── singleton/       # Learn object instantiation
│   ├── factory/         # Deferred creation
│   ├── abstract_factory/# Family of objects
│   ├── builder/         # Complex construction
│   └── prototype/       # Cloning objects
│
├── structural/          # Object composition patterns (7)
│   ├── adapter/         # Interface compatibility
│   ├── bridge/          # Abstraction separation
│   ├── composite/       # Tree structures
│   ├── decorator/       # Dynamic enhancement
│   ├── facade/          # Simplified interface
│   ├── flyweight/       # Object sharing
│   └── proxy/           # Access control
│
├── behavioral/          # Object interaction patterns (8)
│   ├── command/         # Request encapsulation
│   ├── iterator/        # Sequential access
│   ├── mediator/        # Centralized communication
│   ├── memento/         # State preservation
│   ├── observer/        # One-to-many notification
│   ├── state/           # State-dependent behavior
│   ├── strategy/        # Algorithm encapsulation
│   └── visitor/         # Tree traversal
│
├── docs/                # Documentation
├── README.md            # Project overview
├── CONTRIBUTING.md      # How to contribute
└── pyproject.toml       # Project configuration
```

## 📖 Each Pattern Contains

```
pattern_name/
├── __init__.py              # Module initialization
├── README.md                # Pattern documentation
├── pattern.py               # Core implementation
├── real_world_example.py    # Practical use case
└── test_pattern.py          # Test suite
```

---

## 💻 Common Tasks

### Run All Tests

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html to see coverage
```

### Format Your Code

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Check code style
flake8 .
```

### Type Checking

```bash
# Check types with mypy
mypy .
```

### Study a Specific Pattern

```bash
# Run Adapter pattern tests
pytest structural/adapter/test_pattern.py -v

# Run all tests in a category
pytest creational/ -v
pytest structural/ -v
pytest behavioral/ -v
```

---

## 🎓 Learning Tips

### 1. Read the README First
Each pattern README has:
- **Intent** - What the pattern does
- **Problem** - What it solves
- **Solution** - How it works
- **Examples** - Real-world usage

### 2. Study the Code
- Start with `pattern.py` - core concepts
- Then `real_world_example.py` - practical application
- Finally `test_pattern.py` - edge cases

### 3. Run the Tests
```bash
pytest pattern_name/test_pattern.py -v
```

### 4. Modify and Experiment
- Change the code
- Run tests again
- See how it breaks
- Understand why

### 5. Apply to Your Project
- Identify problems in your code
- Find matching patterns
- Refactor using the pattern
- See improvements

---

## ❓ FAQ

**Q: Where do I start?**  
A: Start with [Singleton](../creational/singleton/) or [Factory Method](../creational/factory/)

**Q: How long will it take to learn all patterns?**  
A: 20-40 hours of focused study, depending on your background

**Q: Do I need to memorize all patterns?**  
A: No! Understand 5-10 key patterns well, then refer back as needed

**Q: Can I use these in production?**  
A: Absolutely! These are production-ready implementations

**Q: How do I contribute?**  
A: See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 🔗 Additional Resources

### Documentation
- [Architecture Guide](ARCHITECTURE.md) - Project structure
- [Patterns Overview](PATTERNS_OVERVIEW.md) - Deep comparison
- [Development Guide](DEVELOPMENT.md) - Contributing guide
- [FAQ](FAQ.md) - Common questions

### External Resources
- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) - The original Gang of Four book
- [Refactoring.Guru Design Patterns](https://refactoring.guru/design-patterns) - Interactive examples
- [Python Design Patterns Guide](https://python-patterns.guide/) - Pythonic patterns

---

## 🚨 Common Issues

### Issue: Import Errors
```python
# ❌ Wrong
from pattern import Singleton

# ✅ Right
from creational.singleton import Singleton
```

### Issue: Tests Not Found
```bash
# ❌ Wrong - from wrong directory
python test_pattern.py

# ✅ Right - from project root
pytest creational/singleton/test_pattern.py
```

### Issue: Virtual Environment Not Activated
```bash
# Check if activated (should see (venv) in prompt)
# If not, activate:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

## 🎉 Next Steps

1. **Pick a pattern** - Choose one that interests you
2. **Read its README** - Understand the concept
3. **Study the code** - Learn the implementation
4. **Run the tests** - See it in action
5. **Experiment** - Modify and create
6. **Apply** - Use it in your projects
7. **Contribute** - Help others learn!

---


