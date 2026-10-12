"""
Mediator Pattern (Behavioral)

Define an object that encapsulates how a set of objects interact. The Mediator
pattern promotes loose coupling by keeping objects from referring to each other
explicitly, and it lets you vary their interaction independently.
"""

from .pattern import (
    Colleague,
    ConcreteColleague,
    ConcreteMediator,
    Mediator,
)
from .real_world_example import (
    ChatMediator,
    User,
)

__all__ = [
    "ChatMediator",
    "Colleague",
    "ConcreteColleague",
    "ConcreteMediator",
    "Mediator",
    "User",
]
