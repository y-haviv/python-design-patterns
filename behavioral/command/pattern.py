"""
Command Pattern Implementation (Behavioral).

Encapsulates a request as an object, allowing parameterization of clients 
with different requests, queueing, and logging. Enables undo/redo functionality
and decouples objects that produce commands from those that consume them.

Key Components:
- Command: Abstract interface for executing operations.
- ConcreteCommand: Implements the Command interface, binding an action 
  to a Receiver.
- Receiver: Performs the actual work requested by the command.
- Invoker: Asks the command to carry out the operation.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List
from datetime import datetime


class Command(ABC):
    """
    Abstract interface for commands.
    
    All concrete commands must implement the execute() method to perform
    their specific operations.
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the command's operation."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Undo the command's operation (optional but recommended)."""
        pass


class Receiver:
    """
    The object that performs the actual work.
    
    The Receiver contains the business logic for operations. Commands 
    delegate work to the Receiver rather than implementing logic themselves.
    
    Example:
        In a text editor, the Receiver might be the Document class that 
        knows how to insert and delete text.
    """

    def __init__(self, document_text: str = "") -> None:
        """Initialize the Receiver with optional initial content."""
        self.text = document_text
        self.clipboard = ""

    def insert_text(self, position: int, text: str) -> None:
        """Insert text at a specific position."""
        if position < 0 or position > len(self.text):
            raise ValueError(
                f"Invalid position {position}. Document length: {len(self.text)}"
            )
        self.text = self.text[:position] + text + self.text[position:]

    def delete_text(self, position: int, length: int) -> None:
        """Delete text at a specific position for a given length."""
        if position < 0 or position + length > len(self.text):
            raise ValueError(
                f"Invalid deletion range: position={position}, "
                f"length={length}, text_length={len(self.text)}"
            )
        self.text = self.text[:position] + self.text[position + length :]

    def copy_text(self, position: int, length: int) -> None:
        """Copy text to clipboard."""
        if position < 0 or position + length > len(self.text):
            raise ValueError("Invalid copy range")
        self.clipboard = self.text[position : position + length]

    def get_text(self) -> str:
        """Retrieve the current document text."""
        return self.text

    def get_text_at(self, position: int, length: int) -> str:
        """Get a substring at a specific position."""
        return self.text[position : position + length]


class ConcreteCommand(Command):
    """
    Concrete command that binds an action to a Receiver.
    
    The ConcreteCommand is responsible for associating a Receiver with 
    an action and calling the appropriate Receiver methods to execute 
    the operation.
    """

    def __init__(
        self, receiver: Receiver, action: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize command with receiver and arguments.
        
        Args:
            receiver: The object that will perform the work.
            action: The name of the method to call on the receiver.
            *args: Positional arguments for the action.
            **kwargs: Keyword arguments for the action.
        """
        self.receiver = receiver
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.previous_state = None

    def execute(self) -> None:
        """Execute the command by calling the appropriate receiver method."""
        # Save state before executing (for undo capability)
        self.previous_state = self.receiver.get_text()

        # Call the action on the receiver
        method = getattr(self.receiver, self.action)
        method(*self.args, **self.kwargs)

    def undo(self) -> None:
        """Undo the command by restoring the previous state."""
        if self.previous_state is not None:
            self.receiver.text = self.previous_state


class Invoker:
    """
    The object that invokes commands.
    
    The Invoker knows about the Command interface and invokes 
    commands without knowing their specific implementations. 
    Supports command history and undo/redo functionality.
    
    Attributes:
        history (List[Command]): Stack of executed commands for undo.
        redo_stack: Stack of undone commands for redo.
        max_history: Maximum number of commands to store (default: 100).
    """

    def __init__(self, max_history: int = 100) -> None:
        """
        Initialize the Invoker.
        
        Args:
            max_history: Maximum number of commands to keep in history.
        """
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
        self.max_history = max_history

    def execute_command(self, command: Command) -> None:
        """
        Execute a command and add it to history.
        
        Args:
            command: The command to execute.
        """
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()  # Clear redo stack on new command

        # Maintain max history size
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def undo(self) -> bool:
        """
        Undo the last command.
        
        Returns:
            True if undo was successful, False if history is empty.
        """
        if not self.history:
            return False

        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """
        Redo the last undone command.
        
        Returns:
            True if redo was successful, False if redo stack is empty.
        """
        if not self.redo_stack:
            return False

        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)
        return True

    def get_history(self) -> List[str]:
        """
        Get a string representation of command history.
        
        Returns:
            List of command descriptions.
        """
        return [
            f"{i + 1}. {cmd.action} at {getattr(cmd, 'timestamp', 'unknown')}"
            for i, cmd in enumerate(self.history)
        ]

    def clear_history(self) -> None:
        """Clear all command history and redo stack."""
        self.history.clear()
        self.redo_stack.clear()

    def get_history_size(self) -> int:
        """Return the number of commands in history."""
        return len(self.history)


class MacroCommand(Command):
    """
    Composite command that executes a sequence of commands.
    
    Useful for creating complex operations from simpler ones, or 
    recording and replaying sequences of commands.
    """

    def __init__(self, commands: List[Command] | None = None) -> None:
        """
        Initialize with optional list of commands.
        
        Args:
            commands: Initial sequence of commands to execute.
        """
        self.commands = commands or []

    def add_command(self, command: Command) -> None:
        """Add a command to the macro."""
        self.commands.append(command)

    def remove_command(self, command: Command) -> None:
        """Remove a command from the macro."""
        self.commands.remove(command)

    def execute(self) -> None:
        """Execute all commands in sequence."""
        for command in self.commands:
            command.execute()

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self.commands):
            command.undo()

    def clear(self) -> None:
        """Remove all commands from the macro."""
        self.commands.clear()
