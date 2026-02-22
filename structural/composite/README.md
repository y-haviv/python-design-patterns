# Composite Pattern (Structural)

> **Architectural Level:** Object Structure  
> **Pythonic Strategy:** Recursive Composition  
> **Production Status:** Widely Used | Tree Structures | File Systems

---

## Also Known As

- Part–Whole

---

## Intent

Compose objects into tree structures to represent part–whole hierarchies, allowing clients to treat individual objects and compositions of objects uniformly.

The Composite pattern enables recursive composition, making it possible to build complex hierarchical structures while maintaining a consistent interface for all elements.

---

## Problem

Many systems must represent hierarchical relationships where objects can contain other objects, forming tree-like structures.

### Common Challenges

- **Hierarchical Structures**  
  Objects may contain other objects, which may themselves contain additional objects.

- **Uniform Processing**  
  Clients should not need to distinguish between individual objects and groups of objects.

- **Recursive Behavior**  
  Operations must be applied recursively across the entire structure.

- **Encapsulation of Structure**  
  Clients should not need to understand internal hierarchy details.

### Typical Scenarios

- File systems with files and directories
- GUI systems with nested components
- Organizational hierarchies
- Document object models
- Scene graphs in game development

---

## Solution

The Composite pattern defines a common interface for both individual objects and object collections.

This allows clients to treat both cases uniformly.

### Key Components

| Component | Description |
|---|---|
| Component | Abstract interface for all elements |
| Leaf | Represents individual objects |
| Composite | Represents objects that contain children |
| Client | Uses the Component interface |

---

## Structure

```

Component
│
├── Leaf
│
└── Composite
│
├── Leaf
└── Composite

````

The structure forms a recursive tree.

---

## Implementation Variants

### Safe Composite

Child-management methods are only available in Composite.

```python
from abc import ABC, abstractmethod


class Component(ABC):

    @abstractmethod
    def operation(self):
        pass

    def add(self, component: "Component"):
        raise NotImplementedError()

    def remove(self, component: "Component"):
        raise NotImplementedError()


class Composite(Component):

    def __init__(self):
        self.children = []

    def operation(self):
        return [child.operation() for child in self.children]

    def add(self, component: Component):
        self.children.append(component)

    def remove(self, component: Component):
        self.children.remove(component)
````

---

### Transparent Composite

Child-management methods exist in all classes but may do nothing in Leaf.

```python
class Component(ABC):

    def add(self, component: "Component"):
        pass

    def remove(self, component: "Component"):
        pass
```

---

### Extended Composite

Additional helper methods provide structural information.

```python
class Composite(Component):

    def is_leaf(self):
        return False

    def get_child_count(self):
        return len(self.children)
```

---

## Implementation Guidelines

### When to Use

Use the Composite pattern when:

* Objects form hierarchical tree structures
* Clients should treat individual and grouped objects uniformly
* Recursive processing is required
* The system represents part–whole relationships
* New component types must be added without changing client code

### When to Avoid

Avoid using the Composite pattern when:

* The structure is flat
* Strict type separation is required
* Performance constraints prohibit recursion
* The hierarchy adds unnecessary complexity

---

## Implementation Steps

```python
from abc import ABC, abstractmethod


class Component(ABC):

    @abstractmethod
    def operation(self):
        pass

    def add(self, component: "Component"):
        pass

    def remove(self, component: "Component"):
        pass


class Leaf(Component):

    def operation(self):
        return "Leaf"


class Composite(Component):

    def __init__(self):
        self.children = []

    def operation(self):
        results = []
        for child in self.children:
            results.append(child.operation())
        return results

    def add(self, component: Component):
        self.children.append(component)

    def remove(self, component: Component):
        self.children.remove(component)


def process(component: Component):
    return component.operation()
```

---

## Advantages and Disadvantages

### Advantages

* Uniform interface for all objects
* Simplifies client code
* Supports recursive structures naturally
* Easy to extend
* Flexible hierarchy construction

### Disadvantages

* May reduce type safety
* Can introduce performance overhead in deep hierarchies
* May increase memory usage
* Can be unnecessarily complex for simple structures

---

## Real-World Applications

### File System

```python
class FileSystemItem(ABC):

    @abstractmethod
    def get_size(self):
        pass


class File(FileSystemItem):

    def get_size(self):
        return self.size


class Directory(FileSystemItem):

    def __init__(self):
        self.items = []

    def get_size(self):
        return sum(item.get_size() for item in self.items)
```

---

### GUI Systems

```python
class Widget(ABC):

    @abstractmethod
    def render(self):
        pass


class Button(Widget):

    def render(self):
        return "Button"


class Panel(Widget):

    def __init__(self):
        self.children = []

    def render(self):
        return [child.render() for child in self.children]
```

---

### Organizational Structure

```python
class Employee(ABC):

    @abstractmethod
    def get_salary(self):
        pass


class Individual(Employee):

    def get_salary(self):
        return self.salary


class Department(Employee):

    def __init__(self):
        self.members = []

    def get_salary(self):
        return sum(member.get_salary() for member in self.members)
```

---

### Document Object Model

```python
class Element(ABC):

    @abstractmethod
    def render(self):
        pass


class Text(Element):

    def render(self):
        return self.content


class Container(Element):

    def __init__(self):
        self.children = []

    def render(self):
        return "".join(child.render() for child in self.children)
```

---

## Comparison with Related Patterns

| Pattern     | Purpose                             | Key Difference                  |
| ----------- | ----------------------------------- | ------------------------------- |
| Decorator   | Adds behavior to objects            | Focuses on behavior enhancement |
| Visitor     | Separates operations from structure | Focuses on operations           |
| Interpreter | Represents language grammar         | Focuses on expressions          |
| Proxy       | Controls access                     | Focuses on access control       |

---

## Common Pitfalls

### Excessive Type Checking

Client code should rely on abstraction, not concrete types.

### Overloaded Responsibilities

Components should focus only on structural responsibilities.

### Immutable Structures Without Justification

Allow modification unless immutability is explicitly required.

---

## Best Practices

### Recommended

* Keep the component interface minimal
* Maintain consistent behavior across components
* Encapsulate hierarchy structure
* Document structural assumptions clearly
* Consider performance implications

### Avoid

* Exposing implementation details
* Mixing unrelated responsibilities
* Creating unnecessary hierarchy levels
* Overusing the pattern

---

## Standard Library Example

Python's Abstract Syntax Tree uses the Composite pattern:

```python
import ast

tree = ast.parse("x = 1 + 2")
```

Each node represents part of a recursive structure.

---

## Summary

The Composite pattern allows hierarchical object composition while maintaining a uniform interface.

It is especially useful when:

* Representing tree structures
* Applying recursive operations
* Simplifying client interaction
* Modeling part–whole relationships

**Key Principle**

Represent part–whole hierarchies using recursive composition so clients can treat individual objects and object groups uniformly.

