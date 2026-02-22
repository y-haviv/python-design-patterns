"""
Comprehensive tests for the Memento Pattern.

These tests verify:
1. State capture and restoration.
2. Undo/redo functionality.
3. History management.
4. Memento encapsulation.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Memento,
    Originator,
    Caretaker,
    ConcreteMemento,
)
from .real_world_example import (
    TextDocument,
    DocumentHistory,
)


class TestMemento:
    """Tests for memento functionality."""

    def test_memento_creation(self) -> None:
        """Verify memento captures state."""
        originator = Originator()
        originator.set_state({"name": "Test", "value": 42})
        
        memento = originator.create_memento("Test Snapshot")
        
        assert memento.get_name() == "Test Snapshot"
        assert memento.get_state() == {"name": "Test", "value": 42}

    def test_state_isolation(self) -> None:
        """Verify memento state is isolated (deepcopy)."""
        originator = Originator()
        state = {"list": [1, 2, 3]}
        originator.set_state(state)
        
        memento = originator.create_memento()
        
        # Modify original state
        originator._state["list"].append(4)
        
        # Memento should be unaffected
        assert memento.get_state()["list"] == [1, 2, 3]


class TestOriginator:
    """Tests for originator state management."""

    def test_set_and_get_state(self) -> None:
        """Verify setting and getting state."""
        originator = Originator()
        state = {"key": "value"}
        
        originator.set_state(state)
        assert originator.get_state() == state

    def test_restore_from_memento(self) -> None:
        """Verify restoring from memento."""
        originator = Originator()
        originator.set_state({"version": 1})
        
        memento1 = originator.create_memento()
        
        originator.set_state({"version": 2, "modified": True})
        memento2 = originator.create_memento()
        
        # Restore to first state
        originator.restore_from_memento(memento1)
        assert originator.get_state() == {"version": 1}
        
        # Restore to second state
        originator.restore_from_memento(memento2)
        assert originator.get_state() == {"version": 2, "modified": True}


class TestCaretaker:
    """Tests for caretaker (history management)."""

    def test_save_and_retrieve(self) -> None:
        """Verify saving and retrieving from history."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"value": 1})
        caretaker.save("State 1")
        
        originator.set_state({"value": 2})
        caretaker.save("State 2")
        
        history = caretaker.get_history()
        assert len(history) == 2

    def test_undo(self) -> None:
        """Verify undo functionality."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"step": 1})
        caretaker.save()
        
        originator.set_state({"step": 2})
        caretaker.save()
        
        caretaker.undo()
        assert originator.get_state() == {"step": 1}

    def test_redo(self) -> None:
        """Verify redo functionality."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"value": 1})
        caretaker.save()
        
        originator.set_state({"value": 2})
        caretaker.save()
        
        caretaker.undo()
        caretaker.redo()
        assert originator.get_state() == {"value": 2}

    def test_jump_to_version(self) -> None:
        """Verify jumping to specific version."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        for i in range(1, 5):
            originator.set_state({"version": i})
            caretaker.save()
        
        caretaker.jump_to(1)
        assert originator.get_state() == {"version": 2}

    def test_undo_at_beginning(self) -> None:
        """Verify undo at beginning returns False."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"value": 1})
        caretaker.save()
        
        assert caretaker.undo() is False

    def test_redo_at_end(self) -> None:
        """Verify redo at end returns False."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"value": 1})
        caretaker.save()
        
        assert caretaker.redo() is False

    def test_new_save_clears_redo_history(self) -> None:
        """Verify making new save clears redo history."""
        originator = Originator()
        caretaker = Caretaker(originator)
        
        originator.set_state({"value": 1})
        caretaker.save()
        
        originator.set_state({"value": 2})
        caretaker.save()
        
        caretaker.undo()
        assert len(caretaker.history) == 2
        
        originator.set_state({"value": 3})
        caretaker.save()
        
        # Should only have 2 items now (original + new)
        assert len(caretaker.history) == 2


class TestTextDocumentExample:
    """Tests for real-world text document example."""

    def test_document_creation(self) -> None:
        """Verify document creation."""
        doc = TextDocument("Test Document")
        assert doc.get_title() == "Test Document"
        assert doc.get_content() == ""

    def test_insert_text(self) -> None:
        """Verify text insertion."""
        doc = TextDocument()
        doc.insert_text("Hello")
        assert doc.get_content() == "Hello"

    def test_delete_text(self) -> None:
        """Verify text deletion."""
        doc = TextDocument()
        doc.insert_text("Hello World")
        doc.delete_text(5, 11)
        assert doc.get_content() == "Hello"

    def test_replace_text(self) -> None:
        """Verify text replacement."""
        doc = TextDocument()
        doc.insert_text("The cat is cat")
        doc.replace_text("cat", "dog")
        assert doc.get_content() == "The dog is dog"

    def test_document_save_restore(self) -> None:
        """Verify document save and restore."""
        doc = TextDocument("MyDoc")
        history = DocumentHistory(doc)
        
        doc.insert_text("Initial content")
        history.save_version("v1")
        
        doc.replace_text("content", "modified content")
        history.save_version("v2")
        
        history.undo()
        assert doc.get_content() == "Initial content"
        
        history.redo()
        assert doc.get_content() == "Initial modified content"

    def test_document_version_count(self) -> None:
        """Verify version count tracking."""
        doc = TextDocument()
        history = DocumentHistory(doc)
        
        for i in range(5):
            doc.insert_text(f"Line {i}\n")
            history.save_version(f"v{i + 1}")
        
        assert history.get_version_count() == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
