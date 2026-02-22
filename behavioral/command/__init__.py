"""
Command Pattern (Behavioral)

Encapsulates a request as an object, thereby allowing you to parameterize 
clients with different requests, queue requests, and log requests.
"""

from .pattern import (
    Command,
    Receiver,
    Invoker,
    ConcreteCommand,
)
from .real_world_example import (
    TextEditor,
    TextEditorCommand,
    InsertTextCommand,
    DeleteTextCommand,
    UndoCommand,
    RedoCommand,
)

__all__ = [
    "Command",
    "Receiver",
    "Invoker",
    "ConcreteCommand",
    "TextEditor",
    "TextEditorCommand",
    "InsertTextCommand",
    "DeleteTextCommand",
    "UndoCommand",
    "RedoCommand",
]
