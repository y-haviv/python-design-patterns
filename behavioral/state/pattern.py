"""
State Pattern Implementation (Behavioral).

Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class.

Key Components:
- State: Defines an interface for behavior based on state.
- ConcreteState: Implements behavior for a specific state.
- Context: Maintains instance of ConcreteState that defines current behavior.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


class State(ABC):
    """
    Abstract state that defines behavior for a particular state.
    
    Different states define different behaviors. Each state knows how to
    handle transitions to other states.
    """

    @abstractmethod
    def on_enter(self, context: Context) -> None:
        """Called when entering this state."""
        pass

    @abstractmethod
    def on_exit(self, context: Context) -> None:
        """Called when exiting this state."""
        pass

    @abstractmethod
    def handle(self, context: Context) -> None:
        """Handle the primary action in this state."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this state."""
        pass


class Context:
    """
    Context that maintains state and delegates behavior to current state.
    
    The context maintains a reference to a ConcreteState object that defines
    the current state. The context delegates to the state object all state-specific
    behavior; state objects can access the context to trigger transitions.
    """

    def __init__(self, initial_state: State) -> None:
        """
        Initialize context with initial state.
        
        Args:
            initial_state: The initial state.
        """
        self._state = initial_state
        self.context_data: Dict[str, Any] = {}
        self.state_log: List[Dict[str, Any]] = []
        self._transition_count = 0
        self._record_state_change("initialization")
        self._state.on_enter(self)

    def set_state(self, new_state: State) -> None:
        """
        Transition to a new state.
        
        Args:
            new_state: The new state to transition to.
        """
        old_state_name = self._state.get_name()
        new_state_name = new_state.get_name()
        
        print(f"\n[Context] State transition: {old_state_name} → {new_state_name}")
        
        self._state.on_exit(self)
        self._state = new_state
        self._transition_count += 1
        self._record_state_change(f"transition_from_{old_state_name}")
        self._state.on_enter(self)

    def request(self) -> None:
        """
        Request the current state to handle the action.
        
        The behavior depends on the current state.
        """
        print(f"\n[Context] Handling request in state: {self._state.get_name()}")
        self._state.handle(self)

    def get_state(self) -> State:
        """Get the current state."""
        return self._state

    def get_state_name(self) -> str:
        """Get the name of the current state."""
        return self._state.get_name()

    def get_transition_count(self) -> int:
        """Get the number of state transitions that have occurred."""
        return self._transition_count

    def _record_state_change(self, reason: str) -> None:
        """Record a state change in the log."""
        self.state_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "state": self._state.get_name(),
            "reason": reason,
            "transition_count": self._transition_count,
        })

    def set_data(self, key: str, value: Any) -> None:
        """Store data in context."""
        self.context_data[key] = value

    def get_data(self, key: str) -> Optional[Any]:
        """Retrieve data from context."""
        return self.context_data.get(key)

    def get_state_log(self) -> List[Dict[str, Any]]:
        """Get the log of all state changes."""
        return self.state_log.copy()


class ConcreteStateA(State):
    """Concrete state A with specific behavior."""

    def on_enter(self, context: Context) -> None:
        """Called when entering state A."""
        print("  → Entering State A")

    def on_exit(self, context: Context) -> None:
        """Called when exiting state A."""
        print("  ← Exiting State A")

    def handle(self, context: Context) -> None:
        """Handle request in state A."""
        print("  [State A] Processing request...")
        print("  [State A] Performing action specific to State A")
        print("  [State A] Ready to transition to State B")

    def get_name(self) -> str:
        """Get state name."""
        return "State A"


class ConcreteStateB(State):
    """Concrete state B with specific behavior."""

    def on_enter(self, context: Context) -> None:
        """Called when entering state B."""
        print("  → Entering State B")

    def on_exit(self, context: Context) -> None:
        """Called when exiting state B."""
        print("  ← Exiting State B")

    def handle(self, context: Context) -> None:
        """Handle request in state B."""
        print("  [State B] Processing request...")
        print("  [State B] Performing action specific to State B")
        print("  [State B] Ready to transition to State C")

    def get_name(self) -> str:
        """Get state name."""
        return "State B"


class ConcreteStateC(State):
    """Concrete state C with specific behavior."""

    def on_enter(self, context: Context) -> None:
        """Called when entering state C."""
        print("  → Entering State C")

    def on_exit(self, context: Context) -> None:
        """Called when exiting state C."""
        print("  ← Exiting State C")

    def handle(self, context: Context) -> None:
        """Handle request in state C."""
        print("  [State C] Processing request...")
        print("  [State C] Performing action specific to State C")
        print("  [State C] Ready to transition back to State A")

    def get_name(self) -> str:
        """Get state name."""
        return "State C"
