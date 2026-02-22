# Decorator Pattern (Structural)

> **Architectural Level:** Object Behavior  
> **Pythonic Strategy:** Wrapping & Composition  
> **Production Status:** Widely Used | Runtime Behavior | Best Practice

---

## Intent

Attach additional responsibilities to an object dynamically while maintaining the same interface. The Decorator pattern provides a flexible alternative to subclassing for extending functionality.

---

## Problem

Extending behavior through inheritance can lead to a combinatorial explosion of subclasses:

```

Without Decorator:
Coffee
├── CoffeeWithMilk
├── CoffeeWithSugar
├── CoffeeWithMilkAndSugar
├── CoffeeWithWhippedCream
└── ...

````

You need a way to:

- Add behavior dynamically
- Avoid modifying the original class
- Prevent subclass proliferation
- Maintain flexibility and composability

---

## Solution

Use composition and wrapping to extend behavior at runtime.

### Example

```python
class Coffee:
    def get_cost(self):
        return 2.0


class MilkDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee

    def get_cost(self):
        return self.coffee.get_cost() + 0.5


class SugarDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee

    def get_cost(self):
        return self.coffee.get_cost() + 0.2
````

### Flexible Combination

```python
coffee = Coffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)
# coffee now has milk and sugar behavior
```

---

## Key Components

| Component         | Description                                         |
| ----------------- | --------------------------------------------------- |
| Component         | Interface for objects that can be decorated         |
| ConcreteComponent | Original object implementing Component              |
| Decorator         | Wraps a Component and implements the same interface |
| ConcreteDecorator | Adds specific behavior or responsibility            |

---

## Advantages

* **Single Responsibility Principle:** Each decorator focuses on a single responsibility
* **Open/Closed Principle:** Extend behavior without modifying existing classes
* **Runtime Flexibility:** Decorators can be combined at runtime
* **Alternative to Inheritance:** Avoids subclass explosion
* **Stackable Behavior:** Unlimited combination of decorators

---

## Disadvantages

* **Complexity:** Large chains of decorators can be hard to understand
* **Order Sensitivity:** The order of decorators affects behavior
* **Performance Overhead:** Many small objects may impact performance

---

## Real-World Applications

* I/O stream wrappers (e.g., compression, encryption, buffering)
* UI component decoration (e.g., borders, scrollbars, shadows)
* Configuration decorators (e.g., adding features dynamically)
* Middleware in web frameworks (e.g., request/response processing)

---

## Summary

The Decorator pattern is ideal for:

* Dynamically adding behavior to objects
* Avoiding subclass proliferation
* Combining features flexibly
* Maintaining clean and consistent interfaces

**Key Principle:** Use composition to wrap objects with additional responsibilities while preserving their interface.

