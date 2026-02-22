# Development Guide

This guide is for developers who want to contribute to the Python Design Patterns project.

---

## 🎯 Before You Start

- Read [CONTRIBUTING.md](../CONTRIBUTING.md) - contribution guidelines
- Review [ARCHITECTURE.md](ARCHITECTURE.md) - project structure

---

## 🛠️ Local Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/y-haviv/python-design-patterns.git
cd python-design-patterns

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install regular dependencies
pip install -r requirements.txt
```

### 2. Install Development Tools

```bash
# Install dev tools for code quality
pip install black isort flake8 mypy pytest-cov pre-commit

# Or install from requirements-dev.txt (if it exists)
pip install -r requirements-dev.txt
```

### 3. Set Up Pre-commit Hooks

```bash
# Install pre-commit framework
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

---

## 📝 Making Changes

### Step 1: Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/descriptive-name

# Or for bug fixes
git checkout -b fix/bug-description

# Or for documentation
git checkout -b docs/update-description
```

### Step 2: Make Your Changes

Choose your contribution type:

#### Adding a New Pattern

```bash
# Create pattern directory
mkdir creational/new_pattern  # or structural/ or behavioral/

# Create required files
touch creational/new_pattern/__init__.py
touch creational/new_pattern/pattern.py
touch creational/new_pattern/real_world_example.py
touch creational/new_pattern/test_pattern.py
touch creational/new_pattern/README.md
```

Then implement:

1. **pattern.py** - Core implementation
2. **real_world_example.py** - Practical example
3. **test_pattern.py** - Test suite
4. **README.md** - Documentation
5. **__init__.py** - Module exports

#### Enhancing Existing Pattern

```bash
# Make changes to:
structural/adapter/pattern.py        # Add features
structural/adapter/test_pattern.py   # Add tests
structural/adapter/README.md         # Update docs
```

#### Improving Documentation

```bash
# Update any README.md or docs/*.md files
# No code changes needed for pure docs
```

### Step 3: Verify Your Changes

```bash
# Format code
black .
isort .

# Lint
flake8 .

# Type check
mypy .

# Run tests
pytest -v

# Check coverage
pytest --cov=. --cov-report=term-missing
```

### Step 4: Commit Your Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: Add [Pattern Name] implementation

- Implement core pattern classes
- Add comprehensive real-world example
- Include full test coverage
- Update documentation"

# Example commit messages:
# feat: Add Prototype pattern
# fix: Handle edge case in Singleton pattern  
# docs: Improve Adapter pattern README
# test: Add edge case tests for Decorator pattern
# refactor: Simplify State pattern implementation
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest creational/singleton/test_pattern.py

# Run specific test
pytest -k "test_singleton_creates_same_instance"

# Run with coverage
pytest --cov=. --cov-report=html

# Run with markers
pytest -m "not slow"
```

### Writing Tests

Follow this structure for all tests:

```python
"""
Test suite for the Pattern Name pattern.

Tests cover:
- Core pattern functionality
- Real-world example usage
- Edge cases and error handling
"""

import pytest
from .pattern import MyClass, Helper


class TestPatternCore:
    """Test core pattern components."""
    
    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return MyClass()
    
    def test_basic_functionality(self, instance):
        """Test basic operation."""
        result = instance.do_something()
        assert result == expected_value
    
    def test_multiple_instances(self):
        """Test pattern with multiple instances."""
        obj1 = MyClass()
        obj2 = MyClass()
        # Add assertions
    
    @pytest.mark.parametrize("input,expected", [
        ("case1", "result1"),
        ("case2", "result2"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple scenarios with parametrize."""
        assert function(input) == expected


class TestRealWorldExample:
    """Test real-world implementation."""
    
    def test_real_scenario(self):
        """Test the real-world example."""
        # Implementation
        pass


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_invalid_input(self):
        """Test error handling for invalid input."""
        with pytest.raises(ValueError):
            MyClass(invalid_param)
    
    def test_boundary_conditions(self):
        """Test boundary conditions."""
        pass


class TestIntegration:
    """Test integration between components."""
    
    def test_component_interaction(self):
        """Test how components work together."""
        pass
```

### Code Coverage

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Open report (macOS/Linux)
open htmlcov/index.html

# Open report (Windows)
start htmlcov/index.html

# Generate terminal report
pytest --cov=. --cov-report=term-missing

# Coverage thresholds (check pyproject.toml)
pytest --cov=. --cov-fail-under=90
```

---

## 🔍 Code Quality

### Using Black

```bash
# Format all files
black .

# Format specific file
black creational/singleton/pattern.py

# Check without formatting
black --check .
```

### Using isort

```bash
# Sort imports in all files
isort .

# Sort specific file
isort creational/singleton/pattern.py

# Check without changing
isort --check-only .
```

### Using Flake8

```bash
# Check all files
flake8 .

# Check specific file
flake8 creational/singleton/pattern.py

# Ignore specific errors
flake8 . --ignore=E501  # Ignore long lines
```

### Using MyPy

```bash
# Type check all files
mypy .

# Type check specific file
mypy creational/singleton/pattern.py

# Generate report
mypy . --html mypy_report
```

### Pre-commit

```bash
# Run all pre-commit checks
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks temporarily
git commit --no-verify
```

---

## 📚 Documentation

### Writing READMEs

Every pattern README should have:

1. **Pattern Name (H1)**
   ```markdown
   # Pattern Name
   ```

2. **Badges**
   ```markdown
   [![Pattern](https://img.shields.io/badge/Type-Structural-blue)]()
   ```

3. **Intent** (2-3 paragraphs)
   - What is this pattern?
   - What problem does it solve?

4. **Problem** (with example)
   - Real problem it addresses
   - Code example showing the problem

5. **Solution** (with diagram if possible)
   - How the pattern solves it
   - Design principles applied

6. **Key Components**
   - Class diagram in ASCII or description
   - Explanation of each component

7. **Advantages**
   - Why use this pattern?
   - Real benefits

8. **Disadvantages**
   - Limitations and trade-offs
   - When NOT to use it

9. **Real-World Applications**
   - Where you see this pattern
   - Framework/library examples

10. **Comparison with Similar Patterns**
    - Differences from related patterns
    - When to choose this one

11. **Common Pitfalls**
    - Mistakes to avoid
    - Anti-patterns related to this

12. **Related Patterns**
    - Patterns that work well together
    - Alternative solutions

---

## 🔄 Git Workflow

### Standard Flow

```bash
# 1. Pull latest main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and commit
git add .
git commit -m "message"

# 4. Push to your fork
git push origin feature/your-feature

# 5. Create Pull Request on GitHub
# - Describe what you changed
# - Reference any related issues
# - Fill out PR template

# 6. Address review comments
# Make changes locally, push again
git push origin feature/your-feature

# 7. Once approved, merge via GitHub UI
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style changes (formatting)
- `refactor` - Code refactoring
- `test` - Test additions/changes
- `chore` - Build/deps/tooling

**Examples:**
```bash
git commit -m "feat: Add Builder pattern implementation"
git commit -m "fix: Correct thread safety in Singleton"
git commit -m "docs: Improve README clarity"
git commit -m "test: Add edge case tests for Adapter"
git commit -m "refactor: Simplify AbstractFactory code"
```

---

## 📤 Creating a Pull Request

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Added/updated tests
- [ ] All tests pass locally
- [ ] Updated documentation
- [ ] Commit messages are clear
- [ ] No breaking changes
- [ ] Ready for review

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New pattern implementation
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Related Issues
Closes #<issue_number>

## Changes Made
- Specific change 1
- Specific change 2

## Testing Done
- Test scenario 1
- Test scenario 2

## Breaking Changes
None / Description

## Additional Notes
Any additional information
```

---

## 🐛 Debugging

### Debug Tests

```bash
# Run with verbose output
pytest -vv

# Run with print statements shown
pytest -s

# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show local variables on failure
pytest -l
```

### Debug Code

```python
# Use print debugging
print(f"Value: {variable}")
print(f"Type: {type(variable)}")

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Message: {variable}")

# Use debugger
import pdb
pdb.set_trace()  # Execution stops here
```

---

## 📊 Performance Testing

### Simple Profiling

```python
import time

start = time.time()
# Code to profile
end = time.time()
print(f"Took {end - start} seconds")
```

### Profile with cProfile

```bash
python -m cProfile -s cumulative script.py
```

### Memory Profiling

```bash
pip install memory-profiler

python -m memory_profiler script.py
```

---

## 🚀 Before Submitting

### Final Checklist

```bash
# 1. Format code
black .
isort .

# 2. Lint
flake8 .

# 3. Type check
mypy .

# 4. Run all tests
pytest -v

# 5. Check coverage
pytest --cov=. --cov-report=term-missing

# 6. Review your changes
git diff main

# 7. Update documentation if needed
# 8. Create descriptive commit

git commit -m "your-message"

# 9. Push to your fork
git push origin your-branch

# 10. Create PR on GitHub
```

---

## 📞 Getting Help

- 📖 Check documentation in `docs/`
- 💬 Open a GitHub discussion
- 🐛 Report issues in GitHub issues

---

