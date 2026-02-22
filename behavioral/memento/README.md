# Memento Pattern (Behavioral)

> **Architectural Level:** State Preservation  
> **Pythonic Strategy:** Deep Copy & State Snapshots  
> **Production Status:** Undo/Redo Ready | Encapsulated State | Extensively Documented

## Also Known As

- Snapshot
- Token

## Intent

Capture and externalize an object's internal state without violating encapsulation, and allow the object to be restored to this state later. The Memento pattern provides a way to save snapshots of an object's state so it can be restored to that state without accessing the object's internals.

## Problem

Many applications need undo/redo or save/restore functionality, but:

- **State Encapsulation:** You can't directly access an object's internals to save/restore state without breaking encapsulation.
- **Complex State:** Objects might have complex, nested internal structures.
- **Multiple Snapshots:** You need to maintain multiple versions of state.
- **Performance:** Creating a full copy of state on every change is expensive.

## Solution

Create a `Memento` that captures the state snapshot. An `Originator` creates mementos and restores itself from them. A `Caretaker` manages the collection of mementos.

## Key Characteristics

### Advantages

- **Preserves Encapsulation:** Clients don't access object's internals.
- **Undo/Redo Support:** Easy to implement history management.
- **State Isolation:** Mementos are snapshots, independent of originator.
- **Multiple Snapshots:** Can maintain multiple versions simultaneously.

### Disadvantages

- **Memory Usage:** Each memento consumes memory for state copy.
- **Performance:** Deep copying can be expensive for large objects.
- **Complexity:** Adds several new classes to the design.

## Comparison with Other Patterns

| Pattern | Purpose | Storage | Use When |
|---------|---------|---------|----------|
| **Memento** | Capture state for restoration | Snapshots | Need undo/redo |
| **Command** | Encapsulate actions for execution | Operations | Need reversible actions |
| **Prototype** | Clone objects for creation | Prototypes | Need to create variants |

## When to Use

- Application needs undo/redo functionality
- Save/restore object state without exposing internals
- Multiple versions of state must coexist
- Want to navigate through state history

## When NOT to Use

- Simple objects with trivial state
- Performance-critical applications with huge objects
- Only one state snapshot needed
- Object state changes rarely

## See Also

- [Memento Pattern - Wikipedia](https://en.wikipedia.org/wiki/Memento_pattern)
- [Command Pattern - Wikipedia](https://en.wikipedia.org/wiki/Command_pattern)
- [../command/README.md](../command/README.md)
