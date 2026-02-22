"""
Memento Pattern Implementation (Behavioral).

Capture and externalize an object's internal state without violating encapsulation.
The Memento pattern provides undo and save/restore functionality by creating snapshots
of object state that can be restored later.

Key Components:
- Memento: Stores internal state of Originator at a specific point in time.
- Originator: Creates mementos and restores itself from mementos.
- Caretaker: Keeps track of mementos (typically a history or stack).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from copy import deepcopy
from datetime import datetime


class Memento(ABC):
    """
    Abstract memento that stores the state of an originator.
    
    The interface is designed to prevent other objects from accessing
    the memento's state (white-box mementos expose state; black-box mementos hide it).
    """

    @abstractmethod
    def get_name(self) -> str:
        """Get a descriptive name for this memento."""
        pass

    @abstractmethod
    def get_date(self) -> str:
        """Get the creation date/time of this memento."""
        pass


class ConcreteMemento(Memento):
    """
    Concrete memento that stores internal state.
    
    In Python, we can make this accessible only to the Originator through
    name mangling or by using a simple class structure.
    """

    def __init__(self, state: dict[str, Any], name: str = "") -> None:
        """
        Initialize memento with state snapshot.
        
        Args:
            state: Dictionary containing the object's state.
            name: Optional descriptive name for this memento.
        """
        self._state = deepcopy(state)
        self._name = name
        self._date = datetime.now()

    def get_state(self) -> dict[str, Any]:
        """Get the stored state (protected access)."""
        return deepcopy(self._state)

    def get_name(self) -> str:
        """Get memento name."""
        return self._name or f"Snapshot at {self.get_date()}"

    def get_date(self) -> str:
        """Get memento creation timestamp."""
        return self._date.strftime("%Y-%m-%d %H:%M:%S")


class Originator:
    """
    The object whose state we want to capture.
    
    Creates mementos to save its current state and can restore itself
    from a previously saved memento.
    """

    def __init__(self) -> None:
        """Initialize originator with empty state."""
        self._state: dict[str, Any] = {}

    def set_state(self, state: dict[str, Any]) -> None:
        """Set the internal state."""
        self._state = deepcopy(state)

    def get_state(self) -> dict[str, Any]:
        """Get the current state."""
        return deepcopy(self._state)

    def create_memento(self, name: str = "") -> ConcreteMemento:
        """
        Create a memento of the current state.
        
        Args:
            name: Optional descriptive name for the memento.
            
        Returns:
            A memento object with the current state.
        """
        return ConcreteMemento(self._state, name)

    def restore_from_memento(self, memento: ConcreteMemento) -> None:
        """
        Restore state from a memento.
        
        Args:
            memento: The memento to restore from.
        """
        self._state = memento.get_state()


class Caretaker:
    """
    Manages mementos (history).
    
    Responsible for storing mementos and providing undo/redo functionality.
    Similar to the Invoker pattern but focused on state rather than commands.
    """

    def __init__(self, originator: Originator) -> None:
        """
        Initialize with the originator to manage.
        
        Args:
            originator: The object whose state we're managing.
        """
        self.originator = originator
        self.history: List[ConcreteMemento] = []
        self.current_index = -1

    def save(self, name: str = "") -> None:
        """
        Save the originator's current state.
        
        Args:
            name: Optional name for this save point.
        """
        # Remove any redo history when making a new save
        self.history = self.history[:self.current_index + 1]
        
        memento = self.originator.create_memento(name)
        self.history.append(memento)
        self.current_index = len(self.history) - 1

    def undo(self) -> bool:
        """
        Restore to the previous state.
        
        Returns:
            True if undo was successful, False if at beginning of history.
        """
        if self.current_index <= 0:
            return False

        self.current_index -= 1
        self.originator.restore_from_memento(self.history[self.current_index])
        return True

    def redo(self) -> bool:
        """
        Restore to the next state.
        
        Returns:
            True if redo was successful, False if at end of history.
        """
        if self.current_index >= len(self.history) - 1:
            return False

        self.current_index += 1
        self.originator.restore_from_memento(self.history[self.current_index])
        return True

    def jump_to(self, index: int) -> bool:
        """
        Jump to a specific point in history.
        
        Args:
            index: The history index to jump to.
            
        Returns:
            True if successful, False if index out of range.
        """
        if 0 <= index < len(self.history):
            self.current_index = index
            self.originator.restore_from_memento(self.history[self.current_index])
            return True
        return False

    def get_history(self) -> List[ConcreteMemento]:
        """Get all saved mementos."""
        return self.history.copy()

    def get_current_memento_name(self) -> str:
        """Get the name of the current memento."""
        if -1 < self.current_index < len(self.history):
            return self.history[self.current_index].get_name()
        return "No current state"

    def display_history(self) -> None:
        """Display the entire history."""
        print(f"\nHistory ({self.current_index + 1} of {len(self.history)}):")
        for i, memento in enumerate(self.history):
            marker = " ← Current" if i == self.current_index else ""
            print(f"  {i + 1}. {memento.get_name()} [{memento.get_date()}]{marker}")
