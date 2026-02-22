"""
Factory Method Pattern - Structural Implementation.

This module demonstrates the Factory Method pattern using abstract base classes 
and metaclasses to enforce the pattern's contract. The Factory Method provides 
a way to create objects without specifying the exact classes that will be 
instantiated at compile time.

The pattern delegates object instantiation to factory methods defined in 
subclasses, allowing the type of objects created to be determined at runtime.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Any, Optional


class TransportType(Enum):
    """Enumeration of supported transport protocols."""
    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"
    WEBSOCKET = "websocket"


class Transport(ABC):
    """
    Abstract Product (Transport Protocol).
    
    Defines the interface that all concrete transports must implement.
    This ensures that clients can work with any transport type through 
    a common interface.
    """

    @abstractmethod
    def connect(self) -> str:
        """
        Establish a connection using this transport protocol.
        
        Returns:
            A string describing the connection state.
        """
        pass

    @abstractmethod
    def send_data(self, data: str) -> str:
        """
        Send data using this transport protocol.
        
        Args:
            data: The payload to transmit.
            
        Returns:
            Confirmation message of the transmission.
        """
        pass

    @abstractmethod
    def disconnect(self) -> str:
        """
        Close the connection gracefully.
        
        Returns:
            A string describing the disconnection.
        """
        pass


class HTTPTransport(Transport):
    """
    Concrete Product: HTTP Transport.
    
    Implements the Transport interface for HTTP (unencrypted) communication.
    """

    def __init__(self) -> None:
        self._connected = False

    def connect(self) -> str:
        """Simulate an HTTP connection (typically stateless)."""
        self._connected = True
        return "HTTP connection established on port 80 (stateless)"

    def send_data(self, data: str) -> str:
        """Send data via HTTP GET/POST request."""
        if not self._connected:
            return "Error: Not connected"
        return f"HTTP: Transmitting data: {data}"

    def disconnect(self) -> str:
        """Simulate HTTP disconnection."""
        self._connected = False
        return "HTTP connection closed"


class HTTPSTransport(Transport):
    """
    Concrete Product: HTTPS Transport.
    
    Implements the Transport interface for HTTPS (encrypted) communication.
    Uses SSL/TLS for secure data transmission.
    """

    def __init__(self) -> None:
        self._connected = False
        self._ssl_certificate = "cert_2048bit_RSA"

    def connect(self) -> str:
        """Establish a secure HTTPS connection with certificate verification."""
        self._connected = True
        return (
            f"HTTPS connection established on port 443 "
            f"(secured with {self._ssl_certificate})"
        )

    def send_data(self, data: str) -> str:
        """Send encrypted data via HTTPS."""
        if not self._connected:
            return "Error: Not connected"
        return f"HTTPS: Transmitting encrypted data: {data}"

    def disconnect(self) -> str:
        """Gracefully close the secure connection."""
        self._connected = False
        return "HTTPS connection closed (SSL/TLS session terminated)"


class FTPTransport(Transport):
    """
    Concrete Product: FTP Transport.
    
    Implements the Transport interface for FTP (File Transfer Protocol) 
    communication, suitable for bulk file transfers.
    """

    def __init__(self) -> None:
        self._connected = False
        self._user = "anonymous"

    def connect(self) -> str:
        """Establish an FTP connection with user authentication."""
        self._connected = True
        return f"FTP connection established on port 21 (user: {self._user})"

    def send_data(self, data: str) -> str:
        """Send file data via FTP."""
        if not self._connected:
            return "Error: Not connected"
        return f"FTP: Uploading file: {data}"

    def disconnect(self) -> str:
        """Close the FTP session."""
        self._connected = False
        return "FTP connection closed"


class WebSocketTransport(Transport):
    """
    Concrete Product: WebSocket Transport.
    
    Implements the Transport interface for WebSocket (bi-directional) 
    communication, enabling real-time, low-latency data exchange.
    """

    def __init__(self) -> None:
        self._connected = False
        self._ping_interval = 30  # seconds

    def connect(self) -> str:
        """Establish a persistent WebSocket connection."""
        self._connected = True
        return (
            f"WebSocket connection established on port 443/80 "
            f"(ping interval: {self._ping_interval}s)"
        )

    def send_data(self, data: str) -> str:
        """Send data via WebSocket frame."""
        if not self._connected:
            return "Error: Not connected"
        return f"WebSocket: Sending frame: {data} (real-time)"

    def disconnect(self) -> str:
        """Close the WebSocket connection gracefully."""
        self._connected = False
        return "WebSocket connection closed (close frame sent)"


class TransportFactory(ABC):
    """
    Abstract Creator (Factory).
    
    Declares the factory method that returns a Transport object.
    Subclasses override this method to create specific transport types.
    
    This abstraction allows client code to work with factories through 
    a common interface, promoting loose coupling between client and concrete types.
    """

    @abstractmethod
    def create_transport(self) -> Transport:
        """
        Factory method that creates and returns a Transport instance.
        
        Each concrete factory subclass implements this method to produce
        its specific transport type.
        
        Returns:
            A Transport instance (concrete type depends on factory subclass).
        """
        pass

    def communicate(self, message: str) -> str:
        """
        Template method: Uses the factory method to communicate via transport.
        
        This demonstrates how the factory method allows the base class 
        to defer the creation decision to subclasses while maintaining 
        a common workflow.
        
        Args:
            message: The message to transmit.
            
        Returns:
            A status string describing the communication result.
        """
        transport = self.create_transport()
        result = f"{transport.connect()}\n"
        result += f"{transport.send_data(message)}\n"
        result += f"{transport.disconnect()}"
        return result


class HTTPFactory(TransportFactory):
    """
    Concrete Creator: HTTPFactory.
    
    Creates and returns HTTP Transport instances.
    """

    def create_transport(self) -> Transport:
        """
        Creates an HTTP transport.
        
        Returns:
            An HTTPTransport instance.
        """
        return HTTPTransport()


class HTTPSFactory(TransportFactory):
    """
    Concrete Creator: HTTPSFactory.
    
    Creates and returns HTTPS Transport instances.
    """

    def create_transport(self) -> Transport:
        """
        Creates an HTTPS transport with SSL/TLS encryption.
        
        Returns:
            An HTTPSTransport instance.
        """
        return HTTPSTransport()


class FTPFactory(TransportFactory):
    """
    Concrete Creator: FTPFactory.
    
    Creates and returns FTP Transport instances.
    """

    def create_transport(self) -> Transport:
        """
        Creates an FTP transport for file transfers.
        
        Returns:
            An FTPTransport instance.
        """
        return FTPTransport()


class WebSocketFactory(TransportFactory):
    """
    Concrete Creator: WebSocketFactory.
    
    Creates and returns WebSocket Transport instances.
    """

    def create_transport(self) -> Transport:
        """
        Creates a WebSocket transport for real-time communication.
        
        Returns:
            A WebSocketTransport instance.
        """
        return WebSocketTransport()


class TransportFactoryRegistry:
    """
    Registry Pattern (Enhancement): Manages factory instances.
    
    This registry provides a centralized way to create transports without 
    needing to know the factory class names. It offers flexibility to 
    add or modify factory implementations at runtime.
    
    Attributes:
        _factories: Mapping of TransportType enum to factory instances.
    """

    def __init__(self) -> None:
        self._factories: Dict[TransportType, TransportFactory] = {
            TransportType.HTTP: HTTPFactory(),
            TransportType.HTTPS: HTTPSFactory(),
            TransportType.FTP: FTPFactory(),
            TransportType.WEBSOCKET: WebSocketFactory(),
        }

    def get_factory(self, transport_type: TransportType) -> TransportFactory:
        """
        Retrieve a factory for the specified transport type.
        
        Args:
            transport_type: The TransportType enum value.
            
        Returns:
            The corresponding TransportFactory instance.
            
        Raises:
            ValueError: If the transport type is not registered.
        """
        if transport_type not in self._factories:
            raise ValueError(f"Unknown transport type: {transport_type}")
        return self._factories[transport_type]

    def register_factory(
        self, transport_type: TransportType, factory: TransportFactory
    ) -> None:
        """
        Register a custom factory for a transport type.
        
        This allows runtime customization of transport creation logic.
        
        Args:
            transport_type: The TransportType enum value.
            factory: The TransportFactory instance to register.
        """
        self._factories[transport_type] = factory

    def create_transport(self, transport_type: TransportType) -> Transport:
        """
        Convenient method to create a transport by type.
        
        Args:
            transport_type: The desired TransportType.
            
        Returns:
            A Transport instance of the specified type.
        """
        factory = self.get_factory(transport_type)
        return factory.create_transport()
