"""
Mediator Pattern (Behavioral)

Define an object that encapsulates how a set of objects interact. The Mediator
pattern promotes loose coupling by keeping objects from referring to each other
explicitly, and it lets you vary their interaction independently.
"""

from .pattern import (
    Mediator,
    Colleague,
    ConcreteMediator,
    ConcreteColleague,
)
from .real_world_example import (
    ChatRoom,
    User,
    ChatMediator,
)

__all__ = [
    "Mediator",
    "Colleague",
    "ConcreteMediator",
    "ConcreteColleague",
    "ChatRoom",
    "User",
    "ChatMediator",
]
