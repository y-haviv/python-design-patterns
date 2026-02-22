"""
Real-World Example: Text Editor with Undo/Redo via Command Pattern.

This example demonstrates a practical text editor that uses the Command 
pattern to implement undo/redo functionality, allowing users to reverse 
and reapply their changes at any point.
"""

from __future__ import annotations
from typing import List, Optional
from .pattern import Command, Receiver, Invoker, ConcreteCommand
from datetime import datetime


class TextEditor(Receiver):
    """
    Text editor document that performs actual text operations.
    
    Acts as the Receiver in the Command pattern. All text 
    modifications happen through explicitly defined methods 
    that can be called by commands.
    """

    def __init__(self, initial_text: str = "") -> None:
        """Initialize the text editor."""
        super().__init__(initial_text)
        self.history_log: List[str] = []

    def insert_text(self, position: int, text_to_insert: str) -> None:
        """Insert text and log the action."""
        super().insert_text(position, text_to_insert)
        self.history_log.append(
            f"Inserted '{text_to_insert}' at position {position}"
        )

    def delete_text(self, position: int, length: int) -> None:
        """Delete text and log the action."""
        super().delete_text(position, length)
        self.history_log.append(
            f"Deleted {length} characters at position {position}"
        )

    def display_document(self) -> str:
        """Get a view of the document with line numbers."""
        lines = self.text.split("\n")
        result = []
        for i, line in enumerate(lines, 1):
            result.append(f"{i:3d}: {line}")
        return "\n".join(result)

    def get_document_stats(self) -> dict:
        """Return statistics about the document."""
        return {
            "total_characters": len(self.text),
            "total_lines": len(self.text.split("\n")),
            "total_words": len(self.text.split()),
            "total_operations": len(self.history_log),
        }


class TextEditorCommand(Command):
    """Base class for text editor-specific commands."""

    def __init__(self, editor: TextEditor) -> None:
        """Initialize with the editor (receiver)."""
        self.editor = editor
        self.timestamp = datetime.now()
        self.previous_state = ""

    def __str__(self) -> str:
        """String representation of the command."""
        return f"{self.__class__.__name__} at {self.timestamp.strftime('%H:%M:%S')}"


class InsertTextCommand(TextEditorCommand):
    """Command to insert text at a specific position."""

    def __init__(
        self, editor: TextEditor, position: int, text: str
    ) -> None:
        """
        Initialize insert command.
        
        Args:
            editor: The text editor to modify.
            position: Where to insert the text.
            text: The text to insert.
        """
        super().__init__(editor)
        self.position = position
        self.text = text

    def execute(self) -> None:
        """Execute the insert operation."""
        self.previous_state = self.editor.get_text()
        self.editor.insert_text(self.position, self.text)

    def undo(self) -> None:
        """Undo the insert operation."""
        if self.previous_state is not None:
            self.editor.text = self.previous_state


class DeleteTextCommand(TextEditorCommand):
    """Command to delete text from a specific position."""

    def __init__(
        self, editor: TextEditor, position: int, length: int
    ) -> None:
        """
        Initialize delete command.
        
        Args:
            editor: The text editor to modify.
            position: Where to start deleting.
            length: How many characters to delete.
        """
        super().__init__(editor)
        self.position = position
        self.length = length
        self.deleted_text = ""

    def execute(self) -> None:
        """Execute the delete operation."""
        self.previous_state = self.editor.get_text()
        self.deleted_text = self.editor.get_text_at(self.position, self.length)
        self.editor.delete_text(self.position, self.length)

    def undo(self) -> None:
        """Undo the delete operation by reinserting deleted text."""
        if self.previous_state is not None:
            self.editor.text = self.previous_state


class UndoCommand(TextEditorCommand):
    """Command to undo previous operations."""

    def __init__(self, editor: TextEditor, invoker: Invoker) -> None:
        """
        Initialize undo command.
        
        Args:
            editor: The text editor.
            invoker: The invoker managing command history.
        """
        super().__init__(editor)
        self.invoker = invoker

    def execute(self) -> None:
        """Execute undo operation."""
        self.invoker.undo()

    def undo(self) -> None:
        """Undo of undo is redo."""
        self.invoker.redo()


class RedoCommand(TextEditorCommand):
    """Command to redo previously undone operations."""

    def __init__(self, editor: TextEditor, invoker: Invoker) -> None:
        """
        Initialize redo command.
        
        Args:
            editor: The text editor.
            invoker: The invoker managing command history.
        """
        super().__init__(editor)
        self.invoker = invoker

    def execute(self) -> None:
        """Execute redo operation."""
        self.invoker.redo()

    def undo(self) -> None:
        """Undo of redo is undo."""
        self.invoker.undo()


def demonstrate_text_editor() -> None:
    """
    Demonstrate the text editor with command pattern.
    
    This shows how the editor can perform operations and undo/redo them.
    """
    # Create editor and invoker
    editor = TextEditor("Hello")
    invoker = Invoker(max_history=50)

    print("=== Text Editor with Undo/Redo Demo ===\n")
    print(f"Initial text: '{editor.get_text()}'")

    # Insert text
    cmd1 = InsertTextCommand(editor, 5, " World")
    invoker.execute_command(cmd1)
    print(f"After insert ' World': '{editor.get_text()}'")

    # Delete text
    cmd2 = DeleteTextCommand(editor, 0, 5)
    invoker.execute_command(cmd2)
    print(f"After delete 'Hello': '{editor.get_text()}'")

    # Insert again
    cmd3 = InsertTextCommand(editor, 0, "Hi")
    invoker.execute_command(cmd3)
    print(f"After insert 'Hi': '{editor.get_text()}'")

    # Undo once
    invoker.undo()
    print(f"After undo: '{editor.get_text()}'")

    # Undo again
    invoker.undo()
    print(f"After undo again: '{editor.get_text()}'")

    # Redo once
    invoker.redo()
    print(f"After redo: '{editor.get_text()}'")

    print(f"\nCommand history depth: {invoker.get_history_size()}")
    print(f"Document stats: {editor.get_document_stats()}")
