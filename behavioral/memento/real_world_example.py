"""
Real-World Example: Text Document with Save History.

Demonstrates using the Memento pattern to implement document save/restore
and full undo/redo history without providing direct access to internal state.
"""

from __future__ import annotations
from typing import Optional
from datetime import datetime
from .pattern import Memento, Originator, Caretaker, ConcreteMemento


class DocumentMemento(Memento):
    """Memento specifically for text documents."""

    def __init__(self, content: str, title: str, timestamp: str) -> None:
        self._content = content
        self._title = title
        self._timestamp = timestamp

    @property
    def content(self) -> str:
        return self._content

    @property
    def title(self) -> str:
        return self._title

    def get_name(self) -> str:
        return f"'{self._title}' at {self._timestamp}"

    def get_date(self) -> str:
        return self._timestamp


class TextDocument(Originator):
    """A text document that can save and restore its state."""

    def __init__(self, title: str = "Untitled") -> None:
        super().__init__()
        self.title = title
        self.content = ""
        self.cursor_position = 0
        self.formatting = {}

    def insert_text(self, text: str, position: Optional[int] = None) -> None:
        """Insert text at a specific position."""
        if position is None:
            position = self.cursor_position
        
        self.content = (
            self.content[:position] + text + self.content[position:]
        )
        self.cursor_position = position + len(text)

    def delete_text(self, start: int, end: int) -> None:
        """Delete text from start to end."""
        self.content = self.content[:start] + self.content[end:]
        self.cursor_position = start

    def replace_text(self, old: str, new: str) -> None:
        """Replace all occurrences of old text with new text."""
        self.content = self.content.replace(old, new)

    def get_content(self) -> str:
        """Get the document content."""
        return self.content

    def get_title(self) -> str:
        """Get the document title."""
        return self.title

    def set_title(self, title: str) -> None:
        """Change the document title."""
        self.title = title

    def create_memento(self, name: str = "") -> DocumentMemento:
        """Create a snapshot of the document."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return DocumentMemento(self.content, self.title, timestamp)

    def restore_from_memento(self, memento: DocumentMemento) -> None:
        """Restore document from a memento."""
        self.content = memento.content
        self.title = memento.title

    def display(self) -> None:
        """Display the document content."""
        print(f"\n=== {self.title} ===")
        print(self.content if self.content else "(empty)")
        print(f"Cursor position: {self.cursor_position}")


class DocumentHistory(Caretaker):
    """Manages document save history."""

    def __init__(self, document: TextDocument) -> None:
        super().__init__(document)
        self.document = document

    def save_version(self, description: str = "") -> None:
        """Save current document state with optional description."""
        name = description or f"Version saved at {datetime.now().strftime('%H:%M:%S')}"
        memento = self.document.create_memento(name)
        self.history.append(memento)
        self.current_index = len(self.history) - 1
        print(f"Document saved: {name}")

    def get_version_count(self) -> int:
        """Get number of saved versions."""
        return len(self.history)

    def display_timeline(self) -> None:
        """Display document version timeline."""
        print(f"\n=== Document Timeline ===")
        if not self.history:
            print("  (no versions saved)")
            return
        
        for i, memento in enumerate(self.history, 1):
            marker = " ← Current" if i - 1 == self.current_index else ""
            print(f"  v{i}. {memento.get_name()}{marker}")

    def compare_versions(self, index1: int, index2: int) -> None:
        """Compare two versions."""
        if not (0 <= index1 < len(self.history)) or not (
            0 <= index2 < len(self.history)
        ):
            print("Invalid version indices")
            return

        mem1 = self.history[index1]
        mem2 = self.history[index2]

        print(f"\n=== Comparing Version {index1 + 1} vs {index2 + 1} ===")
        print(f"Version {index1 + 1}: {mem1.get_name()}")
        print(f"  Length: {len(mem1.content)} characters")
        print(f"Version {index2 + 1}: {mem2.get_name()}")
        print(f"  Length: {len(mem2.content)} characters")


def demonstrate_document_history() -> None:
    """Demonstrate text document with memento pattern."""
    
    # Create document
    doc = TextDocument("My Essay")
    history = DocumentHistory(doc)
    
    print("=== Text Document with Undo/Redo History ===\n")
    
    # Initial content
    doc.insert_text("The quick brown fox jumps over the lazy dog.")
    history.save_version("Initial draft")
    doc.display()
    
    # Edit 1
    doc.replace_text("quick", "clever")
    history.save_version("Changed adjective")
    doc.display()
    
    # Edit 2
    doc.replace_text("lazy", "sleepy")
    history.save_version("Changed adjective 2")
    doc.display()
    
    # Undo
    print("\n--- Undoing changes ---")
    history.undo()
    doc.display()
    
    # Undo again
    history.undo()
    doc.display()
    
    # Redo
    print("\n--- Redoing changes ---")
    history.redo()
    doc.display()
    
    # Display timeline
    history.display_timeline()
