# Architecture Guide

This document describes the architecture and organization of the Python Design Patterns project.

---

## 🏗️ Project Structure

```
python-design-patterns/
├── creational/              # Object creation patterns
│   ├── singleton/
│   │   ├── __init__.py
│   │   ├── pattern.py              # Core pattern
│   │   ├── real_world_example.py   # Practical example
│   │   ├── test_pattern.py         # Tests
│   │   └── README.md               # Documentation
│   ├── factory/
│   ├── abstract_factory/
│   ├── builder/
│   ├── prototype/
│   ├── __init__.py                 # Module init (exports)
│   └── README.md                   # Category overview
│
├── structural/              # Object composition patterns
│   ├── adapter/
│   ├── bridge/
│   ├── composite/
│   ├── decorator/
│   ├── facade/
│   ├── flyweight/
│   ├── proxy/
│   ├── __init__.py                 # Module init (exports)
│   └── README.md                   # Category overview
│
├── behavioral/              # Object interaction patterns
│   ├── command/
│   ├── iterator/
│   ├── mediator/
│   ├── memento/
│   ├── observer/
│   ├── state/
│   ├── strategy/
│   ├── visitor/
│   ├── __init__.py                 # Module init (exports)
│   └── README.md                   # Category overview
│
├── docs/                    # Documentation
│   ├── GETTING_STARTED.md
│   ├── ARCHITECTURE.md     (this file)
│   ├── PATTERNS_OVERVIEW.md
│   ├── DEVELOPMENT.md
│   └── FAQ.md
│
├── .github/
│   ├── workflows/           # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/     # GitHub issue templates
│   └── PULL_REQUEST_TEMPLATE/  # PR template
│
├── README.md               # Project overview
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
├── CHANGELOG.md            # Version history
├── CODEOWNERS              # Code ownership
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Python project config
└── requirements.txt        # Dependencies
```

---

## 📚 File Purposes

### Pattern Directories

Each pattern has a consistent structure for consistency and discoverability:

#### `pattern.py` (100-300 lines)

**Purpose:** Core pattern implementation

**Contains:**
- Abstract base classes (ABC) for interfaces
- Concrete implementations (2-4 variations)
- Helper classes/utilities
- Factory functions where applicable
- Complete docstrings

**Style:**
```python
from abc import ABC, abstractmethod
from typing import Optional, List

class AbstractInterface(ABC):
    """Abstract interface for the pattern."""
    
    @abstractmethod
    def operation(self) -> str:
        """Define the operation."""
        pass

class ConcreteImplementation(AbstractInterface):
    """Concrete implementation."""
    
    def operation(self) -> str:
        """Implement the operation."""
        return "result"
```

#### `real_world_example.py` (150-300 lines)

**Purpose:** Practical, realistic example

**Contains:**
- Real-world scenario implementation
- Multiple use cases when applicable
- Error handling and edge cases
- Comments explaining decisions
- Practical output/examples

**Guidelines:**
- Should run without external dependencies
- Should be understandable in 5 minutes
- Should demonstrate actual problem-solving
- Should include multiple variations

#### `test_pattern.py` (200-400 lines)

**Purpose:** Comprehensive test coverage

**Contains:**
- Unit tests for core classes
- Integration tests for real-world example
- Edge case and error scenario tests
- Parametrized tests for variations
- Performance tests where relevant

**Structure:**
```python
class TestPatternCore:
    """Test core pattern components."""
    def test_basic_functionality(self):
        pass

class TestRealWorldExample:
    """Test real-world implementation."""
    def test_scenario(self):
        pass

class TestEdgeCases:
    """Test edge cases and errors."""
    def test_invalid_input(self):
        pass
```

#### `README.md` (400-600 lines)

**Purpose:** pattern documentation

**Sections:**
1. **Intent** - What is this pattern?
2. **Problem** - What problem does it solve?
3. **Solution** - How does it work?
4. **Key Components** - Class diagram and descriptions
5. **Advantages** - When to use it
6. **Disadvantages** - Limitations and concerns
7. **Real-World Applications** - Practical uses
8. **Comparison** - Similar patterns and differences
9. **Common Pitfalls** - What to avoid
10. **Related Patterns** - Pattern relationships

### Module Level

#### Category `__init__.py`

**Purpose:** Module-level initialization and exports

**Contains:**
- Import all public classes from pattern modules
- Define comprehensive `__all__` list
- Optional: convenience imports
- Module docstring with overview

**Example:**
```python
"""Structural design patterns for object composition."""

from .adapter import Adapter, Target, Adaptee
from .bridge import Abstraction, Implementor
# ... more imports

__all__ = [
    'Adapter', 'Target', 'Adaptee',
    'Abstraction', 'Implementor',
    # ... more exports
]
```

#### Category `README.md`

**Purpose:** Overview of pattern category

**Contains:**
- Category description
- Quick reference table
- Pattern list with brief descriptions
- Getting started guide
- Common pitfalls
- Selection guide

---

## 🔄 Dependencies and Imports

### Dependency Model

```
Application Code
        ↓
Any Pattern Module (e.g., creational.singleton)
        ↓
Pattern Implementation (ABC, classes)
        ↓
Python Standard Library Only
```

**Key Principle:** No external dependencies for core patterns

### Internal Imports

```python
# ✅ Good - Explicit imports
from .pattern import Singleton
from ..some_other_pattern import Component

# ✅ Good - For tests
from creational.singleton import Singleton

# ❌ Avoid - Star imports in non-test code
from pattern import *

# ❌ Avoid - Circular imports
# (patterns are designed to avoid this)
```

---

## 🧪 Testing Architecture

### Test Organization

```
pattern/
└── test_pattern.py
    ├── TestPatternCore
    │   └── test_*  (unit tests)
    ├── TestRealWorldExample
    │   └── test_*  (integration tests)
    └── TestEdgeCases
        └── test_*  (error handling)
```

### Test Execution Flow

```bash
# All tests
pytest

# Category
pytest creational/ -v

# Single pattern
pytest creational/singleton/test_pattern.py -v

# Specific test
pytest -k "test_singleton_creates_same_instance"

# With coverage
pytest --cov=. --cov-report=html
```

### Test Conventions

```python
# Naming
def test_description_of_what_is_tested(self):
    """What this test verifies."""
    pass

# Arrange-Act-Assert pattern
def test_something(self):
    # Arrange
    obj = MyClass()
    
    # Act
    result = obj.do_something()
    
    # Assert
    assert result == expected
```

---

## 📝 Code Style Standards

### Python Version

- **Minimum:** Python 3.9
- **Tested:** 3.9, 3.10, 3.11, 3.12

### Type Hints

```python
from typing import Optional, List, Dict, Any, Union

def process(items: List[str], count: int = 10) -> Dict[str, Any]:
    """Type hints throughout."""
    pass
```

### Formatting

- **Line Length:** 100 characters (black default)
- **Indentation:** 4 spaces
- **Quotes:** Double quotes for strings
- **Imports:** Organized by standard → third-party → local

### Tools Used

| Tool | Purpose | Config |
|------|---------|--------|
| black | Code formatting | pyproject.toml |
| isort | Import sorting | pyproject.toml |
| flake8 | Linting | .flake8 |
| mypy | Type checking | pyproject.toml |
| pytest | Testing | pyproject.toml |

---

## 🔍 Documentation Standards

### Docstring Format

```python
def function(param: str) -> str:
    """
    Short description (one line).
    
    Longer description if needed (multiple lines).
    Explain what it does, why, and how.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
        
    Example:
        >>> result = function("input")
        >>> print(result)
        expected_output
    """
```

### README Structure

See individual pattern READMEs for the complete structure, but follow this hierarchy:

1. Pattern name (H1)
2. Badges and quick links
3. Intent section
4. Problem section
5. Solution section
6. Key Components
7. Advantages and Disadvantages
8. Real-World Applications
9. When to Use / When Not to Use
10. Related Patterns

---

## 🚀 Module Initialization

### How to Import

**Option 1: Direct import**
```python
from creational.singleton import Singleton
```

**Option 2: From module**
```python
from creational import Singleton
```

**Option 3: Complete module**
```python
from creational import singleton
instance = singleton.Singleton()
```

All work because `__init__.py` files properly export classes.

---

## 📊 Metrics and Coverage

### Code Coverage Goals

- **Core Patterns:** 95%+ coverage
- **Real-World Examples:** 90%+ coverage
- **Edge Cases:** Comprehensive

### Performance Metrics

- No pattern should significantly impact performance
- Flyweight pattern should reduce memory usage
- Proxy pattern overhead should be minimal

---

## 🔗 Patterns Relationships

### Fundamental Patterns

These patterns are building blocks for others:

```
Factory Method ──→ Abstract Factory
                └──→ Builder
                └──→ Singleton (often used with)

Observer ──────────→ Mediator (alternative)
                └──→ Command (with queuing)

Strategy ──────────→ State (similar structure)
```

### Frequent Combinations

```
Composite + Decorator  (enhance tree nodes)
Facade + Proxy        (simplify and control)
Factory + Singleton   (single factory instance)
Observer + Mediator   (coordination patterns)
```

---

## 📚 Documentation Hierarchy

```
README.md (project overview)
  ↓
docs/GETTING_STARTED.md (setup)
  ↓
creational/README.md (category overview)
  ↓
creational/singleton/README.md (pattern deep dive)
  ↓
creational/singleton/pattern.py (implementation)
```

---

## 🤝 Contributor Architecture

### Where Contributions Go

| Contribution Type | Target | Process |
|-------------------|--------|---------|
| New Pattern | new directory | See CONTRIBUTING.md |
| Pattern Enhancement | existing pattern | Fork → PR |
| Bug Fix | any file | Report issue → PR |
| Documentation | any .md | Direct contribution |
| Examples | real_world_example.py | Enhance existing |
| Tests | test_pattern.py | Improve coverage |

---

## 📈 Future Architecture Considerations

### Planned Extensions

- [ ] Architectural patterns (MVC, MVVM, etc.)
- [ ] Async pattern variants
- [ ] Performance optimization examples
- [ ] Integration with popular frameworks
- [ ] Anti-patterns with corrections

### Scalability

- Current structure supports 50+ patterns
- Each pattern is self-contained
- Categories can be extended
- No monolithic dependencies

---

## 🧠 Design Principles

### Followed Throughout

1. **SOLID Principles**
   - Single Responsibility - each class has one role
   - Open/Closed - open for extension, closed for modification
   - Liskov Substitution - subtypes are substitutable
   - Interface Segregation - many client-specific interfaces
   - Dependency Inversion - depend on abstractions

2. **DRY (Don't Repeat Yourself)**
   - Common patterns extracted
   - Shared documentation structure

3. **KISS (Keep It Simple, Stupid)**
   - Minimal, clear implementations
   - No unnecessary complexity
   - Readable over clever

4. **Clean Code**
   - Self-documenting code
   - Meaningful names
   - Short, focused functions

---

**This architecture ensures consistency, maintainability, and quality across all patterns.**
