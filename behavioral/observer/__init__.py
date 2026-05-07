"""
Observer Pattern (Behavioral)

Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified automatically. This pattern
provides a way to loosely couple disparate components of a system.
"""

from .pattern import (
    ConcreteObserver,
    ConcreteSubject,
    Observer,
    Subject,
)
from .real_world_example import (
    Investor,
    Stock,
    StockMarket,
)

__all__ = [
    "Observer",
    "Subject",
    "ConcreteObserver",
    "ConcreteSubject",
    "Stock",
    "Investor",
    "StockMarket",
]
