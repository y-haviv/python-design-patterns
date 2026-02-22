# Behavioral Design Patterns

> **Category:** Object interaction and responsibility distribution  
> **Focus:** Defining how objects interact and distribute work  
> **Pythonic Strategy:** Protocols, Polymorphism, and State Management

## Overview

Behavioral design patterns are concerned with the interaction between objects—how they communicate, distribute responsibilities, and work together. They help define how objects interact to accomplish tasks and distribute the flow of control.

This directory contains comprehensive implementations of 8 behavioral design patterns, each with:

- **pattern.py** - Core pattern implementation with abstract interfaces and concrete classes
- **real_world_example.py** - Practical, real-world use cases
- **test_pattern.py** - Comprehensive pytest test suites (100+ tests total)
- **README.md** - Documentation with design principles and comparisons

## Patterns Included

### 1. [Command](command/README.md) - Request Encapsulation

Encapsulate a request as an object, allowing parameterization of clients with different requests, execution later, and undo/redo functionality.

**Key Features:**
- Decouple sender from receiver
- Queue, schedule, and log operations
- Undo/redo and macro commands
- Example: Text editor with undo/redo history

**Use When:** You need to queue requests, support undo/redo, or parameterize clients with requests.

---

### 2. [Iterator](iterator/README.md) - Sequential Access

Provide a way to access elements of a collection sequentially without exposing its representation.

**Key Features:**
- Multiple simultaneous iterators on same collection
- Different traversal strategies (forward, reverse, filtered)
- Lazy evaluation for memory efficiency
- Example: Book collection with multiple iteration strategies

**Use When:** Collections need multiple traversal methods without exposing internals.

---

### 3. [Mediator](mediator/README.md) - Centralized Coordination

Define an object that encapsulates how objects interact, promoting loose coupling.

**Key Features:**
- Decoupled colleague communication
- Centralized interaction logic
- Message routing and filtering
- Example: Chat room coordinating user interactions

**Use When:** Objects have complex, many-to-many interactions that change frequently.

---

### 4. [Memento](memento/README.md) - State Preservation

Capture and externalize an object's state without violating encapsulation, enabling restoration later.

**Key Features:**
- State snapshots without exposing internals
- Undo/redo with history navigation
- Multiple version management
- Example: Document save/restore with full history

**Use When:** You need to save/restore object state or support undo/redo.

---

### 5. [Observer](observer/README.md) - One-to-Many Notification

Define a one-to-many dependency between objects so when one changes, all dependents are notified.

**Key Features:**
- Loose coupling between subject and observers
- Automatic notification on state changes
- Multiple observers with independent updates
- Example: Stock prices notifying multiple investors

**Use When:** Objects need to notify multiple other objects about state changes.

---

### 6. [State](state/README.md) - State-Dependent Behavior

Allow an object to alter its behavior when its state changes, appearing to change its class.

**Key Features:**
- State-specific behavior without conditionals
- Entry/exit actions for state transitions
- Complex state machines simplified
- Example: TCP connection state management

**Use When:** Object behavior depends on state, or to avoid cascading if/else chains.

---

### 7. [Strategy](strategy/README.md) - Interchangeable Algorithms

Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Key Features:**
- Runtime algorithm selection
- Encapsulated, interchangeable strategies
- Easy to add new algorithms
- Example: Payment processing with multiple payment methods

**Use When:** You have multiple algorithms for a task, chosen at runtime.

---

### 8. [Visitor](visitor/README.md) - Operations on Elements

Represent an operation to be performed on elements of an object structure, letting you define new operations without changing the elements' classes.

**Key Features:**
- Operations separated from element classes
- Multiple visitors for different operations
- Complex structure traversal
- Example: Document exporting to multiple formats (PDF, HTML)

**Use When:** Many distinct operations on complex object structures, and you want to avoid modifying element classes.

---

## Pattern Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                  BEHAVIORAL PATTERNS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  COMMUNICATION              STATE MANAGEMENT                │
│  ─────────────              ─────────────────                │
│  • Command       ←→ Memento   • State                        │
│  • Observer                   • Strategy                     │
│  • Mediator                   • Visitor                      │
│  • Iterator                                                  │
│                                                              │
│  Related to STRUCTURAL patterns:                            │
│  • Memento ←→ Prototype (state vs. objects)                 │
│  • Visitor ←→ Composite (traversal)                         │
│  • Strategy ←→ Decorator (behavioral variation)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Pattern Selection Guide

### Quick Decision Tree

**Q: Do you need to notify multiple objects about changes?**
→ Observer

**Q: Do you need to select among multiple algorithms at runtime?**
→ Strategy

**Q: Do you need to save/restore object state?**
→ Memento

**Q: Do you need to defer execution or create command queues?**
→ Command

**Q: Do you need to traverse a collection multiple ways?**
→ Iterator

**Q: Do you have complex object interactions to coordinate?**
→ Mediator

**Q: Does object behavior depend on internal state?**
→ State

**Q: Do you need to perform operations on complex object structures?**
→ Visitor

## Comparison Matrix

| Pattern | Coupling | Complexity | Memory | Flexibility | Use Frequency |
|---------|----------|-----------|--------|-------------|---------------|
| Command | Low | Medium | High | High | High |
| Iterator | Low | Medium | Low | Medium | High |
| Mediator | Medium | High | Low | High | Medium |
| Memento | Low | Medium | High | Medium | Medium |
| Observer | Low | Low | Low | High | Very High |
| State | Low | High | Low | High | High |
| Strategy | Low | Low | Low | High | Very High |
| Visitor | Low | High | Low | Medium | Medium |

## Implementation Quality

### Test Coverage
- **Total Tests:** 150+ comprehensive pytest test suites
- **Coverage:** All patterns, edge cases, and real-world scenarios
- **Standards:** Following pytest best practices

### Documentation
- **Code Documentation:** Comprehensive docstrings and type hints
- **Pattern Documentation:** 8 READMEs with comparisons and examples
- **Quality:** Production-ready, publication-quality documentation

### Real-World Examples
- Command: Text editor with undo/redo
- Iterator: Library book collection
- Mediator: Chat room system
- Memento: Document versioning
- Observer: Stock market trading
- State: TCP connection lifecycle
- Strategy: Multi-method payment processing
- Visitor: Document export system

## Pythonic Considerations

### Python's Built-in Support

1. **Iterator Pattern:** Python's `__iter__()` and `__next__()` make iterators Pythonic
2. **Observer Pattern:** Can use callbacks or event frameworks like `PyPubSub`
3. **Strategy Pattern:** First-class functions can often replace Strategy classes
4. **State Pattern:** Can be implemented with simple state machines or libraries
5. **Command Pattern:** Callables and decorators provide alternatives

### When to Use OOP Patterns vs. Pythonic Approaches

```python
# Traditional Strategy Pattern (OOP)- class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass

class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount): ...

# Pythonic approach (functions)
def pay_with_credit_card(amount):
    ...

# Use OOP when:
# - Complex state within strategies
# - Strategies need lifecycle management
# - Team prefers explicit interfaces
```

## Getting Started

### Running Tests

```bash
# Run all behavioral pattern tests
pytest behavioral/ -v

# Run specific pattern tests
pytest behavioral/observer/test_pattern.py -v

# Run with coverage
pytest behavioral/ --cov=behavioral --cov-report=html
```

### Using Patterns

```python
# Example: Observer pattern for stock trading
from behavioral.observer import StockMarket, Investor

market = StockMarket()
apple_stock = market.add_stock("AAPL", 150.00)

investor1 = Investor("Alice", market)
investor2 = Investor("Bob", market)

# Observers are automatically notified of price changes
apple_stock.price_changed(152.50)  # Both investors receive update
```

### Learning Path

**Recommended order for learning:**
1. **Observer** - Start with simple one-to-many notifications
2. **Strategy** - Learn algorithm encapsulation
3. **State** - Understand state-dependent behavior
4. **Command** - Build on state with reversible operations
5. **Memento** - Add state preservation
6. **Iterator** - Explore collection traversal
7. **Mediator** - Handle complex interactions
8. **Visitor** - Master advanced traversal patterns

## Design Principles Applied

### SOLID Principles

- **S**ingle Responsibility: Each pattern isolates specific responsibility
- **O**pen/Closed: Patterns enable extending without modifying existing code
- **L**iskov Substitution: Concrete implementations are substitutable
- **I**nterface Segregation: Focused, minimal interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

### Additional Principles

- **Encapsulation:** State and behavior properly hidden
- **Composition Over Inheritance:** Favor runtime composition  
- **Loose Coupling:** Minimal object dependencies
- **High Cohesion:** Related functionality grouped

## Resources

### Pattern Documentation
- [Gang of Four Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru - Behavioral Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)
- [Python Patterns](https://python-patterns.guide/)

### Related Creational Patterns
- See `../creational/` for object creation patterns
- See `../structural/` for object composition patterns
