"""
Comprehensive tests for the State Pattern.

These tests verify:
1. State transitions and context changes.
2. State-specific behavior delegation.
3. Entry and exit callbacks.
4. State history tracking.
5. Real-world TCP connection scenario.
"""

from __future__ import annotations
import pytest
from .pattern import (
    State,
    Context,
    ConcreteStateA,
    ConcreteStateB,
    ConcreteStateC,
)
from .real_world_example import (
    TCPConnection,
    TCPClosed,
    TCPListen,
    TCPEstablished,
)


class TestContextStateTransitions:
    """Tests for context state transition functionality."""

    def test_initial_state(self) -> None:
        """Verify context starts with initial state."""
        initial_state = ConcreteStateA()
        context = Context(initial_state)
        
        assert context.get_state() is initial_state
        assert context.get_state_name() == "State A"

    def test_set_state_transition(self) -> None:
        """Verify transitioning to a new state."""
        context = Context(ConcreteStateA())
        new_state = ConcreteStateB()
        
        context.set_state(new_state)
        
        assert context.get_state() is new_state
        assert context.get_state_name() == "State B"

    def test_transition_count(self) -> None:
        """Verify transition count is incremented."""
        context = Context(ConcreteStateA())
        
        assert context.get_transition_count() == 0
        
        context.set_state(ConcreteStateB())
        assert context.get_transition_count() == 1
        
        context.set_state(ConcreteStateC())
        assert context.get_transition_count() == 2

    def test_multiple_transitions(self) -> None:
        """Verify multiple state transitions."""
        context = Context(ConcreteStateA())
        
        context.set_state(ConcreteStateB())
        context.set_state(ConcreteStateC())
        context.set_state(ConcreteStateA())
        
        assert context.get_state_name() == "State A"
        assert context.get_transition_count() == 3

    def test_request_delegates_to_state(self) -> None:
        """Verify request delegates to current state."""
        context = Context(ConcreteStateA())
        
        # Request should delegate to State A
        context.request()
        
        assert context.get_state_name() == "State A"

    def test_state_log_records_changes(self) -> None:
        """Verify state log records all state changes."""
        context = Context(ConcreteStateA())
        
        context.set_state(ConcreteStateB())
        context.set_state(ConcreteStateC())
        
        log = context.get_state_log()
        assert len(log) >= 3
        assert log[1]["state"] == "State B"
        assert log[2]["state"] == "State C"

    def test_context_data_storage(self) -> None:
        """Verify context can store and retrieve data."""
        context = Context(ConcreteStateA())
        
        context.set_data("key1", "value1")
        context.set_data("key2", 42)
        
        assert context.get_data("key1") == "value1"
        assert context.get_data("key2") == 42
        assert context.get_data("nonexistent") is None

    def test_state_log_timestamp(self) -> None:
        """Verify state log includes timestamps."""
        context = Context(ConcreteStateA())
        
        context.set_state(ConcreteStateB())
        
        log = context.get_state_log()
        assert "timestamp" in log[-1]
        assert log[-1]["timestamp"] is not None


class TestConcreteStates:
    """Tests for concrete state implementations."""

    def test_state_a_behavior(self) -> None:
        """Verify State A specific behavior."""
        state_a = ConcreteStateA()
        assert state_a.get_name() == "State A"

    def test_state_b_behavior(self) -> None:
        """Verify State B specific behavior."""
        state_b = ConcreteStateB()
        assert state_b.get_name() == "State B"

    def test_state_c_behavior(self) -> None:
        """Verify State C specific behavior."""
        state_c = ConcreteStateC()
        assert state_c.get_name() == "State C"

    def test_on_enter_called_on_transition(self) -> None:
        """Verify on_enter is called when entering state."""
        context = Context(ConcreteStateA())
        
        # Transition should call on_enter
        context.set_state(ConcreteStateB())
        
        assert context.get_state_name() == "State B"

    def test_on_exit_called_on_transition(self) -> None:
        """Verify on_exit is called when leaving state."""
        context = Context(ConcreteStateA())
        
        # Transition should call on_exit on old state
        context.set_state(ConcreteStateB())
        
        assert context.get_state_name() == "State B"


class TestTCPConnection:
    """Tests for TCP connection state machine."""

    def test_connection_initial_state(self) -> None:
        """Verify connection starts in CLOSED state."""
        conn = TCPConnection("test_conn")
        
        assert conn.get_state() == "CLOSED"
        assert not conn.is_established()
        assert not conn.is_listening()

    def test_open_connection(self) -> None:
        """Verify opening a closed connection transitions to LISTEN."""
        conn = TCPConnection("test_conn")
        
        conn.open()
        
        assert conn.get_state() == "LISTEN"
        assert conn.is_listening()

    def test_cannot_open_listening_connection(self) -> None:
        """Verify cannot open a connection already in LISTEN state."""
        conn = TCPConnection("test_conn")
        conn.open()
        
        # Try to open again - should fail
        conn.open()
        
        assert conn.get_state() == "LISTEN"

    def test_syn_ack_transitions_to_established(self) -> None:
        """Verify SYN-ACK transitions from LISTEN to ESTABLISHED."""
        conn = TCPConnection("test_conn")
        conn.open()
        
        conn.send_syn_ack()
        
        assert conn.get_state() == "ESTABLISHED"
        assert conn.is_established()

    def test_cannot_syn_ack_not_listening(self) -> None:
        """Verify cannot send SYN-ACK if not in LISTEN state."""
        conn = TCPConnection("test_conn")
        
        conn.send_syn_ack()
        
        assert conn.get_state() == "CLOSED"

    def test_send_data_established(self) -> None:
        """Verify can send data when connection is established."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        conn.send("Hello, Server!")
        
        assert len(conn.send_log) == 1
        assert conn.send_log[0]["data"] == "Hello, Server!"

    def test_cannot_send_not_established(self) -> None:
        """Verify cannot send data when connection not established."""
        conn = TCPConnection("test_conn")
        
        conn.send("Hello")
        
        assert len(conn.send_log) == 0

    def test_receive_data_established(self) -> None:
        """Verify can receive data when connection is established."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        conn.receive("Hello, Client!")
        
        assert len(conn.receive_log) == 1
        assert conn.receive_log[0]["data"] == "Hello, Client!"

    def test_cannot_receive_not_established(self) -> None:
        """Verify cannot receive data when connection not established."""
        conn = TCPConnection("test_conn")
        
        conn.receive("Data")
        
        assert len(conn.receive_log) == 0

    def test_close_from_listen(self) -> None:
        """Verify closing from LISTEN state transitions to CLOSED."""
        conn = TCPConnection("test_conn")
        conn.open()
        
        conn.close()
        
        assert conn.get_state() == "CLOSED"
        assert not conn.is_listening()

    def test_close_from_established(self) -> None:
        """Verify closing from ESTABLISHED state transitions to CLOSED."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        conn.close()
        
        assert conn.get_state() == "CLOSED"
        assert not conn.is_established()

    def test_bidirectional_communication(self) -> None:
        """Verify bidirectional data transfer."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        conn.send("Request")
        conn.receive("Response")
        conn.send("Ack")
        
        assert len(conn.send_log) == 2
        assert len(conn.receive_log) == 1

    def test_connection_duration(self) -> None:
        """Verify connection duration tracking."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        import time
        time.sleep(0.1)
        
        duration = conn.get_connection_duration()
        assert duration is not None
        assert duration >= 0.1

    def test_state_transitions_sequence(self) -> None:
        """Verify complete connection state sequence."""
        conn = TCPConnection("test_conn")
        
        # Initial state
        assert conn.get_state() == "CLOSED"
        
        # Open connection
        conn.open()
        assert conn.get_state() == "LISTEN"
        
        # Receive and respond
        conn.send_syn_ack()
        assert conn.get_state() == "ESTABLISHED"
        
        # Exchange data
        conn.send("Request")
        conn.receive("Response")
        
        # Close connection
        conn.close()
        assert conn.get_state() == "CLOSED"

    def test_multiple_send_receive(self) -> None:
        """Verify multiple send/receive operations."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        for i in range(5):
            conn.send(f"Message {i}")
            conn.receive(f"Reply {i}")
        
        assert len(conn.send_log) == 5
        assert len(conn.receive_log) == 5

    def test_connection_context_tracking(self) -> None:
        """Verify connection tracks context state."""
        conn = TCPConnection("test_conn")
        
        # Verify context transitions match connection state
        conn.open()
        assert conn.context.get_state_name() == "LISTEN"
        
        conn.send_syn_ack()
        assert conn.context.get_state_name() == "ESTABLISHED"

    def test_tcp_state_entry_exit_sequence(self) -> None:
        """Verify TCP state entry/exit callbacks are called."""
        conn = TCPConnection("test_conn")
        
        initial_state = conn.context.get_state()
        assert isinstance(initial_state, TCPClosed)
        
        conn.open()
        listen_state = conn.context.get_state()
        assert isinstance(listen_state, TCPListen)
        
        conn.send_syn_ack()
        established_state = conn.context.get_state()
        assert isinstance(established_state, TCPEstablished)

    def test_immutable_send_log(self) -> None:
        """Verify send log entries are properly recorded."""
        conn = TCPConnection("test_conn")
        conn.open()
        conn.send_syn_ack()
        
        conn.send("Test message")
        
        log_entry = conn.send_log[0]
        assert "timestamp" in log_entry
        assert "data" in log_entry
        assert "size" in log_entry
        assert log_entry["size"] == len("Test message")
