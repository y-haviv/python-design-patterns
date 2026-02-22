# Strategy Pattern (Behavioral)

> **Architectural Level:** Algorithm Selection  
> **Pythonic Strategy:** Polymorphic Algorithm Encapsulation  
> **Production Status:** Interchangeable Algorithms | Runtime Selection | Extensively Documented

---

## Also Known As

- Policy

---

## Intent

Define a family of algorithms, encapsulate each one, and make them interchangeable.

The Strategy pattern allows the algorithm to vary independently from the clients that use it. It enables selecting and switching algorithms at runtime without modifying the client code.

---

## Problem

Applications often need to support multiple algorithms to accomplish the same task. Direct implementation typically embeds the algorithms inside the context, resulting in rigid and difficult-to-maintain code.

### Common Issues

- **Hard-Coded Logic:** Algorithms are embedded directly in the context, making replacement difficult.
- **Conditional Complexity:** Large `if-elif-else` or `switch` statements control algorithm selection.
- **Limited Extensibility:** Adding new algorithms requires modifying existing code.
- **Code Duplication:** Algorithm selection logic may be repeated across the codebase.
- **Mixed Responsibilities:** Context classes become responsible for both execution and algorithm logic.

### Real-World Scenario (Anti-Pattern)

Payment processing with multiple payment methods:

```python
class PaymentProcessor:
    def process_payment(self, method, amount, details):
        if method == "credit_card":
            card_number, cvv = details
            pass

        elif method == "paypal":
            email, password = details
            pass

        elif method == "crypto":
            wallet = details
            pass
````

This implementation is difficult to extend and violates the Open/Closed Principle.

---

## Solution

Encapsulate each algorithm into its own strategy class and delegate execution to the selected strategy.

```python
class PaymentStrategy:
    def validate(self):
        raise NotImplementedError
    
    def process_payment(self, amount):
        raise NotImplementedError


class CreditCardStrategy(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Processing credit card payment: {amount}")


class PayPalStrategy(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Processing PayPal payment: {amount}")


class PaymentProcessor:

    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def pay(self, amount):
        self.strategy.process_payment(amount)
```

The client can switch strategies dynamically.

---

## Structure

```
Client
  │
  ▼
Context
 ├── set_strategy()
 └── execute()

Strategy
 └── execute()

ConcreteStrategyA
ConcreteStrategyB
ConcreteStrategyC
```

---

## Key Components

### Strategy

Defines a common interface for all supported algorithms.

### ConcreteStrategy

Implements a specific algorithm using the Strategy interface.

### Context

Maintains a reference to a Strategy object and delegates execution to it.

---

## Benefits

### Runtime Flexibility

Algorithms can be selected and changed at runtime.

### Eliminates Conditional Logic

Removes large conditional blocks from the context.

### Open/Closed Principle

New strategies can be introduced without modifying existing code.

### Encapsulation

Each algorithm is isolated in its own class.

### Improved Maintainability

Changes to one algorithm do not affect others.

### Testability

Strategies can be tested independently.

---

## Trade-offs

### Increased Number of Classes

Each algorithm requires its own class.

### Additional Indirection

Adds abstraction between context and implementation.

### Slight Performance Overhead

Polymorphic dispatch introduces minimal runtime overhead.

### Client Awareness

Client must know which strategy to use.

---

## Real-World Example

This project includes a shopping cart system supporting multiple payment strategies:

* CreditCardStrategy
* PayPalStrategy
* CryptocurrencyStrategy

Example:

```python
cart = ShoppingCart()

cart.add_item("Widget", 10.0, 1)

card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
cart.set_payment_method(card)
cart.checkout()

paypal = PayPalStrategy("user@example.com", "password")
cart.set_payment_method(paypal)
cart.checkout()
```

---

## When to Use

Use the Strategy pattern when:

* Multiple algorithms perform the same task
* Algorithms need to be selected at runtime
* Conditional logic becomes complex
* Algorithms evolve independently
* You want to isolate algorithm logic

Common use cases:

* Payment processing
* Sorting algorithms
* Compression systems
* Routing and pathfinding
* Authentication methods

---

## When Not to Use

Avoid the Strategy pattern when:

* Only one algorithm exists
* Algorithm selection never changes
* Simplicity is more important than flexibility
* Performance constraints prohibit abstraction

---

## Pattern Relationships

### State

Both use composition and polymorphism.

* Strategy: Client selects behavior
* State: Behavior changes automatically

### Template Method

Template Method defines the structure of an algorithm, while Strategy encapsulates the entire algorithm.

### Decorator

Decorator adds behavior dynamically. Strategy replaces behavior entirely.

### Factory Method

Factory Method can create Strategy instances.

---

## Python-Specific Considerations

### First-Class Functions

Functions can replace strategy classes for simpler implementations.

### Duck Typing

Strategies do not need explicit inheritance as long as the interface is respected.

### Dynamic Assignment

Strategies can be assigned and replaced dynamically.

### Context Managers

Useful for setup and teardown logic.

---

## Example Usage

```python
context = Context(ConcreteStrategyA())

result = context.execute_strategy(data)

context.set_strategy(ConcreteStrategyB())

result = context.execute_strategy(data)

strategies = [
    ConcreteStrategyA(),
    ConcreteStrategyB(),
    ConcreteStrategyC()
]

for strategy in strategies:
    context.set_strategy(strategy)
    print(context.execute_strategy(data))
```

---

## Implementation Notes

### Consistent Interface

All strategies must implement the same interface.

### Simple Context

Context should only delegate execution.

### Strategy Independence

Strategies should not depend on each other.

### Runtime Safety

Switching strategies should not break the system.

### Documentation

Clearly document available strategies and their use cases.

---

## Related Patterns

* State
* Template Method
* Visitor
* Composite
* Factory Method

---

## Common Mistakes

### Missing Strategy Interface

All strategies must conform to the same contract.

### Mixing Responsibilities

Context should not implement algorithm logic.

### Excessive Strategy Creation

Reuse strategy instances when possible.

### Poor Documentation

Users must understand when to use each strategy.

### Overengineering

Avoid using Strategy when simple conditional logic is sufficient.

---

## Comparison: Strategy vs Alternatives

| Pattern         | Purpose                                | Selection Method  | Complexity |
| --------------- | -------------------------------------- | ----------------- | ---------- |
| Strategy        | Encapsulate interchangeable algorithms | Client or runtime | Medium     |
| State           | Encapsulate state-dependent behavior   | Internal state    | High       |
| Template Method | Define algorithm structure             | Inheritance       | Low        |
| Visitor         | Add operations to object structures    | External dispatch | High       |

---

## Summary

The Strategy pattern is a behavioral design pattern that encapsulates algorithms into separate, interchangeable components.

It improves flexibility, maintainability, and extensibility by allowing algorithms to vary independently from the context.

It is widely used in systems that require runtime algorithm selection and modular design.

