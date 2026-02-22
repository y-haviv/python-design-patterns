# Python Design Patterns

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive, production-ready collection of Gang of Four (GoF) design patterns implemented in modern, idiomatic Python. This repository serves as a valuable resource for developers looking to understand, learn, and apply design patterns to build robust, scalable, and maintainable software.

Inspired by the highly-regarded [java-design-patterns](https://github.com/iluwatar/java-design-patterns) project, this repository aims to provide the Python community with a similarly high-quality educational tool, focusing on clarity and practical application.

---

## Project Philosophy

This project is built upon a set of core principles to ensure it is a high-quality, trustworthy resource for the Python community.

- **Clarity and Readability**: Code is written to be understood, not just to work. We prioritize clear variable names, simple logic, and comprehensive comments.
- **Pythonic Implementation**: Patterns are adapted to leverage Python's unique features (like decorators, context managers, and first-class functions), not just translated from other languages.
- **Production-Ready**: Implementations are robust, type-hinted, and suitable for real-world applications. Thread-safety and performance are considered where applicable.
- **Comprehensive Documentation**: Each pattern is thoroughly documented to explain its intent, structure, trade-offs, and real-world use cases.
- **Thorough Testing**: A full test suite with high coverage ensures correctness, reliability, and adherence to the pattern's principles.

---

## Quick Start

Get up and running in a few simple steps.

```bash
# 1. Clone the repository
git clone https://github.com/y-haviv/python-design-patterns.git
cd python-design-patterns

# 2. Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests to verify the setup
pytest
```

### Basic Usage

```python
# Import any pattern
from creational.singleton import Singleton
from structural.adapter import Adapter, Target
from behavioral.observer import Subject, Observer

# Use in your code
my_singleton = Singleton()
my_adapter = Adapter(adaptee)
my_subject = Subject()
my_subject.attach(my_observer)
```

### Learn a Pattern

Each pattern directory has a comprehensive `README.md`:

```bash
# Read about any pattern
cat creational/singleton/README.md
cat structural/adapter/README.md
cat behavioral/observer/README.md
```

---

## 📋 Complete Pattern List

### Creational Patterns (Object Creation)

1. **[Singleton](creational/singleton/)** - Single instance, global access
2. **[Factory Method](creational/factory/)** - Deferred instantiation
3. **[Abstract Factory](creational/abstract_factory/)** - Family of objects
4. **[Builder](creational/builder/)** - Complex object construction
5. **[Prototype](creational/prototype/)** - Clone existing objects

### Structural Patterns (Object Composition)

1. **[Adapter](structural/adapter/)** - Interface compatibility
2. **[Bridge](structural/bridge/)** - Abstraction-implementation separation
3. **[Composite](structural/composite/)** - Tree composition
4. **[Decorator](structural/decorator/)** - Dynamic enhancement
5. **[Facade](structural/facade/)** - Simplified interface
6. **[Flyweight](structural/flyweight/)** - Object sharing
7. **[Proxy](structural/proxy/)** - Access control

### Behavioral Patterns (Object Interaction)

1. **[Command](behavioral/command/)** - Request encapsulation
2. **[Iterator](behavioral/iterator/)** - Sequential access
3. **[Mediator](behavioral/mediator/)** - Centralized communication
4. **[Memento](behavioral/memento/)** - State preservation
5. **[Observer](behavioral/observer/)** - One-to-many notification
6. **[State](behavioral/state/)** - State-dependent behavior
7. **[Strategy](behavioral/strategy/)** - Algorithm encapsulation
8. **[Visitor](behavioral/visitor/)** - Object tree traversal

---

## 🎓 Learning Path

### For Beginners
1. Start with [Singleton](creational/singleton/) - simplest pattern
2. Move to [Factory Method](creational/factory/) - common foundation
3. Try [Observer](behavioral/observer/) - practical and powerful
4. Learn [Decorator](structural/decorator/) - shows composition benefits

### For Intermediate
1. Study [Strategy](behavioral/strategy/) - runtime algorithm selection
2. Master [Composite](structural/composite/) - tree structures
3. Explore [Adapter](structural/adapter/) - integration problems
4. Understand [Bridge](structural/bridge/) - abstraction separation

### For Advanced
1. Deep dive [Memento](behavioral/memento/) - state management complexity
2. Implement [Mediator](behavioral/mediator/) - coordination patterns
3. Use [Visitor](behavioral/visitor/) - advanced traversal
4. Optimize with [Flyweight](structural/flyweight/) - memory efficiency

---

## 💡 Real-World Applications

These patterns are used everywhere:

- **Web Frameworks:** Django, Flask, FastAPI
- **Data Processing:** pandas, NumPy, scikit-learn
- **Testing Frameworks:** pytest, unittest, Mock
- **Databases:** SQLAlchemy, tortoise-orm
- **Async Libraries:** asyncio, aiohttp

See specific implementations for real use cases!

---

## 📈 Code Quality

### Standards Followed

```python
# Type hints
def process_data(items: List[str], count: int) -> Dict[str, Any]:
    ...

# Comprehensive docstrings
def method(param: str) -> None:
    """
    Do something helpful.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is invalid
    """
    pass

# Clean, readable code
name = TypedName("valid_identifier")
factory = PatternFactory()
result = factory.create(config)
```

### Test Coverage

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# All patterns have:
# - Unit tests (100% coverage)
# - Integration tests (real-world scenarios)
# - Edge case tests (error handling)
# - Performance tests (optimization checks)
```

---

## 🤝 Contributing

This is an open-source project

### Ways to Contribute

1. **Fix bugs** - Found an issue? Open a PR!
2. **Improve documentation** - Clearer explanations help everyone
3. **Add examples** - Show real-world usage
4. **Optimize performance** - Make pattern implementations faster
5. **Add tests** - Better coverage = better code

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📚 Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Setup and first steps
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Project structure
- **[Development Guide](docs/DEVELOPMENT.md)** - How to contribute
- **[Patterns Overview](docs/PATTERNS_OVERVIEW.md)** - Deep dive comparison
- **[FAQ](docs/FAQ.md)** - Common questions answered

---

## 📋 Requirements

- **Python:** 3.9 or higher
- **Dependencies:** None (core library) - see optionals in requirements.txt
- **Testing:** pytest

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

### Why MIT?

The MIT License is ideal for educational projects because it:
- Allows commercial use
- Permits modification and distribution
- Requires only attribution
- Is simple and permissive

---

## 📞 Support

### Questions or Issues?

- 📖 Check the [FAQ](docs/FAQ.md)
- 🐛 [Report a bug](https://github.com/y-haviv/python-design-patterns/issues)
- 💬 [Start a discussion](https://github.com/y-haviv/python-design-patterns/discussions)

---

## 🙏 Acknowledgments

- **Gang of Four** - Original design patterns from their seminal work
- **java-design-patterns** - Inspiration for this project structure
- **Python Community** - For the amazing ecosystem

---

## 🗺️ Roadmap

- [ ] Pattern implementation guides (video tutorials)
- [ ] Interactive pattern browser (web app)
- [ ] Design patterns converter (e.g., Java → Python)
- [ ] Performance benchmarks dashboard
- [ ] Anti-patterns examples and solutions
- [ ] Design pattern quiz/assessment tool

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| **Total Patterns** | 21 |
| **Implementation Files** | 84+ |
| **Test Cases** | 200+ |
| **Code Examples** | 50+ |
| **Documentation** | 5,000+ lines |
| **Test Coverage** | ~95% |

---

## 🌟 How to Get the Most Value

1. **Clone the repo** - `git clone ...`
2. **Read a pattern README** - Understand the concept
3. **Study pattern.py** - Learn the implementation
4. **Check real_world_example.py** - See practical usage
5. **Run and modify tests** - Experiment and learn
6. **Apply to your project** - Use what you learned

---

**Ready to master design patterns?** Start with [Singleton](creational/singleton/README.md)!

---

<div align="center">

⭐ If you find this helpful, please give it a star!

[Report Bug](https://github.com/y-haviv/python-design-patterns/issues) • [Request Feature](https://github.com/y-haviv/python-design-patterns/issues) • [Contribute](CONTRIBUTING.md)

</div>
