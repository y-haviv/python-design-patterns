# Flyweight Pattern (Structural)

> **Architectural Level:** Memory Optimization  
> **Pythonic Strategy:** Object Pooling & Factory  
> **Production Status:** Performance Critical | Large-Scale Systems

---

## Intent

The Flyweight pattern uses sharing to support large numbers of fine-grained objects efficiently. It minimizes memory usage by separating intrinsic (shared) state from extrinsic (unique) state, allowing objects with similar data to share resources.

---

## Problem

Working with a very large number of similar objects can cause:

- Memory exhaustion when creating millions of objects  
- Performance degradation due to garbage collection overhead  
- Reduced rendering or simulation performance in games or visualizations  

**Example: Forest with 1 million trees**

```

Without Flyweight: 1M trees × (100KB texture) = 100GB
With Flyweight: 10 tree types × (100KB) + 1M positions = 1MB

````

---

## Solution

Separate intrinsic (shared) state from extrinsic (unique) state. Use a factory to manage shared instances.

### Example

```python
class TreeType:  # Intrinsic: shared, expensive
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture  # Expensive to load

class Tree:  # Extrinsic: unique per instance
    def __init__(self, x, y, tree_type: TreeType):
        self.x = x
        self.y = y
        self.type = tree_type  # Reference to shared intrinsic state

class TreeFactory:
    _tree_types = {}

    @classmethod
    def get_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
        return cls._tree_types[key]

# Usage
positions = [(0, 0), (1, 0), (0, 1)]  # Example positions
trees = []
oak_type = TreeFactory.get_type("Oak", "Green", "OakTexture.png")
for x, y in positions:
    trees.append(Tree(x, y, oak_type))
````

---

## Key Components

| Component        | Role                                   |
| ---------------- | -------------------------------------- |
| Flyweight        | Stores intrinsic (shared) state        |
| FlyweightFactory | Creates and manages shared instances   |
| Client           | Combines intrinsic and extrinsic state |

---

## Advantages

* Reduces memory usage significantly
* Improves performance through sharing
* Enables handling millions of objects efficiently
* Centralizes management of shared state

---

## When to Use

* Video games (particles, sprites, objects)
* Text editors (characters)
* Rendering engines or graphical simulations
* Large-scale systems with many similar objects

---

## Summary

The **Flyweight pattern** is essential for:

* Sharing expensive objects across multiple instances
* Minimizing memory usage in large-scale systems
* Improving performance and scalability
* Supporting millions of fine-grained objects efficiently

**Key Principle:** Separate intrinsic (shared) from extrinsic (unique) state and manage shared instances through a factory.

