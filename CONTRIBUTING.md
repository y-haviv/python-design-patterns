# Contributing to Python Design Patterns

---

## 💡 How Can You Contribute?

### 1. Report Bugs 🐛

Found a bug? Help us fix it!

**Before submitting a bug report:**
- Check if the issue already exists
- Verify the bug is reproducible
- Collect relevant information

**When submitting a bug report, please include:**
- Clear, descriptive title
- Exact steps to reproduce the problem
- Code samples and expected behavior
- Python version and OS information
- Any relevant error messages or logs

### 2. Suggest Enhancements 💭

Have an idea? We'd love to hear it!

**Before suggesting an enhancement:**
- Check if it's already been suggested
- Provide clear use cases

**When suggesting an enhancement:**
- Use a clear, descriptive title
- Provide a step-by-step description
- Provide specific examples
- Describe the current behavior and expected behavior
- Explain why this enhancement would be useful

### 3. Submit Pull Requests 📝

This is the best way to contribute code!

**Before you start:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Read the Development Guide below

**When submitting a PR:**
- Include a clear description of changes
- Reference any related issues
- Follow the code style guidelines
- Include tests for new functionality
- Update documentation as needed
- Keep commits logical and atomic

### 4. Improve Documentation 📚

Documentation is crucial for learning!

**Ways to help:**
- Fix typos or unclear explanations
- Add missing examples
- Create tutorials or guides
- Translate documentation
- Improve pattern explanations

---

## 🛠️ Development Guide

### Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/y-haviv/python-design-patterns.git
cd python-design-patterns

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (including dev tools)
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dev tools: pytest, black, etc.
```

### Code Style Requirements

We follow PEP 8 and use tools to enforce consistency:

```bash
# Format code with black
black .

# Check code style
flake8 .

# Type checking
mypy .

# All checks
pre-commit run --all-files
```

### Adding a New Pattern

To add a complete pattern implementation, create the following structure:

```
pattern_category/your_pattern/
├── __init__.py                 # Empty initialization
├── pattern.py                  # Core pattern implementation
├── real_world_example.py       # Practical example
├── test_pattern.py             # Comprehensive tests
└── README.md                   # Documentation
```

#### 1. **pattern.py** Template

```python
"""
Core implementation of the [Pattern Name] pattern.

The [Pattern Name] pattern solves [the problem] by [the solution].
This module provides:
- Abstract interfaces using ABC
- Concrete implementations
- Usage examples
"""

from abc import ABC, abstractmethod
from typing import Any


class PatternInterface(ABC):
    """Abstract interface for the pattern."""
    
    @abstractmethod
    def operation(self) -> str:
        """Perform the operation."""
        pass


class ConcreteImplementation(PatternInterface):
    """Concrete implementation of the pattern."""
    
    def operation(self) -> str:
        """Implementation details."""
        return "Result"


# Include 2-3 more realistic implementations
# Include factory if applicable
# Include helper utilities
```

#### 2. **real_world_example.py** Template

```python
"""
Real-world example of the [Pattern Name] pattern.

This example demonstrates [Pattern Name] in a practical scenario: [use case].
"""

# Implementation should be:
# - Realistic and practical
# - Well-commented
# - Include error handling
# - Show multiple use cases when applicable
```

#### 3. **test_pattern.py** Template

```python
"""
Comprehensive test suite for the [Pattern Name] pattern.

Tests cover:
- Basic pattern functionality
- Edge cases
- Error scenarios
- Integration between components
"""

import pytest
from .pattern import *


class TestPatternCore:
    """Test core pattern functionality."""
    
    def test_basic_usage(self):
        """Test basic pattern usage."""
        # Arrange
        # Act
        # Assert
        pass


class TestPatternRealWorld:
    """Test real-world implementations."""
    pass


class TestPatternEdgeCases:
    """Test edge cases and error handling."""
    pass
```

#### 4. **README.md** Template

Use the structure from existing pattern READMEs:
- **Intent** - What is the pattern?
- **Problem** - What problem does it solve?
- **Solution** - How does it work?
- **Key Components** - Diagram and explanation
- **Advantages** - When to use it
- **Disadvantages** - Limitations
- **Real-World Applications** - Practical uses
- **Comparison** - Alternatives and differences
- **Common Pitfalls** - What to avoid
- **Related Patterns** - Similar patterns

---

### Writing Tests

Good tests are essential:

```python
import pytest
from your_module import YourClass


class TestYourClass:
    """Test suite for YourClass."""
    
    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return YourClass()
    
    def test_basic_functionality(self, instance):
        """Test basic operation."""
        result = instance.do_something()
        assert result == expected_value
    
    def test_error_handling(self):
        """Test error conditions."""
        with pytest.raises(ValueError):
            YourClass(invalid_input)
    
    @pytest.mark.parametrize("input,expected", [
        ("case1", "result1"),
        ("case2", "result2"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple scenarios."""
        assert function(input) == expected
```

### Testing Your Code

```bash
# Run all tests
pytest

# Run specific test file
pytest structural/adapter/test_pattern.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest -k "test_name"

# Run in verbose mode
pytest -v
```

---

## 📋 Commit Guidelines

Write clear, meaningful commit messages:

```bash
# Good examples:
git commit -m "Add Adapter pattern implementation with tests"
git commit -m "Fix: Handle edge case in Singleton pattern"
git commit -m "Docs: Improve Decorator pattern README clarity"

# Format:
# [Type]: Brief description (50 chars max)
# [optional body with more details]

# Types: feat, fix, docs, style, refactor, test, chore
```

---

## 📤 Pull Request Process

1. **Create your feature branch**: `git checkout -b feature/amazing-feature`
2. **Make your changes** following the style guide
3. **Add or update tests** - all new code needs tests
4. **Update documentation** - keep READMEs current
5. **Test locally**: `pytest` and `black` checks must pass
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request** with clear description


### PR Checklist

- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] My commit messages are clear and follow guidelines

---

## 📝 License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.

---

## ❓ Questions?

- 📖 Check [docs/](docs/)
- 💬 Open a discussion on GitHub

---

