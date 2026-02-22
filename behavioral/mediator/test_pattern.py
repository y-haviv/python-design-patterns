"""
Comprehensive tests for the Mediator Pattern.

These tests verify:
1. Basic colleague registration and communication.
2. Broadcast and direct messaging.
3. Message history and logging.
4. Multiple mediators and colleagues.
5. Advanced filtering and routing (SmartMediator).
"""

from __future__ import annotations
import pytest
from .pattern import (
    Colleague,
    Mediator,
    ConcreteColleague,
    ConcreteMediator,
    SmartMediator,
)
from .real_world_example import (
    User,
    ChatMediator,
)


class TestConcreteMediator:
    """Tests for basic mediator functionality."""

    def test_register_colleague(self) -> None:
        """Verify registering colleagues."""
        mediator = ConcreteMediator()
        colleague1 = ConcreteColleague("User1", mediator)
        colleague2 = ConcreteColleague("User2", mediator)
        
        mediator.register_colleague(colleague1)
        mediator.register_colleague(colleague2)
        
        assert mediator.get_colleague_count() == 2
        assert mediator.get_colleague("User1") is colleague1

    def test_send_to_specific_colleague(self) -> None:
        """Verify sending message to a specific colleague."""
        mediator = ConcreteMediator()
        sender = ConcreteColleague("Sender", mediator)
        recipient = ConcreteColleague("Recipient", mediator)
        
        mediator.register_colleague(sender)
        mediator.register_colleague(recipient)
        
        mediator.send_message("Hello", sender, "Recipient")
        
        assert len(recipient.received_messages) == 1
        assert recipient.received_messages[0][0] == "Sender"
        assert recipient.received_messages[0][1] == "Hello"

    def test_broadcast_message(self) -> None:
        """Verify broadcasting message to all colleagues."""
        mediator = ConcreteMediator()
        sender = ConcreteColleague("Sender", mediator)
        colleague1 = ConcreteColleague("Colleague1", mediator)
        colleague2 = ConcreteColleague("Colleague2", mediator)
        
        mediator.register_colleague(sender)
        mediator.register_colleague(colleague1)
        mediator.register_colleague(colleague2)
        
        mediator.send_message("Broadcast message", sender, None)
        
        assert len(colleague1.received_messages) == 1
        assert len(colleague2.received_messages) == 1
        assert colleague1.received_messages[0][1] == "Broadcast message"

    def test_message_history(self) -> None:
        """Verify message logging."""
        mediator = ConcreteMediator()
        sender = ConcreteColleague("Sender", mediator)
        recipient = ConcreteColleague("Recipient", mediator)
        
        mediator.register_colleague(sender)
        mediator.register_colleague(recipient)
        
        mediator.send_message("Message 1", sender, "Recipient")
        mediator.send_message("Message 2", sender, None)
        
        history = mediator.get_message_history()
        assert len(history) == 2
        assert history[0]["message"] == "Message 1"
        assert history[1]["recipient"] == "All"

    def test_self_message_not_allowed(self) -> None:
        """Verify colleague cannot send to themselves."""
        mediator = ConcreteMediator()
        colleague = ConcreteColleague("User", mediator)
        mediator.register_colleague(colleague)
        
        mediator.send_message("Self message", colleague, "User")
        
        # Should not receive message from self
        assert len(colleague.received_messages) == 0

    def test_nonexistent_recipient(self) -> None:
        """Verify sending to nonexistent recipient."""
        mediator = ConcreteMediator()
        sender = ConcreteColleague("Sender", mediator)
        mediator.register_colleague(sender)
        
        # Should handle gracefully
        mediator.send_message("Message", sender, "NonExistent")
        assert True  # No error


class TestChatMediator:
    """Tests for real-world chat room example."""

    @pytest.fixture
    def chat_room(self) -> ChatMediator:
        """Create a test chat room."""
        return ChatMediator("Test Room", max_users=5)

    def test_user_joins_chat(self, chat_room: ChatMediator) -> None:
        """Verify user can join chat."""
        user = User("Alice", chat_room)
        chat_room.register_colleague(user)
        
        assert chat_room.get_active_user_count() == 1
        assert "Alice" in chat_room.get_active_users()

    def test_max_users_limit(self, chat_room: ChatMediator) -> None:
        """Verify max users limit is enforced."""
        users = [User(f"User{i}", chat_room) for i in range(6)]
        
        for user in users:
            chat_room.register_colleague(user)
        
        # Only 5 should be registered (due to max_users=5)
        assert chat_room.get_active_user_count() == 5

    def test_broadcast_in_chat(self, chat_room: ChatMediator) -> None:
        """Verify broadcast message in chat."""
        alice = User("Alice", chat_room)
        bob = User("Bob", chat_room)
        
        chat_room.register_colleague(alice)
        chat_room.register_colleague(bob)
        
        alice.send("Hello everyone!")
        
        # Bob should receive the message
        assert bob.get_message_count() >= 1

    def test_direct_message_in_chat(self, chat_room: ChatMediator) -> None:
        """Verify direct message in chat."""
        alice = User("Alice", chat_room)
        bob = User("Bob", chat_room)
        
        chat_room.register_colleague(alice)
        chat_room.register_colleague(bob)
        
        alice.send("Hi Bob", "Bob")
        
        assert bob.get_message_count() >= 1

    def test_user_leaves_chat(self, chat_room: ChatMediator) -> None:
        """Verify user can leave chat."""
        user = User("Alice", chat_room)
        chat_room.register_colleague(user)
        assert chat_room.get_active_user_count() == 1
        
        chat_room.remove_user("Alice")
        assert chat_room.get_active_user_count() == 0
        assert "Alice" not in chat_room.get_active_users()


class TestSmartMediator:
    """Tests for advanced mediator with filtering."""

    def test_smart_mediator_with_routing(self) -> None:
        """Verify routing rules in smart mediator."""
        smart_mediator = SmartMediator()
        
        sender = ConcreteColleague("Sender", smart_mediator)
        target = ConcreteColleague("Target", smart_mediator)
        alternative = ConcreteColleague("Alternative", smart_mediator)
        
        smart_mediator.register_colleague(sender)
        smart_mediator.register_colleague(target)
        smart_mediator.register_colleague(alternative)
        
        # Add routing rule: Sender's messages always go to Alternative
        smart_mediator.add_routing_rule("Sender", "Alternative")
        
        # Send message (intended for Target, but routed to Alternative)
        smart_mediator.send_message("Hello", sender, "Target")
        
        assert len(alternative.received_messages) == 1
        assert len(target.received_messages) == 0

    def test_smart_mediator_with_filter(self) -> None:
        """Verify message filtering in smart mediator."""
        smart_mediator = SmartMediator()
        
        sender = ConcreteColleague("Sender", smart_mediator)
        recipient = ConcreteColleague("Recipient", smart_mediator)
        
        smart_mediator.register_colleague(sender)
        smart_mediator.register_colleague(recipient)
        
        # Add filter: only allow messages containing "approved"
        smart_mediator.add_filter("Recipient", lambda msg: "approved" in msg.lower())
        
        # Send unapproved message
        smart_mediator.send_message("This is bad", sender, "Recipient")
        assert len(recipient.received_messages) == 0
        
        # Send approved message
        smart_mediator.send_message("This is approved", sender, "Recipient")
        assert len(recipient.received_messages) == 1


class TestMultipleMediators:
    """Tests for multiple independent mediators."""

    def test_multiple_chat_rooms(self) -> None:
        """Verify multiple independent chat rooms."""
        room1 = ChatMediator("Room1")
        room2 = ChatMediator("Room2")
        
        alice_in_room1 = User("Alice", room1)
        alice_in_room2 = User("Alice", room2)
        
        room1.register_colleague(alice_in_room1)
        room2.register_colleague(alice_in_room2)
        
        # Send message in room1 shouldn't affect room2
        alice_in_room1.send("Message in Room1")
        
        assert room1.get_message_count() >= 1
        assert room2.get_message_count() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
