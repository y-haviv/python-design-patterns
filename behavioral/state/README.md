# State Pattern (Behavioral)

> **Architectural Level:** Object Behavior Control  
> **Pythonic Strategy:** State-Dependent Behavior Delegation  
> **Production Status:** Stateful Behavior | Cleaner State Logic | Extensively Documented

---

## Also Known As

- Objects for States

---

## Intent

Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

The State pattern enables an object to change its behavior dynamically by delegating state-specific behavior to separate state objects. This eliminates complex conditional logic and promotes cleaner, more maintainable designs.

---

## Problem

Many real-world objects must behave differently depending on their internal state. A direct implementation typically relies on conditional logic, which leads to complex and fragile code.

### Common Issues

- **Cascading Conditionals:** Large `if-elif-else` or `switch` statements become difficult to maintain.
- **Mixed Responsibilities:** State management and behavior logic are combined in a single class.
- **Tight Coupling:** Adding or modifying states requires changing existing logic.
- **Code Duplication:** Conditional logic is often repeated across multiple methods.
- **Reduced Clarity:** Complex state machines become difficult to understand and extend.

### Real-World Scenario (Anti-Pattern)

A TCP connection behaves differently depending on its state:

```python
# Anti-pattern: Cascading conditionals
class TCPConnection:
    def __init__(self):
        self.state = "CLOSED"
    
    def open(self):
        if self.state == "CLOSED":
            self.state = "LISTEN"
        elif self.state == "LISTEN":
            print("Already listening")
    
    def send(self, data):
        if self.state == "ESTABLISHED":
            pass
        elif self.state == "CLOSED":
            print("Cannot send - connection closed")
        elif self.state == "LISTEN":
            print("Cannot send - connection not established")
    
    def close(self):
        if self.state in ("LISTEN", "ESTABLISHED"):
            self.state = "CLOSED"
        elif self.state == "CLOSED":
            print("Already closed")
````

This implementation tightly couples behavior with state representation and becomes harder to maintain as complexity grows.

---

## Solution

Encapsulate state-specific behavior into separate state classes.

```python
class TCPState:
    def open(self, context):
        raise NotImplementedError
    
    def send(self, context, data):
        raise NotImplementedError
    
    def close(self, context):
        raise NotImplementedError


class TCPClosed(TCPState):
    def open(self, context):
        context.state = TCPListen()


class TCPEstablished(TCPState):
    def send(self, context, data):
        print("Sending data:", data)
```

The context delegates behavior to its current state object.

---

## Structure

```
Context
 ├── request()
 ├── set_state(state)
 └── state

State
 ├── handle()
 ├── on_enter()
 └── on_exit()

ConcreteStateA
ConcreteStateB
ConcreteStateC
```

---

## Key Components

### Context

* Maintains a reference to the current state
* Defines the interface exposed to clients
* Delegates state-specific behavior to the state object

### State

* Defines the interface for handling behavior associated with a state

### ConcreteState

* Implements behavior for a specific state
* Handles transitions when appropriate

---

## Benefits

### Single Responsibility Principle

Each state encapsulates its own behavior.

### Open/Closed Principle

New states can be added without modifying existing code.

### Eliminates Conditional Complexity

Replaces complex conditional logic with polymorphism.

### Improved Maintainability

State logic is organized into clear, isolated units.

### Clear State Transitions

State machines become easier to understand and extend.

### Lifecycle Hooks

States can perform initialization and cleanup operations.

---

## Trade-offs

### Increased Number of Classes

Each state requires its own class.

### Potential Overengineering

May be unnecessary for simple state machines.

### Indirection

Adds an extra layer of abstraction.

### Learning Curve

Requires understanding of polymorphism and delegation.

---

## Real-World Example

This project includes a TCP connection state machine with the following states:

* **TCPClosed** — Initial state, connection can be opened
* **TCPListen** — Waiting for connection establishment
* **TCPEstablished** — Active connection, allows data transfer

Example:

```python
connection = TCPConnection("conn1")

connection.open()
connection.send_syn_ack()
connection.send("Hello")
connection.close()

connection.display_connection_info()
```

---

## When to Use

Use the State pattern when:

* Object behavior changes depending on internal state
* Conditional logic based on state becomes complex
* State transitions occur at runtime
* You are implementing:

  * Network protocols
  * Workflow engines
  * GUI state handling
  * Game character states
  * Process lifecycles

---

## When Not to Use

Avoid the State pattern when:

* The object has very few states
* State transitions are simple and static
* The added abstraction provides no clear benefit
* Performance constraints prohibit additional indirection

---

## Pattern Relationships

### Strategy

Both use composition and polymorphism.

* Strategy: Client selects behavior
* State: Behavior changes automatically based on internal state

### Visitor

Visitor applies external operations. State internalizes behavior.

### Factory Method

Can be used to create state objects.

### Singleton

State objects are often implemented as singletons.

---

## Python-Specific Considerations

### Stateless State Objects

State objects are often stateless and reusable.

### Dynamic Delegation

Python makes delegation natural and flexible.

### Context Managers

Can be used to handle state entry and exit.

### Metaprogramming

Metaclasses can validate transitions automatically.

---

## Example Usage

```python
connection = TCPConnection("conn1")

print(connection.get_state())

connection.open()

connection.send("data")

connection.close()
```

---

## Implementation Notes

### State Transitions

Ensure transitions only occur between valid states.

### Context Access

State objects typically receive the context as a parameter.

### Lifecycle Methods

Implement optional entry and exit methods when needed.

### Singleton Optimization

Reuse state instances when possible.

### Logging and Debugging

Track transitions to simplify debugging.

---

## Related Patterns

* Strategy
* Visitor
* Template Method
* Bridge

---

## Comparison: State vs Strategy

| Aspect          | State                                         | Strategy                                |
| --------------- | --------------------------------------------- | --------------------------------------- |
| Purpose         | Encapsulates behavior based on internal state | Encapsulates interchangeable algorithms |
| Behavior Change | Automatic                                     | Selected by client                      |
| Object Role     | Appears to change class                       | Uses different algorithm                |
| Control         | Internal                                      | External                                |

---

## Common Mistakes

### Incomplete State Interface

All states must implement the required interface.

### External State Manipulation

State transitions should be controlled internally.

### Tight Coupling Between States

States should communicate through the context.

### Missing Lifecycle Handling

Entry and exit logic should be clearly defined when required.

### Excessive State Creation

Reuse state instances when possible.

---

## Summary

The State pattern is a behavioral design pattern that enables an object to change its behavior dynamically based on its internal state.

It improves maintainability, scalability, and clarity by eliminating conditional logic and organizing behavior into well-defined state objects.

It is particularly useful in systems that model workflows, protocols, or any process with clearly defined states and transitions.



