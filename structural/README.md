# Structural Design Patterns

> **Category:** Object composition and relationship structuring  
> **Focus:** Creating larger structures from individual objects and classes  
> **Pythonic Strategy:** Composition, Inheritance, and Abstraction

## Overview

Structural design patterns are concerned with how classes and objects are combined to form larger, more complex structures. They deal with object composition, creating relationships between entities to form new functionality. Rather than changing functionality, they simplify the structure.

This directory contains comprehensive implementations of 7 structural design patterns, each with:

- **pattern.py** - Core pattern implementation with abstract interfaces and concrete classes
- **real_world_example.py** - Practical, real-world use cases
- **test_pattern.py** - Comprehensive pytest test suites (200+ tests total)
- **README.md** - Documentation with design principles and comparisons

## Patterns Included

### 1. [Adapter](adapter/README.md) - Interface Compatibility

Convert the interface of a class into another interface clients expect, allowing incompatible interfaces to work together.

**Key Features:**
- Adapt incompatible interfaces to work seamlessly
- Reduce coupling between different subsystems
- Support for bidirectional adaptation
- Dynamic adapter registration and lookup
- Example: Payment gateway adapters (Stripe/PayPal), legacy system integration

**Use When:** You need to integrate classes with incompatible interfaces, or provide a unified interface for multiple implementations.

---

### 2. [Bridge](bridge/README.md) - Abstraction Separation

Decouple an abstraction from its implementation so the two can vary independently.

**Key Features:**
- Separate abstraction from implementation
- Enable independent variation of both dimensions
- Avoid permanent binding through inheritance
- Support for multiple implementations per abstraction
- Example: Remote controls with multiple communication protocols (WiFi, Bluetooth, Infrared)

**Use When:** You need to avoid permanent abstraction-implementation binding, or to prevent excessive class hierarchies.

---

### 3. [Composite](composite/README.md) - Tree Composition

Compose objects into tree structures to represent part-whole hierarchies, letting clients treat individual objects and compositions uniformly.

**Key Features:**
- Recursive object composition for tree structures
- Treat individual and composite objects uniformly
- Build complex trees from simple components
- Traverse and manipulate hierarchies easily
- Example: File systems (files/directories), organization charts (employees/departments), document structures

**Use When:** You need to represent hierarchical structures, or to let clients work with individual and composite objects identically.

---

### 4. [Decorator](decorator/README.md) - Dynamic Enhancement

Attach additional responsibilities to an object dynamically, providing a flexible alternative to subclassing.

**Key Features:**
- Add responsibilities dynamically without modifying objects
- Avoid tedious subclassing for behavior combinations
- Multiple decorators can be stacked
- Transparent wrapping of objects
- Example: Stream enhancements (compression, encryption, buffering), UI component decoration (borders, scrollbars, shadows)

**Use When:** You need to extend object functionality dynamically, or when subclassing creates too many classes.

---

### 5. [Facade](facade/README.md) - Interface Simplification

Provide a unified, simplified interface to a set of interfaces in a subsystem, making it easier to use.

**Key Features:**
- Hide complex subsystem details behind simple interface
- Decouple clients from subsystem components
- Reduce dependencies and improve maintainability
- Provide single entry point for related functionality
- Example: Computer startup sequence, order processing system, database repository management

**Use When:** You need to provide a simple interface to a complex subsystem, or to decouple clients from complex components.

---

### 6. [Flyweight](flyweight/README.md) - Object Sharing

Use sharing to support large numbers of fine-grained objects efficiently when simple repeated representation would use unacceptable amounts of memory.

**Key Features:**
- Share common state (intrinsic) across many objects
- Minimize memory usage through object pooling
- Separate intrinsic from extrinsic state
- Factory manages shared flyweight instances
- Example: Text rendering (shared font objects), particle systems, tree forests, image caching

**Use When:** You have many similar objects consuming excessive memory, or need efficient object pooling.

---

### 7. [Proxy](proxy/README.md) - Access Control

Provide a surrogate or placeholder for another object to control access to it.

**Key Features:**
- Control access to real objects through surrogates
- Lazy initialization of expensive objects
- Add operations before/after accessing real object
- Support for protection, caching, logging, and validation
- Example: Image lazy loading, database query caching, remote service access with request caching

**Use When:** You need to control or intercept access to objects, lazy-load expensive resources, or add cross-cutting concerns.

---

## Quick Comparison Matrix

| Pattern | Problem | Solution | Complexity |
|---------|---------|----------|------------|
| **Adapter** | Incompatible interfaces | Create compatible wrapper | Medium |
| **Bridge** | Coupled abstraction-implementation | Separate concerns | Medium |
| **Composite** | Part-whole hierarchies | Treat uniformly | Medium |
| **Decorator** | Multiple behavior combinations | Dynamic enhancement | Medium |
| **Facade** | Complex subsystem | Simplified interface | Low |
| **Flyweight** | Too many objects / memory | Share common state | High |
| **Proxy** | Need access control/interception | Surrogate object | Medium |

---

## Getting Started

### Basic Usage Pattern

Each pattern follows a consistent structure:

```python
# Import from the pattern module
from structural.adapter import Adapter, Target
from structural.bridge import Abstraction, Implementor
from structural.composite import Component, Leaf, Composite
from structural.decorator import Decorator, Component as DecoratorComponent
from structural.facade import Facade
from structural.flyweight import Flyweight, FlyweightFactory
from structural.proxy import Subject, Proxy

# Or import everything
from structural import *
```

### Understanding the Examples

Each pattern directory includes:

1. **pattern.py** - Theoretical implementation showing the core pattern
2. **real_world_example.py** - Practical example demonstrating real-world usage
3. **test_pattern.py** - Comprehensive test suite with multiple scenarios

### Running Tests

```bash
# Test a specific pattern
pytest structural/adapter/test_pattern.py -v

# Test all structural patterns
pytest structural/ -v

# Run with coverage
pytest structural/ --cov=structural --cov-report=html
```

---

## Pattern Selection Guide

### Choose an Adapter when:
- Integrating third-party libraries with different interfaces
- Supporting multiple implementations of an interface
- Retrofitting new functionality into existing classes

### Choose a Bridge when:
- You want to avoid permanent binding between abstraction and implementation
- You have multiple independent dimensions of variation
- You need to share an implementation among multiple objects

### Choose a Composite when:
- You need to represent hierarchical structures
- You want clients to treat individual and composite objects identically
- Building file systems, organization charts, GUI hierarchies, document structures

### Choose a Decorator when:
- You need to add responsibilities dynamically
- Subclassing would create too many classes
- You want to avoid modifying existing object implementations

### Choose a Facade when:
- You need to simplify a complex subsystem
- You want to provide entry points layered into a subsystem
- You need to reduce dependencies between clients and subsystems

### Choose a Flyweight when:
- You have many similar objects consuming excessive memory
- You need efficient object pooling and reuse
- Intrinsic state is stable and can be shared

### Choose a Proxy when:
- You need lazy initialization of expensive objects
- You need to control access to real objects
- You need to add logging, caching, or validation transparently

---

## Common Pitfalls

### Adapter
- ❌ Creating adapters for every minor interface difference (use composition instead)
- ✅ Reserve adapters for genuinely incompatible interfaces

### Bridge
- ❌ Using when abstraction-implementation binding is stable (unnecessary complexity)
- ✅ Use when you need independent variation in multiple dimensions

### Composite
- ❌ Overusing for list-like structures (simpler alternatives exist)
- ✅ Use when you need recursive composition with uniform interface

### Decorator
- ❌ Stacking too many decorators (becomes hard to understand)
- ✅ Keep decorator chains manageable and well-documented

### Facade
- ❌ Making facade do too much (should simplify, not orchestrate)
- ✅ Keep facade focused on providing simple interface to subsystem

### Flyweight
- ❌ Premature optimization (profile first!)
- ✅ Apply when you have evidence of memory problems

### Proxy
- ❌ Adding too much logic to proxy (defeats purpose of real object)
- ✅ Keep proxy focused on access control or lazy loading

---

## Related Patterns

These structural patterns often work together:

- **Adapter + Bridge:** Make incompatible bridges compatible
- **Composite + Decorator:** Decorate leaf and composite objects
- **Facade + Proxy:** Simplify access through facade, control via proxy
- **Decorator + Flyweight:** Decorate shared flyweights efficiently
- **Adapter + Factory:** Factories often adapt constructors

---

## Key Principles

### 1. Composition Over Inheritance

Structural patterns favor composition because:
- More flexible than inheritance hierarchies
- Can combine behaviors dynamically
- Easier to modify and extend

### 2. Separation of Concerns

Each pattern separates specific concerns:
- **Adapter:** Interface compatibility
- **Bridge:** Abstraction vs. implementation
- **Composite:** Part vs. whole
- **Decorator:** Core object vs. enhancement
- **Facade:** Complex system vs. simple interface
- **Flyweight:** Intrinsic vs. extrinsic state
- **Proxy:** Real object vs. access control

### 3. Preserving Original Semantics

All structural patterns preserve the semantics of the objects they manipulate—they change structure, not essential behavior.

---

## Performance Considerations

| Pattern | Time Impact | Space Impact | Notes |
|---------|-------------|--------------|-------|
| Adapter | Negligible | Minimal | Wrapper adds small overhead |
| Bridge | Negligible | Minimal | One extra indirection |
| Composite | Low | Varies | Recursive traversal cost |
| Decorator | Low | Linear | Wrapping stack adds slight overhead |
| Facade | Negligible | Minimal | Simple delegation |
| Flyweight | Negligible | Significant Savings | Reduces memory substantially |
| Proxy | Low | Minimal | Lazy loading saves initial space |

---

## Resources and Further Reading

### Design Pattern References
- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) - Gang of Four
- [Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/0596007124/) - Freeman & Freeman
- [Refactoring.Guru Design Patterns](https://refactoring.guru/design-patterns) - Interactive examples

### Python-Specific Resources
- [Python Design Patterns](https://python-patterns.guide/) - Comprehensive Python patterns
- [PEP 20 - The Zen of Python](https://www.python.org/dev/peps/pep-0020/) - Pythonic principles
- [Python ABC Module](https://docs.python.org/3/library/abc.html) - Abstract base classes

### Real-World Applications
- Most enterprise frameworks use all structural patterns
- Python standard library implements many patterns internally
- Web frameworks (Django, Flask) use structural patterns extensively

