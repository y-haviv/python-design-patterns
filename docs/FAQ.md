# Frequently Asked Questions (FAQ)

Got questions? You're not alone! Here are answers to common questions about design patterns and this repository.

---

## General Questions

### Q: What is a design pattern?
**A:** A design pattern is a reusable solution to a common programming problem. It's a template or guide that shows how to solve a problem in a proven way. Think of it like architectural blueprints for buildings—the same patterns are used repeatedly because they work well.

### Q: Why should I learn design patterns?
**A:** Learning design patterns helps you:
- Write cleaner, more maintainable code
- Communicate better with other developers
- Solve problems faster
- Avoid common mistakes
- Understand how popular frameworks work
- Excel in technical interviews

### Q: How many design patterns should I know?
**A:** Start with 5-10 fundamental patterns (Singleton, Observer, Strategy, Factory Method, Adapter). As you progress, learn more specialized patterns. You don't need to memorize all 21—what matters is knowing where to look when you need one.

### Q: What's the difference between design patterns and anti-patterns?
**A:** 
- **Design Patterns** - Proven solutions to common problems
- **Anti-patterns** - Common mistakes to avoid

For example, Singleton is a design pattern, but a Singleton that's misused can become an anti-pattern.

### Q: Can I use design patterns in production code?
**A:** Absolutely! These are production-ready implementations. Design patterns are used in:
- Django, Flask, FastAPI (web frameworks)
- numpy, pandas, scikit-learn (data science)
- All major software projects

### Q: Are design patterns language-specific?
**A:** No! Patterns exist in all programming languages. This repository focuses on Python, but the concepts apply everywhere. Patterns like Singleton and Observer work the same in Java, C++, C#, JavaScript, etc.

---

## Learning Questions

### Q: Which pattern should I learn first?
**A:** Start in this order:
1. **Singleton** - Simplest, understand object instantiation
2. **Factory Method** - Common and practical
3. **Observer** - Powerful for event systems
4. **Strategy** - Simple but powerful for algorithms

### Q: How long does it take to learn all patterns?
**A:** This varies by background:
- **Beginners:** 20-40 hours for solid understanding
- **Intermediate:** 10-20 hours to fill gaps
- **Advanced:** 5-10 hours to review and deep-dive

### Q: Are there prerequisites for learning patterns?
**A:** You should be comfortable with:
- Python basics (classes, inheritance)
- Object-oriented programming concepts
- Basic problem-solving

You don't need to know all patterns—they build on each other.

### Q: What if I don't understand a pattern?
**A:** Try this approach:
1. Read the README - understand the concept
2. Study pattern.py - see the code
3. Check real_world_example.py - see practical usage
4. Run test_pattern.py - execute and experiment
5. Modify the code - change parameters, see what breaks
6. Apply to your code - implement it yourself

Still stuck? [Open a discussion](https://github.com/y-haviv/python-design-patterns/discussions)!

### Q: Should I memorize the patterns?
**A:** No! Understanding is better than memorization. You should know:
- The general idea of each pattern
- When to use it
- Where to find implementation details

### Q: How do I practice design patterns?
**A:** 
1. Read pattern documentation
2. Study the implementation
3. Implement it in a small project
4. Refactor existing code to use the pattern
5. Explain it to someone else
6. Use it in a real project

---

## Usage Questions

### Q: How do I import a pattern?
**A:** Multiple ways work:

```python
# Method 1: Direct import
from creational.singleton import Singleton

# Method 2: From module
from creational import Singleton

# Method 3: Full path
import creational.singleton
obj = creational.singleton.Singleton()
```

### Q: Can I modify the patterns?
**A:** Yes! Feel free to:
- Adapt patterns to your needs
- Add features
- Optimize for your use case
- Combine patterns

But keep the core concept for clarity.

### Q: Which pattern should I use for my problem?
**A:** See [PATTERNS_OVERVIEW.md](PATTERNS_OVERVIEW.md) for pattern selection guide. If unsure:
1. Check "When to Use" section in pattern README
2. Look at real_world_example.py
3. Compare with similar patterns
4. Try it and see if it works

### Q: Can I use multiple patterns together?
**A:** Yes! Patterns often work together:
- Composite + Decorator (enhance tree nodes)
- Facade + Proxy (simplify and control)
- Factory + Singleton (single factory)
- Observer + Mediator (event systems)

### Q: Do patterns make code more complex?
**A:** Short answer: sometimes. Patterns can add complexity if overused. Use them when:
- Problem is complex enough to warrant it
- Multiple developers need clear structure
- Code needs to be extensible
- Team understands the pattern

Don't use patterns for simple problems.

### Q: Performance impact of patterns?
**A:** Most patterns have negligible performance impact. Some considerations:
- **Flyweight** - Reduces memory significantly
- **Proxy** - Can improve performance (caching)
- **Composite** - Overhead depends on tree depth
- **Decorator** - Small overhead per wrapper

See pattern README for specifics.

---

## Project Questions

### Q: How is this project organized?
**A:** 
```
python-design-patterns/
├── creational/  (5 patterns)
├── structural/  (7 patterns)
├── behavioral/  (8 patterns)
├── docs/       (documentation)
└── [config and license files]
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed structure.

### Q: What Python version is required?
**A:** Python 3.9 or higher. Install from [python.org](https://python.org).

### Q: Can I use this in my project?
**A:** Absolutely! It's licensed under MIT, which allows:
- ✓ Commercial use
- ✓ Modification  
- ✓ Distribution
- ✓ Private use
- ✓ Just include attribution

### Q: How do I contribute?
**A:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines. Quick summary:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Q: What's the code quality standard?
**A:** All code follows:
- PEP 8 style guide
- Type hints throughout
- 95%+ test coverage
- Comprehensive documentation
- Black formatting
- isort import sorting

---

## Troubleshooting

### Q: Why am I getting import errors?
**A:** Check your imports:
```python
# ❌ Wrong - pattern module doesn't exist like this
from pattern import Singleton

# ✓ Correct
from creational.singleton import Singleton
```

### Q: Why are tests failing?
**A:** 
1. Run from project root: `pytest`
2. Check Python version: `python --version` (need 3.9+)
3. Install dependencies: `pip install -r requirements.txt`
4. Check for typos in code

### Q: Why is code slow?
**A:** 
1. Most patterns don't cause slowness
2. Check for N+1 queries (database)
3. Consider Flyweight if memory-heavy
4. Use Proxy for caching
5. Profile before optimizing

### Q: Why are my tests not running?
**A:**
```bash
# Run from project root
cd python-design-patterns

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest -v
```

### Q: Why do I see duplicate classes in different patterns?
**A:** This is intentional! Each pattern is self-contained with examples like `Component`, `Adapter`, etc. This makes each pattern independently understandable.

---

## Advanced Questions

### Q: How do design patterns relate to SOLID principles?
**A:** Patterns help you follow SOLID:
- **S**ingle Responsibility - Bridge, Facade
- **O**pen/Closed - Strategy, Decorator
- **L**iskov Substitution - Factory Method, Adapter
- **I**nterface Segregation - Adapter
- **D**ependency Inversion - Factory Method, Observer

### Q: Can patterns be anti-patterns?
**A:** Yes! When overused or misapplied:
- Singleton can hide global state
- Observer can create spammy notifications
- Decorator can create deeply nested objects
- Use patterns appropriately, not everywhere

### Q: How do patterns relate to architectural patterns?
**A:** These are GoF patterns (structural/behavioral/creational).

Architectural patterns include:
- MVC, MVP, MVVM
- Horizontal vs vertical slicing
- Microservices
- These are related but different scope

### Q: How do I combine patterns?
**A:** 
1. Identify the problems each solves
2. Ensure they don't conflict
3. Implement one at a time
4. Test integration
5. Document the combination

Example: Factory + Singleton
```python
# Singleton factory
class SingletonFactory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Getting Help

### Q: Where can I ask questions?
**A:** Several options:
- 📖 [Getting Started Guide](GETTING_STARTED.md)
- 📚 [Documentation](../README.md)
- 💬 [GitHub Discussions](https://github.com/y-haviv/python-design-patterns/discussions)
- 🐛 [Issue Tracker](https://github.com/y-haviv/python-design-patterns/issues)

### Q: How do I report a bug?
**A:** [Open an issue](https://github.com/y-haviv/python-design-patterns/issues) with:
- Clear title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS

### Q: How do I suggest improvements?
**A:** 
- [Open a discussion](https://github.com/y-haviv/python-design-patterns/discussions)
- Explain the suggestion
- Why it would be helpful
- Implementation ideas (if you have them)

### Q: Can I contribute examples?
**A:** Yes! We welcome:
- Better explanations
- Additional real-world examples
- Code optimization
- Test improvements
- Documentation fixes

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

**Still have questions? [Start a discussion!](https://github.com/y-haviv/python-design-patterns/discussions)**
