"""
Real-World Example: Chat Room Implementation.

Demonstrates how a chat room mediates communication between multiple users
without them knowing about each other directly.
"""

from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from .pattern import Colleague, Mediator


class User(Colleague):
    """Represents a user in the chat room."""

    def __init__(self, name: str, chat_room: ChatMediator) -> None:
        """Initialize user."""
        super().__init__(name, chat_room)
        self.message_history: List[str] = []

    def send(self, message: str, recipient: Optional[str] = None) -> None:
        """Send a message to another user or broadcast."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if recipient:
            print(f"[{timestamp}] {self.name} → {recipient}: {message}")
        else:
            print(f"[{timestamp}] {self.name} (broadcast): {message}")
        
        self.mediator.send_message(message, self, recipient)

    def receive(self, message: str, sender: str) -> None:
        """Receive a message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {sender}: {message}"
        self.message_history.append(formatted_msg)
        print(f"    ↳ {self.name} received: {formatted_msg}")

    def get_message_count(self) -> int:
        """Get number of messages received."""
        return len(self.message_history)

    def display_history(self) -> None:
        """Display message history for this user."""
        print(f"\n=== Message history for {self.name} ===")
        if not self.message_history:
            print("  (no messages)")
        else:
            for msg in self.message_history:
                print(f"  {msg}")


class ChatMediator(Mediator):
    """
    Concrete chat room mediator.
    
    Coordinates communication between users. When a user sends a message,
    the chat room decides who receives it.
    """

    def __init__(self, name: str, max_users: int = 100) -> None:
        """
        Initialize the chat room.
        
        Args:
            name: Name of the chat room.
            max_users: Maximum number of users allowed.
        """
        self.name = name
        self.users: dict = {}
        self.max_users = max_users
        self.message_log: List[dict] = []
        self.created_at = datetime.now()

    def register_colleague(self, colleague: Colleague) -> None:
        """Register a user to join the chat room."""
        if len(self.users) >= self.max_users:
            print(f"[{self.name}] Chat room is full!")
            return

        if colleague.name not in self.users:
            self.users[colleague.name] = colleague
            # Announce user joining
            self._broadcast_system_message(f"{colleague.name} joined the chat")
            print(f"[{self.name}] User '{colleague.name}' joined")

    def send_message(
        self,
        message: str,
        sender: Colleague,
        recipient: Optional[str] = None
    ) -> None:
        """Send a message from one user to recipient(s)."""
        timestamp = datetime.now()
        
        self.message_log.append({
            "sender": sender.name,
            "recipient": recipient or "broadcast",
            "message": message,
            "timestamp": timestamp,
        })

        if recipient:
            # Direct message
            if recipient in self.users and recipient != sender.name:
                self.users[recipient].receive(message, sender.name)
            elif recipient == sender.name:
                print(f"    ↳ Cannot send message to yourself")
        else:
            # Broadcast
            for username, user in self.users.items():
                if username != sender.name:
                    user.receive(message, sender.name)

    def _broadcast_system_message(self, message: str) -> None:
        """Send a system message to all users."""
        for user in self.users.values():
            user.message_history.append(f"[SYSTEM]: {message}")

    def remove_user(self, username: str) -> None:
        """Remove a user from the chat room."""
        if username in self.users:
            del self.users[username]
            self._broadcast_system_message(f"{username} left the chat")
            print(f"[{self.name}] User '{username}' left")

    def get_active_users(self) -> List[str]:
        """Get list of active users."""
        return list(self.users.keys())

    def get_active_user_count(self) -> int:
        """Get number of active users."""
        return len(self.users)

    def get_message_count(self) -> int:
        """Get total number of messages."""
        return len(self.message_log)

    def display_statistics(self) -> None:
        """Display chat room statistics."""
        print(f"\n=== '{self.name}' Statistics ===")
        print(f"Active users: {self.get_active_user_count()}")
        print(f"Total messages: {self.get_message_count()}")
        print(f"Users online: {', '.join(self.get_active_users())}")
        uptime = datetime.now() - self.created_at
        print(f"Uptime: {uptime.total_seconds():.0f} seconds")


def demonstrate_chat_room() -> None:
    """Demonstrate the chat room mediator pattern."""
    
    # Create chat room
    chat = ChatMediator("Python Developers", max_users=10)
    
    # Create users
    alice = User("Alice", chat)
    bob = User("Bob", chat)
    charlie = User("Charlie", chat)
    diana = User("Diana", chat)
    
    # Register users
    chat.register_colleague(alice)
    chat.register_colleague(bob)
    chat.register_colleague(charlie)
    chat.register_colleague(diana)
    
    print("\n=== Chat Room Interactions ===\n")
    
    # Broadcast messages
    alice.send("Hello everyone!")
    bob.send("Hey Alice!")
    charlie.send("Welcome to the chat!")
    
    # Direct messages
    print()
    diana.send("Bob, can you help with Python?", "Bob")
    bob.send("Sure Diana, what do you need?", "Diana")
    
    # More interaction
    print()
    alice.send("Anyone doing machine learning?")
    charlie.send("Yes, working on some TensorFlow projects")
    
    # Display statistics
    chat.display_statistics()
    
    # Show message history for one user
    alice.display_history()
