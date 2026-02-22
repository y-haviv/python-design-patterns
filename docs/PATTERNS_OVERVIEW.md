# Patterns Overview - Detailed Comparison

This document provides a comprehensive comparison of all 21 design patterns in this repository.

---

## Quick Reference Table

| Pattern | Category | Complexity | Frequency | Best For |
|---------|----------|-----------|-----------|----------|
| Singleton | Creational | Low | Very High | Single instance objects |
| Factory Method | Creational | Medium | Very High | Flexible object creation |
| Abstract Factory | Creational | High | High | Family of objects |
| Builder | Creational | Medium | High | Complex construction |
| Prototype | Creational | Medium | Medium | Efficient cloning |
| **Adapter** | Structural | Medium | High | Interface compatibility |
| **Bridge** | Structural | Medium | Medium | Abstraction separation |
| **Composite** | Structural | Medium | High | Tree structures |
| **Decorator** | Structural | Medium | High | Dynamic enhancement |
| **Facade** | Structural | Low | High | Simplification |
| **Flyweight** | Structural | High | Medium | Memory optimization |
| **Proxy** | Structural | Medium | High | Access control |
| Command | Behavioral | Medium | Medium | Request encapsulation |
| Iterator | Behavioral | Low | High | Collection access |
| Mediator | Behavioral | High | Medium | Centralized coordination |
| Memento | Behavioral | Medium | Medium | State preservation |
| Observer | Behavioral | Low | Very High | Event notification |
| State | Behavioral | Medium | High | State-dependent behavior |
| Strategy | Behavioral | Low | Very High | Algorithm selection |
| Visitor | Behavioral | High | Low | Tree traversal |

---

## 🎓 Learning Difficulty

### Easiest (Start Here)
```
1. Singleton       - Basic principle: single instance
2. Observer        - Natural event system
3. Strategy        - Simple algorithm switching
4. Iterator        - Familiar traversal concept
5. Factory Method  - Common in practice
```

### Intermediate
```
6. Adapter         - Clear interface translation
7. Decorator       - Wrapping concept
8. Command         - Encapsulating requests
9. State          - Behavioral logic
10. Composite     - Recursive thinking
11. Builder       - Step-by-step construction
12. Facade        - Complexity hiding
13. Prototype     - Cloning logic
```

### Advanced
```
14. Abstract Factory - Multiple families
15. Bridge           - Abstraction separation
16. Visitor          - Double dispatch
17. Mediator         - Complex communication
18. Memento          - State externalization
19. Flyweight        - Intrinsic/extrinsic state
20. Proxy            - Access control complexity
```

---

## 🏗️ By Creation Method

### Object Creation Patterns (Creational)

```
Singleton
├─ Ensure single instance
├─ Provide global access
└─ Thread-safe creation

Factory Method
├─ Defer to subclasses
├─ Flexible instantiation
└─ Encapsulate creation

Abstract Factory
├─ Family of objects
├─ Multiple implementations
└─ Interchangeable families

Builder
├─ Step-by-step construction
├─ Handle optional parameters
└─ Reduce parameter lists

Prototype
├─ Clone existing objects
├─ Efficient duplication
└─ Prototype registry
```

---

## 🔗 By Composition Method (Structural)

```
Adapter
├─ Translate interfaces
├─ Bridge incompatibilities
└─ Multiple implementations

Bridge
├─ Separate abstraction/implementation
├─ Independent variation
└─ Avoid hierarchy explosion

Composite
├─ Treat individual and composite uniformly
├─ Tree structure
└─ Recursive composition

Decorator
├─ Add responsibilities dynamically
├─ Multiple wrappings
└─ Avoid subclassing

Facade
├─ Hide complex subsystems
├─ Provide simple interface
└─ Reduce dependencies

Flyweight
├─ Share common state
├─ Memory optimization
└─ Object pooling

Proxy
├─ Control access
├─ Lazy loading
└─ Add operations transparently
```

---

## 💬 By Interaction Method (Behavioral)

```
Command
├─ Encapsulate requests
├─ Parameterize clients
└─ Undo/redo support

Iterator
├─ Access collection elements
├─ Hide internal structure
└─ Multiple iterations

Mediator
├─ Centralize communication
├─ Reduce coupling
└─ Manage interactions

Memento
├─ Capture state
├─ Restore later
└─ Undo history

Observer
├─ Notify multiple objects
├─ Event distribution
└─ Loose coupling

State
├─ Encapsulate state behavior
├─ Change appearance
└─ State transitions

Strategy
├─ Select algorithm
├─ Runtime choice
└─ Interchangeable algorithms

Visitor
├─ Add operations to hierarchy
├─ Double dispatch
└─ Separate concerns
```

---

## 🎯 By Use Frequency

### Very High (Essential Knowledge)
1. **Singleton** - Almost every project
2. **Factory Method** - Object creation
3. **Observer** - Event systems
4. **Strategy** - Algorithm selection
5. **Decorator** - Behavior extension

### High  (Important for Scaling)
1. **Abstract Factory** - Multi-family creation
2. **Composite** - Tree structures
3. **Facade** - Complexity management
4. **Adapter** - Integration challenges
5. **Builder** - Complex construction
6. **Proxy** - Access control
7. **State** - State machines

### Medium (Situational)
1. **Iterator** - Custom traversal
2. **Bridge** - Dimension separation
3. **Command** - Request queuing
4. **Memento** - State preservation
5. **Prototype** - Efficient cloning
6. **Flyweight** - Memory optimization

### Lower (Specialized)
1. **Mediator** - Complex coordination
2. **Visitor** - Tree operations

---

## 🔄 Pattern Interactions

### Frequently Used Together

```
Singleton + Factory
├─ Single factory instance
├─ Centralized object creation
└─ Shared configuration

Composite + Decorator
├─ Decorate leaf and composite
├─ Enhance hierarchy
└─ Recursive enhancement

Observer + Mediator
├─ Decoupled communication
├─ Event distribution
└─ Coordination mechanisms

Strategy + Command
├─ Algorithm families
├─ Encapsulated requests
└─ Runtime flexibility

Adapter + Factory
├─ Adapt and create
├─ Flexible adaptation
└─ Multiple implementations

Facade + Proxy
├─ Simplify + Control
├─ Single entry point
└─ Controlled access

Prototype + Factory
├─ Clone and create
├─ Efficient creation
└─ Template-based objects
```

### Can Substitute For Each Other

```
Strategy vs State
├─ Strategy: Client chooses algorithm
├─ State: Object changes behavior
└─ Can often swap depending on design

Adapter vs Decorator
├─ Adapter: Change interface
├─ Decorator: Add behavior
└─ Sometimes used for same goal

Composite vs Iterator
├─ Composite: Tree structure with uniform access
├─ Iterator: Sequential access
└─ Often used together

Template Method vs Strategy
├─ Template Method: Inheritance
├─ Strategy: Composition
└─ Strategy is more flexible

Proxy vs Decorator
├─ Proxy: Access control
├─ Decorator: Enhance behavior
└─ Proxy usually wraps single interface
```

---

## 📊 Scales of Complexity

### Memory Trade-offs

```
Low Memory:
└─ Singleton, Adapter, Facade, Strategy

Medium Memory:
└─ Factory Method, Builder, Composite, State

High Memory (but controllable):
└─ Observer (many instances), Visitor (traversal)
├─ Optimizable with Flyweight
└─ Controllable with Proxy (caching)

Memory Savings:
└─ Flyweight - Reduces memory significantly
└─ Proxy - Lazy loading saves upfront memory
```

### Performance Trade-offs

```
Negligible Overhead:
└─ Strategy, Adapter, Facade, Iterator, Visitor

Small Overhead (one indirection):
└─ Bridge, Singleton, Observer, Command

Moderate Overhead:
└─ Factory Method, Decorator, State, Mediator

Optimizable:
└─ Flyweight - Memory savings > CPU cost
└─ Proxy - Optional lazy loading benefit

Context-Dependent:
└─ Composite - Depends on tree depth/size
```

---

## 🔍 When to Use Each Pattern

### Problem: Need to Limit Object Instances
```
✓ Singleton Pattern
- Only one instance needed
- Global access required
```

### Problem: Many Incompatible Interfaces
```
✓ Adapter Pattern
- Convert incompatible interfaces
- Third-party library integration
```

### Problem: Too Many Classes in Hierarchy
```
✓ Bridge Pattern - Separate abstraction/implementation
✓ Abstract Factory - Group related families
✓ Composite - Treat individual/composite uniformly
```

### Problem: Need Flexible Object Creation
```
✓ Factory Method - Deferred to subclasses
✓ Builder - Complex construction
✓ Abstract Factory - Family of objects
```

### Problem: Many Similar Objects Using Memory
```
✓ Flyweight - Share common state
✓ Prototype - Efficient cloning
```

### Problem: Need to Add Behavior Dynamically
```
✓ Decorator - Wrap objects
✓ Proxy - Control access
✓ State - Encapsulate state logic
```

### Problem: Simplify Complex Subsystem
```
✓ Facade - Hide complexity
✓ Adapter - Translate interface
```

### Problem: Notify Multiple Objects of Change
```
✓ Observer - Event distribution
✓ Mediator - Centralized communication
```

### Problem: Need Multiple Algorithm Variations
```
✓ Strategy - Runtime selection
✓ Command - Encapsulated requests
✓ Visitor - Tree operations
```

---

## 🎓 Patterns by Evolution Level

### Foundation (Week 1)
```
→ Singleton - Understand single instances
→ Observer - Understand event systems
→ Strategy - Understand algorithm switching
```

### Solid (Week 2-3)
```
→ Factory Method - Deferred creation
→ Adapter - Interface translation
→ Composite - Tree structures
→ Decorator - Behavior extension
```

### Professional (Week 4+)
```
→ Abstract Factory - Families of objects
→ Builder - Complex creation
→ Bridge - Architecture patterns
→ Facade - Subsystem management
→ State - Complex state machines
→ Command - Request systems
```

### Mastery (Advanced)
```
→ Mediator - Complex coordination
→ Visitor - Advanced traversal
→ Memento - State management
→ Prototype - Cloning strategies
→ Flyweight - Memory optimization
→ Proxy - Advanced access control
→ Iterator - Custom traversals
```

---

## 💼 Industry-Specific Usage

### Web Frameworks (Django, Flask)
```
Primary: Factory Method, Observer, Middleware (Chain of Responsibility)
Secondary: Adapter, Singleton, Decorator
```

### Data Science (numpy, pandas)
```
Primary: Composite, Iterator, Facade
Secondary: Adapter, Flyweight, Proxy
```

### Game Development
```
Primary: Observer, Command, State
Secondary: Composite, Factory Method, Prototype
```

### Enterprise Systems
```
Primary: Factory Method, Adapter, Facade, Observer
Secondary: Mediator, Command, Builder
```

### System Programming
```
Primary: Singleton, Command, Observer, Proxy
Secondary: Factory Method, Adapter, Flyweight
```

---

## 🚀 Scaling Considerations

### For Thousands of Objects
```
Use Flyweight - Reduce memory footprint
Use Proxy - Cache and optimize
Consider Iterator - Efficient traversal
```

### For Complex Hierarchies
```
Use Composite - Uniform access
Use Visitor - Non-invasive operations
Consider Facade - Simplification layer
```

### For Flexible Systems
```
Use Strategy - Algorithm switching
Use Factory Method - Flexible creation
Use Adapter - Integration flexibility
```

### For Event-Heavy Systems
```
Use Observer - Event notification
Use Command - Request queuing
Use Mediator - Centralized coordination
```

---

## 📚 Related Resources

### Books Covering These Patterns
- Design Patterns: Elements of Reusable OOP - Gang of Four
- Head First Design Patterns - Freeman & Freeman
- Refactoring: Improving Design - Martin Fowler

### Pattern Databases
- https://refactoring.guru/design-patterns
- https://www.patterns.dev/
- https://python-patterns.guide/

---

**Tip: Master a few patterns deeply rather than know all patterns superficially. Start with Singleton, Observer, and Strategy!**
