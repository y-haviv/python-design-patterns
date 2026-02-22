# Bridge Pattern (Structural)

> **Architectural Level:** Object Structure  
> **Pythonic Strategy:** Composition Over Inheritance  
> **Production Status:** Mission Critical | Architecture Pattern | Best Practice

---

## Also Known As

- Handle / Body

---

## Intent

Decouple an abstraction from its implementation so that the two can vary independently.

The Bridge pattern separates a system into two independent hierarchies:

- The **Abstraction**, which defines the high-level control logic
- The **Implementation**, which provides the low-level operational behavior

This separation improves flexibility, extensibility, and maintainability.

---

## Problem

When a class must support multiple independent dimensions of variation, inheritance alone leads to combinatorial class explosion, tight coupling, and duplication.

### Common Issues

- **Class Explosion**  
  Supporting multiple abstractions and implementations leads to exponential growth in subclasses.

- **Rigid Hierarchies**  
  Changes in implementation force changes in abstraction.

- **Code Duplication**  
  Similar logic appears across multiple subclasses.

- **Violation of Single Responsibility Principle**  
  Classes must change for both abstraction and implementation reasons.

### Illustration

Without Bridge:

```

RefinedAbstraction1ImplA
RefinedAbstraction1ImplB
RefinedAbstraction2ImplA
RefinedAbstraction2ImplB

```

With Bridge:

```

Abstraction Hierarchy:

* RefinedAbstraction1
* RefinedAbstraction2

Implementation Hierarchy:

* ConcreteImplementorA
* ConcreteImplementorB

```

The hierarchies evolve independently.

---

## Solution

The Bridge pattern separates abstraction and implementation using composition.

The abstraction contains a reference to an implementation object and delegates work to it.

### Key Components

| Component | Description |
|---|---|
| Abstraction | Defines high-level interface |
| RefinedAbstraction | Extends abstraction |
| Implementor | Defines implementation interface |
| ConcreteImplementor | Provides implementation |

---

## Structure

```

Abstraction
|
| references
v
Implementor

RefinedAbstraction      ConcreteImplementorA
RefinedAbstraction      ConcreteImplementorB

````

---

## Implementation Variants

### Classic Bridge Pattern

Separates abstraction and implementation using composition.

```python
from abc import ABC, abstractmethod


class DrawingAPI(ABC):

    @abstractmethod
    def draw_circle(self):
        pass


class CanvasAPI(DrawingAPI):

    def draw_circle(self):
        return "Drawing circle on Canvas"


class SVGAPI(DrawingAPI):

    def draw_circle(self):
        return "<circle />"


class Shape(ABC):

    def __init__(self, api: DrawingAPI):
        self.api = api

    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):

    def draw(self):
        return self.api.draw_circle()
````

---

### Runtime Implementation Switching

The implementation can be replaced dynamically.

```python
shape = Circle(CanvasAPI())
shape.draw()

shape.api = SVGAPI()
shape.draw()
```

---

### Default Implementation

Provide default implementation when flexibility is not required.

```python
class DefaultDrawingAPI(DrawingAPI):

    def draw_circle(self):
        return "Default drawing"


class Shape:

    def __init__(self, api: DrawingAPI = DefaultDrawingAPI()):
        self.api = api
```

---

## Implementation Guidelines

### When to Use

Use the Bridge pattern when:

* There are multiple independent dimensions of variation
* Class hierarchy is growing excessively
* Implementation should be replaceable at runtime
* Abstraction and implementation must evolve independently
* You want to avoid permanent binding between abstraction and implementation

### When to Avoid

Avoid the Bridge pattern when:

* Only one dimension of variation exists
* Abstraction and implementation are tightly coupled
* Complexity outweighs flexibility benefits

---

## Implementation Steps

```python
# Implementor interface
class DrawingAPI(ABC):

    @abstractmethod
    def draw_circle(self):
        pass


# Concrete Implementors
class CanvasAPI(DrawingAPI):

    def draw_circle(self):
        return "Canvas circle"


class SVGAPI(DrawingAPI):

    def draw_circle(self):
        return "SVG circle"


# Abstraction
class Shape(ABC):

    def __init__(self, api: DrawingAPI):
        self.api = api

    @abstractmethod
    def draw(self):
        pass


# Refined Abstraction
class Circle(Shape):

    def draw(self):
        return self.api.draw_circle()


# Usage
circle1 = Circle(CanvasAPI())
circle2 = Circle(SVGAPI())
```

---

## Advantages and Disadvantages

### Advantages

* Decouples abstraction from implementation
* Enables independent extensibility
* Reduces class explosion
* Improves maintainability
* Supports runtime implementation switching
* Promotes reuse

### Disadvantages

* Increases architectural complexity
* Introduces additional abstraction layers
* May be unnecessary for simple systems

---

## Real-World Applications

### UI Frameworks

Different UI implementations behind unified interface:

```python
class Window:

    def __init__(self, toolkit):
        self.toolkit = toolkit

    def render(self):
        return self.toolkit.create_window()
```

---

### Payment Processing

Payment types independent of providers:

```python
class Payment:

    def __init__(self, provider):
        self.provider = provider

    def process(self, amount):
        return self.provider.charge(amount)
```

---

### Database Abstraction

Repositories independent of database engine:

```python
class Repository:

    def __init__(self, database):
        self.database = database

    def find(self, id):
        return self.database.query(id)
```

---

### Device Control Systems

Control logic independent of communication protocol:

```python
class Remote:

    def __init__(self, protocol):
        self.protocol = protocol

    def power_on(self):
        return self.protocol.send("power_on")
```

---

## Comparison with Related Patterns

| Pattern         | Purpose                          | Difference                     |
| --------------- | -------------------------------- | ------------------------------ |
| Adapter         | Converts incompatible interfaces | Works with existing code       |
| Decorator       | Adds responsibilities            | Focuses on behavior extension  |
| Strategy        | Selects algorithms               | Focuses on algorithm variation |
| Template Method | Defines algorithm structure      | Uses inheritance               |

---

## Common Pitfalls

### Unnecessary Use

Avoid Bridge when simpler solutions exist.

### Incorrect Separation

Ensure abstraction and implementation are truly independent.

### Exposing Implementation Details

Abstraction should not reveal implementation internals.

---

## Best Practices

### Recommended

* Clearly define abstraction and implementation boundaries
* Prefer composition over inheritance
* Keep implementation encapsulated
* Document variation dimensions
* Provide clear abstraction interfaces

### Avoid

* Mixing abstraction and implementation logic
* Exposing implementation details
* Over-engineering simple designs
* Creating unnecessary hierarchies

---

## Standard Library Example

Python's file I/O system separates abstraction and implementation:

```python
with open("file.txt", "r") as file:
    data = file.read()
```

The file object represents abstraction, while buffering and encoding represent implementation.

---

## Summary

The Bridge pattern separates abstraction from implementation to allow independent variation.

It is especially useful when:

* Multiple independent dimensions exist
* Flexibility and extensibility are required
* System complexity must remain manageable

**Key Principle**

Favor composition to separate abstraction and implementation, allowing both to evolve independently.

