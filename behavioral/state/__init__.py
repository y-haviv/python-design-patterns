"""
State Pattern (Behavioral)

Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class. This pattern lets you change
behavior without modifying the object's class directly.
"""

from .pattern import (
    ConcreteStateA,
    ConcreteStateB,
    ConcreteStateC,
    Context,
    State,
)
from .real_world_example import (
    TCPClosed,
    TCPConnection,
    TCPEstablished,
    TCPListen,
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
