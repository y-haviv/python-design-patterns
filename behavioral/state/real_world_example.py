"""
Real-World Example: TCP Connection State Machine.

Demonstrates how different TCP connection states have different behaviors.
TCPConnection transitions through states like Listen, Established, and Closed
depending on the operations performed on it.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from .pattern import State, Context


class TCPState(State):
    """Base class for TCP connection states."""

    def __init__(self) -> None:
        """Initialize TCP state."""
        self.entry_time: Optional[datetime] = None
        self.exit_time: Optional[datetime] = None

    def on_enter(self, context: Context) -> None:
        """Record entry time."""
        self.entry_time = datetime.now()

    def on_exit(self, context: Context) -> None:
        """Record exit time."""
        self.exit_time = datetime.now()


class TCPClosed(TCPState):
    """
    TCP closed state.
    
    The connection is closed and can be opened.
    """

    def on_enter(self, context: Context) -> None:
        """Called when entering closed state."""
        super().on_enter(context)
        connection = context.get_data("connection")
        if connection:
            print(f"  → [{connection.name}] Entering CLOSED state")

    def on_exit(self, context: Context) -> None:
        """Called when leaving closed state."""
        connection = context.get_data("connection")
        if connection:
            print(f"  ← [{connection.name}] Leaving CLOSED state")
        super().on_exit(context)

    def handle(self, context: Context) -> None:
        """Handle actions in closed state."""
        print("  [CLOSED] Connection is closed")

    def open(self, context: Context, connection: TCPConnection) -> None:
        """Open the connection - transition to LISTEN state."""
        print(f"  [CLOSED] Opening connection...")
        context.set_state(TCPListen())

    def get_name(self) -> str:
        """Get state name."""
        return "CLOSED"


class TCPListen(TCPState):
    """
    TCP listen state.
    
    Connection is listening for incoming connections.
    """

    def on_enter(self, context: Context) -> None:
        """Called when entering listen state."""
        super().on_enter(context)
        connection = context.get_data("connection")
        if connection:
            print(f"  → [{connection.name}] Entering LISTEN state")
            connection.listening = True

    def on_exit(self, context: Context) -> None:
        """Called when leaving listen state."""
        connection = context.get_data("connection")
        if connection:
            connection.listening = False
            print(f"  ← [{connection.name}] Leaving LISTEN state")
        super().on_exit(context)

    def handle(self, context: Context) -> None:
        """Handle actions in listen state."""
        print("  [LISTEN] Waiting for incoming connections...")

    def send_syn_ack(self, context: Context, connection: TCPConnection) -> None:
        """Send SYN-ACK and transition to ESTABLISHED state."""
        print(f"  [LISTEN] Received connection request, sending SYN-ACK...")
        context.set_state(TCPEstablished())

    def close(self, context: Context, connection: TCPConnection) -> None:
        """Close the connection - transition to CLOSED state."""
        print(f"  [LISTEN] Closing connection...")
        context.set_state(TCPClosed())

    def get_name(self) -> str:
        """Get state name."""
        return "LISTEN"


class TCPEstablished(TCPState):
    """
    TCP established state.
    
    Connection is active and data can be transferred.
    """

    def on_enter(self, context: Context) -> None:
        """Called when entering established state."""
        super().on_enter(context)
        connection = context.get_data("connection")
        if connection:
            print(f"  → [{connection.name}] Entering ESTABLISHED state")
            connection.established = True
            connection.connected_at = datetime.now()

    def on_exit(self, context: Context) -> None:
        """Called when leaving established state."""
        connection = context.get_data("connection")
        if connection:
            connection.established = False
            print(f"  ← [{connection.name}] Leaving ESTABLISHED state")
        super().on_exit(context)

    def handle(self, context: Context) -> None:
        """Handle actions in established state."""
        print("  [ESTABLISHED] Connection is active, can send/receive data")

    def send(self, context: Context, connection: TCPConnection, data: str) -> None:
        """Send data over the connection."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [ESTABLISHED] Sending data: {data}")
        connection.send_log.append({
            "timestamp": timestamp,
            "data": data,
            "size": len(data),
        })

    def receive(self, context: Context, connection: TCPConnection, data: str) -> None:
        """Receive data on the connection."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [ESTABLISHED] Received data: {data}")
        connection.receive_log.append({
            "timestamp": timestamp,
            "data": data,
            "size": len(data),
        })

    def close(self, context: Context, connection: TCPConnection) -> None:
        """Close the connection - transition to CLOSED state."""
        print(f"  [ESTABLISHED] Initiating close sequence...")
        context.set_state(TCPClosed())

    def get_name(self) -> str:
        """Get state name."""
        return "ESTABLISHED"


class TCPConnection:
    """
    Represents a TCP connection with state-dependent behavior.
    
    The connection delegates operations to its current state, allowing
    different behaviors in different states.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a TCP connection.
        
        Args:
            name: Identifier for this connection.
        """
        self.name = name
        self.listening = False
        self.established = False
        self.connected_at: Optional[datetime] = None
        self.send_log: List[Dict[str, Any]] = []
        self.receive_log: List[Dict[str, Any]] = []
        
        # Create context with initial CLOSED state
        self.context = Context(TCPClosed())
        self.context.set_data("connection", self)

    def open(self) -> None:
        """Open the connection."""
        if isinstance(self.context.get_state(), TCPClosed):
            self.context.get_state().open(self.context, self)  # type: ignore
        else:
            print(f"[{self.name}] Cannot open: not in CLOSED state")

    def send_syn_ack(self) -> None:
        """Send SYN-ACK to establish connection."""
        if isinstance(self.context.get_state(), TCPListen):
            self.context.get_state().send_syn_ack(self.context, self)  # type: ignore
        else:
            print(f"[{self.name}] Cannot send SYN-ACK: not in LISTEN state")

    def send(self, data: str) -> None:
        """Send data on the connection."""
        if isinstance(self.context.get_state(), TCPEstablished):
            self.context.get_state().send(self.context, self, data)  # type: ignore
        else:
            print(f"[{self.name}] Cannot send: connection not established")

    def receive(self, data: str) -> None:
        """Receive data on the connection."""
        if isinstance(self.context.get_state(), TCPEstablished):
            self.context.get_state().receive(self.context, self, data)  # type: ignore
        else:
            print(f"[{self.name}] Cannot receive: connection not established")

    def close(self) -> None:
        """Close the connection."""
        current_state = self.context.get_state()
        if isinstance(current_state, (TCPListen, TCPEstablished)):
            current_state.close(self.context, self)  # type: ignore
        else:
            print(f"[{self.name}] Cannot close: already closed")

    def get_state(self) -> str:
        """Get the current connection state."""
        return self.context.get_state_name()

    def is_established(self) -> bool:
        """Check if connection is established."""
        return self.established

    def is_listening(self) -> bool:
        """Check if connection is listening."""
        return self.listening

    def get_connection_duration(self) -> Optional[float]:
        """Get duration of established connection in seconds."""
        if self.connected_at:
            return (datetime.now() - self.connected_at).total_seconds()
        return None

    def display_connection_info(self) -> None:
        """Display connection information."""
        print(f"\n=== Connection Info: {self.name} ===")
        print(f"  State: {self.get_state()}")
        print(f"  Established: {self.is_established()}")
        print(f"  Listening: {self.is_listening()}")
        
        if self.connected_at:
            duration = self.get_connection_duration()
            print(f"  Connection Duration: {duration:.2f}s")
        
        print(f"  Data Sent: {len(self.send_log)} messages")
        print(f"  Data Received: {len(self.receive_log)} messages")
        
        if self.send_log:
            print("  Last sent:")
            for entry in self.send_log[-3:]:
                print(f"    [{entry['timestamp']}] {entry['data']}")
        
        if self.receive_log:
            print("  Last received:")
            for entry in self.receive_log[-3:]:
                print(f"    [{entry['timestamp']}] {entry['data']}")
