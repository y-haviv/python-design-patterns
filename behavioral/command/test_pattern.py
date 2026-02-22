"""
Comprehensive tests for the Command Pattern.

These tests verify:
1. Basic command execution and undo/redo.
2. Receiver state management.
3. Invoker history management.
4. Macro commands executing multiple operations.
5. Real-world text editor scenario.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Command,
    Receiver,
    ConcreteCommand,
    Invoker,
    MacroCommand,
)
from .real_world_example import (
    TextEditor,
    InsertTextCommand,
    DeleteTextCommand,
)


class TestReceiver:
    """Tests for the Receiver class."""

    def test_receiver_initialization(self) -> None:
        """Verify receiver initializes correctly."""
        receiver = Receiver("initial text")
        assert receiver.get_text() == "initial text"

    def test_insert_text(self) -> None:
        """Verify text insertion at various positions."""
        receiver = Receiver("Hello World")
        receiver.insert_text(5, " Beautiful")
        assert receiver.get_text() == "Hello Beautiful World"

    def test_insert_at_beginning(self) -> None:
        """Verify inserting at position 0."""
        receiver = Receiver("World")
        receiver.insert_text(0, "Hello ")
        assert receiver.get_text() == "Hello World"

    def test_insert_at_end(self) -> None:
        """Verify inserting at the end."""
        receiver = Receiver("Hello")
        receiver.insert_text(5, " World")
        assert receiver.get_text() == "Hello World"

    def test_delete_text(self) -> None:
        """Verify text deletion."""
        receiver = Receiver("Hello World")
        receiver.delete_text(5, 6)  # Delete " World"
        assert receiver.get_text() == "Hello"

    def test_delete_at_beginning(self) -> None:
        """Verify deleting at the start."""
        receiver = Receiver("Hello World")
        receiver.delete_text(0, 6)  # Delete "Hello "
        assert receiver.get_text() == "World"

    def test_invalid_insert_position(self) -> None:
        """Verify error on invalid insert position."""
        receiver = Receiver("Hello")
        with pytest.raises(ValueError):
            receiver.insert_text(10, "text")

    def test_invalid_delete_range(self) -> None:
        """Verify error on invalid delete range."""
        receiver = Receiver("Hello")
        with pytest.raises(ValueError):
            receiver.delete_text(0, 10)

    def test_copy_text(self) -> None:
        """Verify text copying to clipboard."""
        receiver = Receiver("Hello World")
        receiver.copy_text(0, 5)
        assert receiver.clipboard == "Hello"


class TestConcreteCommand:
    """Tests for ConcreteCommand implementation."""

    def test_command_execution(self) -> None:
        """Verify command executes on receiver."""
        receiver = Receiver("Hello")
        cmd = ConcreteCommand(receiver, "insert_text", 5, " World")
        cmd.execute()
        assert receiver.get_text() == "Hello World"

    def test_command_undo(self) -> None:
        """Verify command can be undone."""
        receiver = Receiver("Hello")
        cmd = ConcreteCommand(receiver, "insert_text", 5, " World")
        cmd.execute()
        assert receiver.get_text() == "Hello World"

        cmd.undo()
        assert receiver.get_text() == "Hello"

    def test_command_saves_state(self) -> None:
        """Verify command saves state before executing."""
        receiver = Receiver("initial")
        cmd = ConcreteCommand(receiver, "insert_text", 0, "pre_")
        assert cmd.previous_state is None

        cmd.execute()
        assert cmd.previous_state == "initial"


class TestInvoker:
    """Tests for the Invoker class."""

    def test_invoker_executes_command(self) -> None:
        """Verify invoker executes commands."""
        receiver = Receiver("Hello")
        invoker = Invoker()
        cmd = ConcreteCommand(receiver, "insert_text", 5, " World")

        invoker.execute_command(cmd)
        assert receiver.get_text() == "Hello World"
        assert invoker.get_history_size() == 1

    def test_undo_single_command(self) -> None:
        """Verify undoing a single command."""
        receiver = Receiver("Hello")
        invoker = Invoker()
        cmd = ConcreteCommand(receiver, "insert_text", 5, " World")

        invoker.execute_command(cmd)
        assert receiver.get_text() == "Hello World"

        success = invoker.undo()
        assert success is True
        assert receiver.get_text() == "Hello"

    def test_undo_multiple_commands(self) -> None:
        """Verify undoing multiple commands in sequence."""
        receiver = Receiver("start")
        invoker = Invoker()

        cmd1 = ConcreteCommand(receiver, "insert_text", 5, "1")
        cmd2 = ConcreteCommand(receiver, "insert_text", 6, "2")
        cmd3 = ConcreteCommand(receiver, "insert_text", 7, "3")

        invoker.execute_command(cmd1)
        invoker.execute_command(cmd2)
        invoker.execute_command(cmd3)
        assert receiver.get_text() == "start123"

        invoker.undo()
        assert receiver.get_text() == "start12"

        invoker.undo()
        assert receiver.get_text() == "start1"

        invoker.undo()
        assert receiver.get_text() == "start"

    def test_redo_command(self) -> None:
        """Verify redoing an undone command."""
        receiver = Receiver("Hello")
        invoker = Invoker()
        cmd = ConcreteCommand(receiver, "insert_text", 5, " World")

        invoker.execute_command(cmd)
        invoker.undo()
        assert receiver.get_text() == "Hello"

        success = invoker.redo()
        assert success is True
        assert receiver.get_text() == "Hello World"

    def test_undo_empty_history(self) -> None:
        """Verify undo on empty history returns False."""
        invoker = Invoker()
        assert invoker.undo() is False

    def test_redo_empty_redo_stack(self) -> None:
        """Verify redo on empty redo stack returns False."""
        invoker = Invoker()
        assert invoker.redo() is False

    def test_new_command_clears_redo_stack(self) -> None:
        """Verify executing new command clears redo stack."""
        receiver = Receiver("start")
        invoker = Invoker()

        cmd1 = ConcreteCommand(receiver, "insert_text", 5, "1")
        cmd2 = ConcreteCommand(receiver, "insert_text", 6, "2")

        invoker.execute_command(cmd1)
        invoker.undo()
        assert len(invoker.redo_stack) == 1

        invoker.execute_command(cmd2)
        assert len(invoker.redo_stack) == 0

    def test_history_max_size(self) -> None:
        """Verify history respects max_history limit."""
        receiver = Receiver("")
        invoker = Invoker(max_history=5)

        for i in range(10):
            cmd = ConcreteCommand(receiver, "insert_text", len(receiver.get_text()), str(i))
            invoker.execute_command(cmd)

        assert invoker.get_history_size() == 5

    def test_clear_history(self) -> None:
        """Verify clearing history and redo stack."""
        receiver = Receiver("test")
        invoker = Invoker()

        cmd1 = ConcreteCommand(receiver, "insert_text", 4, "1")
        cmd2 = ConcreteCommand(receiver, "insert_text", 5, "2")

        invoker.execute_command(cmd1)
        invoker.execute_command(cmd2)
        invoker.undo()

        assert invoker.get_history_size() == 1
        invoker.clear_history()
        assert invoker.get_history_size() == 0
        assert len(invoker.redo_stack) == 0


class TestMacroCommand:
    """Tests for the MacroCommand composite command."""

    def test_macro_command_executes_all_commands(self) -> None:
        """Verify macro command executes all contained commands."""
        receiver = Receiver("start")
        cmd1 = ConcreteCommand(receiver, "insert_text", 5, "1")
        cmd2 = ConcreteCommand(receiver, "insert_text", 6, "2")
        cmd3 = ConcreteCommand(receiver, "insert_text", 7, "3")

        macro = MacroCommand([cmd1, cmd2, cmd3])
        macro.execute()

        assert receiver.get_text() == "start123"

    def test_macro_command_undo(self) -> None:
        """Verify macro command can be undone."""
        receiver = Receiver("start")
        cmd1 = ConcreteCommand(receiver, "insert_text", 5, "1")
        cmd2 = ConcreteCommand(receiver, "insert_text", 6, "2")

        macro = MacroCommand([cmd1, cmd2])
        macro.execute()
        assert receiver.get_text() == "start12"

        macro.undo()
        assert receiver.get_text() == "start"

    def test_add_command_to_macro(self) -> None:
        """Verify adding commands to macro."""
        receiver = Receiver("")
        macro = MacroCommand()

        cmd1 = ConcreteCommand(receiver, "insert_text", 0, "A")
        cmd2 = ConcreteCommand(receiver, "insert_text", 1, "B")

        macro.add_command(cmd1)
        macro.add_command(cmd2)
        macro.execute()

        assert receiver.get_text() == "AB"

    def test_clear_macro(self) -> None:
        """Verify clearing commands from macro."""
        macro = MacroCommand()
        cmd1 = ConcreteCommand(Receiver(), "insert_text", 0, "A")
        cmd2 = ConcreteCommand(Receiver(), "insert_text", 1, "B")

        macro.add_command(cmd1)
        macro.add_command(cmd2)
        assert len(macro.commands) == 2

        macro.clear()
        assert len(macro.commands) == 0


class TestTextEditorExample:
    """Tests for the real-world text editor example."""

    def test_insert_command(self) -> None:
        """Verify insert text command."""
        editor = TextEditor("Hello")
        cmd = InsertTextCommand(editor, 5, " World")
        cmd.execute()
        assert editor.get_text() == "Hello World"

    def test_delete_command(self) -> None:
        """Verify delete text command."""
        editor = TextEditor("Hello World")
        cmd = DeleteTextCommand(editor, 5, 6)
        cmd.execute()
        assert editor.get_text() == "Hello"

    def test_editor_undo_redo(self) -> None:
        """Verify editor undo/redo workflow."""
        editor = TextEditor("Hello")
        invoker = Invoker()

        cmd1 = InsertTextCommand(editor, 5, " World")
        invoker.execute_command(cmd1)
        assert editor.get_text() == "Hello World"

        cmd2 = DeleteTextCommand(editor, 0, 6)
        invoker.execute_command(cmd2)
        assert editor.get_text() == "World"

        invoker.undo()
        assert editor.get_text() == "Hello World"

        invoker.undo()
        assert editor.get_text() == "Hello"

        invoker.redo()
        assert editor.get_text() == "Hello World"

    def test_editor_document_stats(self) -> None:
        """Verify editor statistics calculation."""
        editor = TextEditor("Hello World")
        stats = editor.get_document_stats()

        assert stats["total_characters"] == 11
        assert stats["total_words"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
