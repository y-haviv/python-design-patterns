"""
Behavioral Patterns

Design patterns that deal with object collaboration and responsibility distribution.
These patterns characterize the ways in which classes or objects interact and
distribute responsibility. They describe not just patterns of objects or classes,
but the communication patterns between them.

This module provides eight fundamental behavioral patterns:

1. **Command** - Encapsulate a request as an object with undo/redo support
2. **Iterator** - Access elements of an aggregate object sequentially
3. **Mediator** - Define an object that encapsulates how a set of objects interact
4. **Memento** - Capture and externalize object's internal state for undo/restore
5. **Observer** - Define a one-to-many dependency with automatic notifications
6. **State** - Allow an object to alter behavior when internal state changes
7. **Strategy** - Define a family of interchangeable algorithms
8. **Visitor** - Represent an operation to be performed on object structure

Usage Examples:
    # Command - request encapsulation
    from behavioral import Command, Invoker
    
    # Iterator - sequential access
    from behavioral import Iterator, ConcreteIterable
    
    # Mediator - centralized communication
    from behavioral import Mediator, Colleague
    
    # Memento - state snapshots
    from behavioral import Memento, Originator, Caretaker
    
    # Observer - event notifications
    from behavioral import Observer, Subject
    
    # State - dynamic behavior
    from behavioral import State, Context
    
    # Strategy - algorithm selection
    from behavioral import Strategy, Context
    
    # Visitor - operations on structures
    from behavioral import Visitor, Element

See README.md for comprehensive comparison and best practices.
"""

# Command Pattern
from .command.pattern import (
    Command,
    Receiver,
    ConcreteCommand,
    Invoker,
    MacroCommand,
)

# Iterator Pattern
from .iterator.pattern import (
    Iterator,
    Iterable,
    ConcreteIterator,
    ReverseIterator,
    FilteredIterator,
    ConcreteIterable,
    BidirectionalIterator,
    LazyIterator,
)

# Mediator Pattern
from .mediator.pattern import (
    Colleague,
    Mediator,
    ConcreteColleague,
    ConcreteMediator,
    SmartMediator,
)

# Memento Pattern
from .memento.pattern import (
    Memento,
    ConcreteMemento,
    Originator,
    Caretaker,
)

# Observer Pattern
from .observer.pattern import (
    Observer,
    Subject,
    ConcreteObserver,
    ConcreteSubject,
)

# State Pattern
from .state.pattern import (
    State,
    Context as StateContext,
    ConcreteStateA,
    ConcreteStateB,
    ConcreteStateC,
)

# Strategy Pattern
from .strategy.pattern import (
    Strategy,
    Context as StrategyContext,
    ConcreteStrategyA,
    ConcreteStrategyB,
    ConcreteStrategyC,
)

# Visitor Pattern
from .visitor.pattern import (
    Visitor,
    Element,
    ConcreteElementA,
    ConcreteElementB,
    ConcreteVisitorA,
    ConcreteVisitorB,
)

__all__ = [
    # Command
    "Command",
    "Receiver",
    "ConcreteCommand",
    "Invoker",
    "MacroCommand",
    
    # Iterator
    "Iterator",
    "Iterable",
    "ConcreteIterator",
    "ReverseIterator",
    "FilteredIterator",
    "ConcreteIterable",
    "BidirectionalIterator",
    "LazyIterator",
    
    # Mediator
    "Colleague",
    "Mediator",
    "ConcreteColleague",
    "ConcreteMediator",
    "SmartMediator",
    
    # Memento
    "Memento",
    "ConcreteMemento",
    "Originator",
    "Caretaker",
    
    # Observer
    "Observer",
    "Subject",
    "ConcreteObserver",
    "ConcreteSubject",
    
    # State
    "State",
    "StateContext",
    "ConcreteStateA",
    "ConcreteStateB",
    "ConcreteStateC",
    
    # Strategy
    "Strategy",
    "StrategyContext",
    "ConcreteStrategyA",
    "ConcreteStrategyB",
    "ConcreteStrategyC",
    
    # Visitor
    "Visitor",
    "Element",
    "ConcreteElementA",
    "ConcreteElementB",
    "ConcreteVisitorA",
    "ConcreteVisitorB",
]
