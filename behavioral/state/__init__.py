"""
State Pattern (Behavioral)

Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class. This pattern lets you change
behavior without modifying the object's class directly.
"""

from .pattern import (
    State,
    Context,
    ConcreteStateA,
    ConcreteStateB,
    ConcreteStateC,
)
from .real_world_example import (
    TCPConnection,
    TCPListen,
    TCPEstablished,
    TCPClosed,
)

__all__ = [
    "State",
    "Context",
    "ConcreteStateA",
    "ConcreteStateB",
    "ConcreteStateC",
    "TCPConnection",
    "TCPListen",
    "TCPEstablished",
    "TCPClosed",
]
