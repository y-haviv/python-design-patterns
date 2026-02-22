# Observer Pattern (Behavioral)

> **Architectural Level:** Event Notification  
> **Pythonic Strategy:** Event-Driven Decoupling  
> **Production Status:** One-to-Many Communication | Loose Coupling | Extensively Documented

---

## Also Known As

- Publish–Subscribe
- Listener
- Dependents

---

## Intent

Define a one-to-many dependency between objects such that when one object changes state, all its dependents are notified automatically.

The Observer pattern provides a mechanism for building loosely coupled systems where components can react to events without being tightly bound to each other.

---

## Problem

In many systems, objects need to react to changes in the state of other objects. A naive implementation introduces direct dependencies, which leads to tight coupling and reduced flexibility.

### Common Issues

- **Hard Dependencies:** Objects must maintain explicit references to all dependents.
- **Cascading Changes:** Modifying one component requires modifying many others.
- **Reduced Reusability:** Objects become tied to specific collaborators.
- **Poor Scalability:** Adding new dependents requires modifying existing code.
- **Tight Coupling:** System flexibility and maintainability suffer.

### Real-World Scenario (Anti-Pattern)

Stock price updates must notify investors:

```python
# Anti-pattern: Direct dependencies (tight coupling)
class Stock:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self.investors = []  # Direct references
    
    def add_investor(self, investor):
        self.investors.append(investor)
    
    def set_price(self, new_price):
        self.price = new_price
        for investor in self.investors:
            investor.on_price_change(self.symbol, new_price)


class Investor:
    def on_price_change(self, symbol, new_price):
        if new_price < 100:
            self.buy()
        elif new_price > 150:
            self.sell()
````

**Problem:** The `Stock` class must know every investor. This creates tight coupling.

---

## Solution

Use the Observer pattern to introduce a generic notification interface.

```python
# Subject
class Stock:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def detach(self, observer):
        self.observers.remove(observer)
    
    def set_price(self, new_price):
        self.price = new_price
        self.notify()
    
    def notify(self):
        for observer in self.observers:
            observer.update(self)


# Observer
class Investor:
    def update(self, stock):
        if stock.price < 100:
            self.buy(stock)
        elif stock.price > 150:
            self.sell(stock)
```

**Result:** The subject no longer depends on concrete observer implementations.

---

## Structure

```
Subject
 ├── attach(observer)
 ├── detach(observer)
 ├── notify()
 └── state

ConcreteSubject
 └── maintains state and notifies observers

Observer
 └── update(subject)

ConcreteObserver
 └── reacts to subject state changes
```

---

## Key Components

### Subject

Defines the interface for:

* Attaching observers
* Detaching observers
* Notifying observers

### ConcreteSubject

* Stores state
* Sends notifications when state changes

### Observer

Defines the update interface.

### ConcreteObserver

* Implements reaction logic
* May store subject state

---

## Benefits

### Loose Coupling

Subjects and observers interact only through an abstract interface.

### Dynamic Relationships

Observers can be added or removed at runtime.

### Broadcast Communication

A subject can notify multiple observers efficiently.

### Separation of Concerns

Subjects manage state. Observers manage reactions.

### Open/Closed Principle

New observers can be introduced without modifying existing subject code.

---

## Trade-offs

### Notification Order

Observers are notified in registration order, which may not always be desirable.

### Memory Management

Observers must be detached properly to avoid memory leaks.

### Performance Considerations

Large numbers of observers may impact performance.

### Indirect Behavior

Side effects caused by observers may be difficult to trace.

---

## Real-World Example

This project includes a realistic stock market simulation:

* **Stock** — Subject that publishes price changes
* **Investor** — Observer reacting to price changes
* **StockMarket** — Coordinator managing entities

Example:

```python
market = StockMarket("NYSE")

aapl = market.add_stock("AAPL", 150.0)

alice = Investor("Alice")
alice.watch_stock(aapl)

aapl.set_price(155.0)

alice.display_portfolio()
```

---

## When to Use

Use the Observer pattern when:

* Changes in one object affect multiple objects
* The number of dependents is unknown beforehand
* You need event-driven architecture
* You want to avoid tight coupling
* You are implementing:

  * GUI frameworks
  * Event systems
  * Message brokers
  * Real-time feeds

---

## When Not to Use

Avoid the Observer pattern when:

* Communication is strictly one-to-one
* Relationships are static and fixed
* Performance constraints prohibit indirect calls
* Notification order is critical and must be guaranteed

---

## Pattern Relationships

### Mediator

Centralizes communication. Observer distributes it.

### Publish–Subscribe

A distributed form of Observer using message channels.

### Command

Observers may execute commands in response to events.

### Strategy

Observers may apply different strategies when reacting.

---

## Python-Specific Considerations

### Property-Based Notifications

Python properties can trigger observer notifications automatically.

### Weak References

The `weakref` module helps prevent memory leaks.

### Event-Driven Libraries

Many Python libraries implement observer-style patterns.

### Context Managers

Can ensure proper observer lifecycle management.

---

## Example Usage

```python
stock = Stock("AAPL", 150.0)

alice = Investor("Alice")
bob = Investor("Bob")

alice.watch_stock(stock)
bob.watch_stock(stock)

stock.set_price(155.0)

alice.display_portfolio()
bob.display_portfolio()
```

---

## Implementation Notes

### Thread Safety

Synchronize access in multithreaded environments.

### Observer Lifecycle

Ensure proper attachment and detachment.

### Exception Handling

Prevent one observer failure from affecting others.

### Performance Optimization

Cache expensive computations when needed.

---

## Related Patterns

* Observable
* Event Loop
* Signal / Slot
* Reactive Extensions

---

## Summary

The Observer pattern is a fundamental behavioral design pattern that enables scalable, maintainable, and loosely coupled event-driven systems.

It is especially valuable in modern architectures where modularity, extensibility, and separation of concerns are essential.

