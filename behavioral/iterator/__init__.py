"""
Iterator Pattern (Behavioral)

Provides a way to access the elements of an aggregate object sequentially 
without exposing its underlying representation.
"""

from .pattern import (
    Iterator,
    Iterable,
    ConcreteIterator,
    ConcreteIterable,
)
from .real_world_example import (
    BookCollection,
    BookIterator,
    ReverseBookIterator,
    FilteredBookIterator,
)

__all__ = [
    "Iterator",
    "Iterable",
    "ConcreteIterator",
    "ConcreteIterable",
    "BookCollection",
    "BookIterator", 
    "ReverseBookIterator",
    "FilteredBookIterator",
]
