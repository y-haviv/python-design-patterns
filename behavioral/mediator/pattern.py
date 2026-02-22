"""
Mediator Pattern Implementation (Behavioral).

Define an object that encapsulates how a set of objects interact. The Mediator
pattern lets objects communicate through a mediator rather than directly with
each other. This promotes loose coupling and simplifies complex interactions.

Key Components:
- Mediator: Abstract interface that defines interaction methods.
- ConcreteMediator: Centralized coordination logic for all colleagues.
- Colleague: Knows its mediator but not other colleagues.
- ConcreteColleague: Sends requests to mediator; receives notifications from mediator.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class Colleague(ABC):
    """
    Abstract colleague that interacts through a mediator.
    
    Colleagues don't interact directly with each other; they communicate
    exclusively through the mediator. This reduces coupling between colleagues.
    """

    def __init__(self, name: str, mediator: Mediator) -> None:
        """
        Initialize colleague with name and mediator.
        
        Args:
            name: Unique identifier for this colleague.
            mediator: The mediator that coordinates interactions.
        """
        self.name = name
        self.mediator = mediator

    @abstractmethod
    def send(self, message: str, recipient: Optional[str] = None) -> None:
        """Send a message through the mediator."""
        pass

    @abstractmethod
    def receive(self, message: str, sender: str) -> None:
        """Receive a message from another colleague through the mediator."""
        pass


class Mediator(ABC):
    """
    Abstract mediator that defines how colleagues interact.
    
    The mediator encapsulates the interaction logic, allowing colleagues
    to be decoupled from each other.
    """

    @abstractmethod
    def register_colleague(self, colleague: Colleague) -> None:
        """Register a colleague with this mediator."""
        pass

    @abstractmethod
    def send_message(
        self, message: str, sender: Colleague, recipient: Optional[Colleague] = None
    ) -> None:
        """Send a message from one colleague to another (or all)."""
        pass


class ConcreteColleague(Colleague):
    """
    Concrete colleague that communicates through the mediator.
    
    Knows about the mediator but not about other colleagues. All communication
    goes through the mediator.
    """

    def __init__(self, name: str, mediator: Mediator) -> None:
        """Initialize the colleague."""
        super().__init__(name, mediator)
        self.received_messages: List[tuple] = []

    def send(self, message: str, recipient: Optional[str] = None) -> None:
        """
        Send a message through the mediator.
        
        Args:
            message: The message content.
            recipient: Optional specific recipient (None for broadcast).
        """
        print(f"[{self.name}] sends: {message}")
        self.mediator.send_message(message, self, recipient)

    def receive(self, message: str, sender: str) -> None:
        """Receive a message from the mediator."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.received_messages.append((sender, message, timestamp))
        print(f"[{self.name}] receives from [{sender}] at {timestamp}: {message}")


class ConcreteMediator(Mediator):
    """
    Concrete mediator that implements the interaction logic.
    
    Maintains a list of colleagues and coordinates communication between them.
    This is where the complex interaction logic resides, centralizing it
    instead of scattering it across colleague classes.
    """

    def __init__(self) -> None:
        """Initialize the mediator."""
        self.colleagues: Dict[str, Colleague] = {}
        self.message_log: List[Dict[str, Any]] = []

    def register_colleague(self, colleague: Colleague) -> None:
        """
        Register a colleague with this mediator.
        
        Args:
            colleague: The colleague to register.
        """
        self.colleagues[colleague.name] = colleague
        print(f"[Mediator] Registered colleague: {colleague.name}")

    def send_message(
        self, 
        message: str, 
        sender: Colleague, 
        recipient: Optional[str] = None
    ) -> None:
        """
        Send a message from sender to recipient (or all colleagues).
        
        Args:
            message: The message content.
            sender: The sending colleague.
            recipient: Name of recipient colleague (None for broadcast).
        """
        timestamp = datetime.now()
        
        # Log the message
        self.message_log.append({
            "sender": sender.name,
            "recipient": recipient or "All",
            "message": message,
            "timestamp": timestamp,
        })

        if recipient:
            # Send to specific colleague
            if recipient in self.colleagues and recipient != sender.name:
                self.colleagues[recipient].receive(message, sender.name)
            elif recipient == sender.name:
                print(f"[Mediator] Cannot send message to yourself ({sender.name})")
            else:
                print(f"[Mediator] Recipient '{recipient}' not found")
        else:
            # Broadcast to all colleagues except sender
            for colleague_name, colleague in self.colleagues.items():
                if colleague_name != sender.name:
                    colleague.receive(message, sender.name)

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get the history of all messages processed by this mediator."""
        return self.message_log.copy()

    def get_colleague_count(self) -> int:
        """Get the number of registered colleagues."""
        return len(self.colleagues)

    def get_colleague(self, name: str) -> Optional[Colleague]:
        """Get a colleague by name."""
        return self.colleagues.get(name)


class SmartMediator(ConcreteMediator):
    """
    An advanced mediator with filtering, routing, and rule-based logic.
    
    Demonstrates how the mediator pattern allows for sophisticated
    interaction logic without modifying colleagues.
    """

    def __init__(self) -> None:
        """Initialize the smart mediator."""
        super().__init__()
        self.filters: Dict[str, callable] = {}
        self.routing_rules: Dict[str, str] = {}  # recipient mapping

    def add_filter(self, colleague_name: str, filter_func: callable) -> None:
        """
        Add a message filter for a colleague.
        
        The filter function receives a message and returns whether to deliver it.
        """
        self.filters[colleague_name] = filter_func

    def add_routing_rule(self, from_name: str, to_name: str) -> None:
        """Add a routing rule: messages from 'from_name' always go to 'to_name'."""
        self.routing_rules[from_name] = to_name

    def send_message(
        self,
        message: str,
        sender: Colleague,
        recipient: Optional[str] = None
    ) -> None:
        """Send with filtering and routing logic."""
        # Check routing rules
        actual_recipient = self.routing_rules.get(sender.name, recipient)

        if actual_recipient:
            # Check if recipient has a filter
            filter_func = self.filters.get(actual_recipient)
            if filter_func and not filter_func(message):
                print(f"[SmartMediator] Message blocked by filter for {actual_recipient}")
                return

        # Proceed with normal send
        super().send_message(message, sender, actual_recipient)
