"""
Observer Pattern Implementation (Behavioral).

Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified automatically.

Key Components:
- Observer: Interface for receiving updates from the subject.
- Subject: Interface for registering and notifying observers.
- ConcreteObserver: Updates its state when notified by the subject.
- ConcreteSubject: Stores state and notifies observers when state changes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from datetime import datetime


class Observer(ABC):
    """
    Abstract observer that receives updates from a subject.
    
    Observers define the interface for receiving notifications from
    the subject about state changes.
    """

    @abstractmethod
    def update(self, subject: Subject, **kwargs: Any) -> None:
        """
        Receive an update from the subject.
        
        Args:
            subject: The subject that changed.
            **kwargs: Additional information about the change.
        """
        pass


class Subject(ABC):
    """
    Abstract subject that notifies observers of state changes.
    
    The subject maintains a list of observers and notifies them
    whenever its state changes.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        pass

    @abstractmethod
    def notify(self, **kwargs: Any) -> None:
        """Notify all observers about a state change."""
        pass


class ConcreteObserver(Observer):
    """
    Concrete observer that tracks subject state changes.
    
    Implements the observer interface and maintains a reference to
    the subject whose state it observes.
    """

    def __init__(self, name: str, subject: Subject) -> None:
        """
        Initialize the observer.
        
        Args:
            name: Identifier for this observer.
            subject: The subject to observe.
        """
        self.name = name
        self.subject = subject
        self.subject_state: Optional[Any] = None
        self.update_count: int = 0
        self.update_history: List[Dict[str, Any]] = []

    def update(self, subject: Subject, **kwargs: Any) -> None:
        """
        Receive update from subject.
        
        Args:
            subject: The subject that changed.
            **kwargs: Information about the change.
        """
        if subject is self.subject:
            self.subject_state = subject.get_state()
            self.update_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            update_info = {
                "timestamp": timestamp,
                "update_count": self.update_count,
                "state": self.subject_state,
                "extra_info": kwargs,
            }
            self.update_history.append(update_info)
            
            print(
                f"[{self.name}] Updated at {timestamp}: "
                f"Subject state = {self.subject_state}"
            )
            if kwargs:
                for key, value in kwargs.items():
                    print(f"           {key}: {value}")

    def get_update_count(self) -> int:
        """Get the number of updates received."""
        return self.update_count

    def get_last_update(self) -> Optional[Dict[str, Any]]:
        """Get information about the last update."""
        return self.update_history[-1] if self.update_history else None


class ConcreteSubject(Subject):
    """
    Concrete subject that maintains state and notifies observers.
    
    When the state changes, the subject automatically notifies all
    attached observers about the change.
    """

    def __init__(self, name: str, initial_state: Optional[Any] = None) -> None:
        """
        Initialize the subject.
        
        Args:
            name: Identifier for this subject.
            initial_state: Initial state of the subject.
        """
        self.name = name
        self._state = initial_state
        self._observers: List[Observer] = []
        self.state_change_log: List[Dict[str, Any]] = []

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to this subject.
        
        Args:
            observer: The observer to attach.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[Subject({self.name})] Attached observer: {observer}")

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from this subject.
        
        Args:
            observer: The observer to detach.
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[Subject({self.name})] Detached observer: {observer}")

    def notify(self, **kwargs: Any) -> None:
        """
        Notify all observers about a state change.
        
        Args:
            **kwargs: Additional information about the change.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.state_change_log.append({
            "timestamp": timestamp,
            "state": self._state,
            "observer_count": len(self._observers),
            "extra_info": kwargs,
        })
        
        print(f"\n[Subject({self.name})] Notifying {len(self._observers)} observer(s)...")
        for observer in self._observers:
            observer.update(self, **kwargs)

    def set_state(self, new_state: Any) -> None:
        """
        Set the subject's state and notify observers.
        
        Args:
            new_state: The new state value.
        """
        if self._state != new_state:
            old_state = self._state
            self._state = new_state
            print(
                f"[Subject({self.name})] State changed: {old_state} → {new_state}"
            )
            self.notify(old_state=old_state, new_state=new_state)

    def get_state(self) -> Any:
        """Get the current state of the subject."""
        return self._state

    def get_observer_count(self) -> int:
        """Get the number of attached observers."""
        return len(self._observers)

    def get_observers(self) -> List[Observer]:
        """Get a copy of the observers list."""
        return self._observers.copy()

    def get_state_change_log(self) -> List[Dict[str, Any]]:
        """Get the log of all state changes."""
        return self.state_change_log.copy()
