"""
Memento Pattern (Behavioral)

Capture and externalize an object's internal state without violating encapsulation,
and allow restoring the object to this state later without triggering side effects.
"""

from .pattern import (
    Memento,
    Originator,
    Caretaker,
)
from .real_world_example import (
    TextDocument,
    DocumentMemento,
    DocumentHistory,
)

__all__ = [
    "Memento",
    "Originator",
    "Caretaker",
    "TextDocument",
    "DocumentMemento",
    "DocumentHistory",
]
