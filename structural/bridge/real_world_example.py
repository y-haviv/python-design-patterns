"""
Real-World Example: Multi-Platform Remote Control System.

This example demonstrates the Bridge pattern in a practical scenario:
creating remote controls that can work with different types of devices
(TV, stereo, projector) on different platforms (WiFi, Bluetooth, IR).

The Bridge pattern allows us to vary the device type and communication 
platform independently.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime


class CommunicationBridge(ABC):
    """
    Implementor interface - represents communication method.
    
    Different concrete implementations handle different communication
    protocols (WiFi, Bluetooth, Infrared) for controlling remote devices.
    """

    @abstractmethod
    def send_command(self, device_id: str, command: str, *args: Any) -> bool:
        """Send a command to a device."""
        pass

    @abstractmethod
    def receive_status(self, device_id: str) -> Dict[str, Any]:
        """Receive status from a device."""
        pass

    @abstractmethod
    def connect(self, device_id: str) -> bool:
        """Connect to device."""
        pass

    @abstractmethod
    def disconnect(self, device_id: str) -> bool:
        """Disconnect from device."""
        pass

    @abstractmethod
    def get_connection_type(self) -> str:
        """Get connection type name."""
        pass


class WiFiBridge(CommunicationBridge):
    """
    Concrete Implementor - WiFi-based communication.
    
    Communicates with devices over WiFi/network protocol.
    """

    def __init__(self) -> None:
        """Initialize WiFi bridge."""
        self.connected_devices: Dict[str, bool] = {}
        self.log: List[str] = []

    def send_command(self, device_id: str, command: str, *args: Any) -> bool:
        """Send command via WiFi."""
        if device_id not in self.connected_devices:
            return False

        msg = f"WiFi: Sending '{command}' to {device_id} with args {args}"
        self.log.append(msg)
        return True

    def receive_status(self, device_id: str) -> Dict[str, Any]:
        """Receive status via WiFi."""
        return {
            "device": device_id,
            "status": "online",
            "signal": 95,
            "protocol": "WiFi",
            "timestamp": datetime.now().isoformat(),
        }

    def connect(self, device_id: str) -> bool:
        """Connect via WiFi."""
        self.connected_devices[device_id] = True
        self.log.append(f"WiFi: Connected to {device_id}")
        return True

    def disconnect(self, device_id: str) -> bool:
        """Disconnect from WiFi."""
        if device_id in self.connected_devices:
            del self.connected_devices[device_id]
            self.log.append(f"WiFi: Disconnected from {device_id}")
            return True
        return False

    def get_connection_type(self) -> str:
        """Get connection type."""
        return "WiFi"


class BluetoothBridge(CommunicationBridge):
    """
    Concrete Implementor - Bluetooth-based communication.
    
    Communicates with devices over Bluetooth protocol.
    """

    def __init__(self) -> None:
        """Initialize Bluetooth bridge."""
        self.paired_devices: Dict[str, bool] = {}
        self.log: List[str] = []

    def send_command(self, device_id: str, command: str, *args: Any) -> bool:
        """Send command via Bluetooth."""
        if device_id not in self.paired_devices:
            return False

        msg = f"Bluetooth: Sending '{command}' to {device_id}"
        self.log.append(msg)
        return True

    def receive_status(self, device_id: str) -> Dict[str, Any]:
        """Receive status via Bluetooth."""
        return {
            "device": device_id,
            "status": "paired",
            "signal": 70,
            "protocol": "Bluetooth",
            "timestamp": datetime.now().isoformat(),
        }

    def connect(self, device_id: str) -> bool:
        """Pair via Bluetooth."""
        self.paired_devices[device_id] = True
        self.log.append(f"Bluetooth: Paired with {device_id}")
        return True

    def disconnect(self, device_id: str) -> bool:
        """Unpair from Bluetooth."""
        if device_id in self.paired_devices:
            del self.paired_devices[device_id]
            self.log.append(f"Bluetooth: Unpaired from {device_id}")
            return True
        return False

    def get_connection_type(self) -> str:
        """Get connection type."""
        return "Bluetooth"


class InfraredBridge(CommunicationBridge):
    """
    Concrete Implementor - Infrared-based communication.
    
    Communicates with devices using infrared signals (traditional remote).
    """

    def __init__(self) -> None:
        """Initialize Infrared bridge."""
        self.in_range_devices: Dict[str, bool] = {}
        self.log: List[str] = []

    def send_command(self, device_id: str, command: str, *args: Any) -> bool:
        """Send command via Infrared."""
        if device_id not in self.in_range_devices:
            return False

        msg = f"IR: Sending signal '{command}' to {device_id}"
        self.log.append(msg)
        return True

    def receive_status(self, device_id: str) -> Dict[str, Any]:
        """Receive status via Infrared."""
        return {
            "device": device_id,
            "status": "in_range",
            "signal": "pulsed",
            "protocol": "Infrared",
            "timestamp": datetime.now().isoformat(),
        }

    def connect(self, device_id: str) -> bool:
        """Put device in range (IR)."""
        self.in_range_devices[device_id] = True
        self.log.append(f"IR: {device_id} is now in range")
        return True

    def disconnect(self, device_id: str) -> bool:
        """Put device out of range (IR)."""
        if device_id in self.in_range_devices:
            del self.in_range_devices[device_id]
            self.log.append(f"IR: {device_id} is now out of range")
            return True
        return False

    def get_connection_type(self) -> str:
        """Get connection type."""
        return "Infrared"


class RemoteControl:
    """
    Abstraction - represents a remote control.
    
    This is what the user interacts with. Different remote types and
    communication methods can be used without changing this interface.
    """

    def __init__(self, device_id: str, communication: CommunicationBridge) -> None:
        """
        Initialize remote control.
        
        Args:
            device_id: ID of the device to control
            communication: The communication bridge to use
        """
        self.device_id = device_id
        self.communication = communication
        self.connected = False

    def connect(self) -> bool:
        """Connect to the device."""
        self.connected = self.communication.connect(self.device_id)
        return self.connected

    def disconnect(self) -> bool:
        """Disconnect from the device."""
        self.connected = False
        return self.communication.disconnect(self.device_id)

    def get_status(self) -> Dict[str, Any]:
        """Get device status."""
        return self.communication.receive_status(self.device_id)

    def change_communication(self, communication: CommunicationBridge) -> None:
        """Switch to a different communication method at runtime."""
        if self.connected:
            self.disconnect()
        self.communication = communication


class TVRemote(RemoteControl):
    """
    Refined Abstraction - TV-specific remote control.
    
    Provides TV-specific operations like volume, channel, power.
    """

    def power_on(self) -> bool:
        """Turn on TV."""
        return self.communication.send_command(self.device_id, "power_on")

    def power_off(self) -> bool:
        """Turn off TV."""
        return self.communication.send_command(self.device_id, "power_off")

    def change_channel(self, channel: int) -> bool:
        """Change TV channel."""
        return self.communication.send_command(self.device_id, "change_channel", channel)

    def set_volume(self, level: int) -> bool:
        """Set TV volume."""
        return self.communication.send_command(self.device_id, "set_volume", level)

    def increase_volume(self) -> bool:
        """Increase volume."""
        return self.communication.send_command(self.device_id, "volume_up")

    def decrease_volume(self) -> bool:
        """Decrease volume."""
        return self.communication.send_command(self.device_id, "volume_down")


class StereoRemote(RemoteControl):
    """
    Refined Abstraction - Stereo-specific remote control.
    
    Provides stereo-specific operations like play, stop, album, artist.
    """

    def play(self) -> bool:
        """Play music."""
        return self.communication.send_command(self.device_id, "play")

    def stop(self) -> bool:
        """Stop music."""
        return self.communication.send_command(self.device_id, "stop")

    def pause(self) -> bool:
        """Pause music."""
        return self.communication.send_command(self.device_id, "pause")

    def next_track(self) -> bool:
        """Skip to next track."""
        return self.communication.send_command(self.device_id, "next_track")

    def previous_track(self) -> bool:
        """Go to previous track."""
        return self.communication.send_command(self.device_id, "previous_track")

    def set_volume(self, level: int) -> bool:
        """Set stereo volume."""
        return self.communication.send_command(self.device_id, "set_volume", level)


class ProjectorRemote(RemoteControl):
    """
    Refined Abstraction - Projector-specific remote control.
    
    Provides projector-specific operations like focus, zoom, brightness.
    """

    def power_on(self) -> bool:
        """Turn on projector."""
        return self.communication.send_command(self.device_id, "power_on")

    def power_off(self) -> bool:
        """Turn off projector."""
        return self.communication.send_command(self.device_id, "power_off")

    def focus(self, direction: str) -> bool:
        """Adjust focus."""
        return self.communication.send_command(self.device_id, "focus", direction)

    def zoom(self, amount: float) -> bool:
        """Zoom in or out."""
        return self.communication.send_command(self.device_id, "zoom", amount)

    def brightness(self, level: int) -> bool:
        """Set brightness."""
        return self.communication.send_command(self.device_id, "brightness", level)


class RemoteControlFactory:
    """
    Factory for creating remote controls with specific configurations.
    
    Allows easy instantiation of different remote types with different
    communication bridges.
    """

    def __init__(self) -> None:
        """Initialize factory."""
        self.remotes: Dict[str, RemoteControl] = {}

    def create_tv_remote(
        self, device_id: str, communication: CommunicationBridge
    ) -> TVRemote:
        """Create TV remote."""
        remote = TVRemote(device_id, communication)
        self.remotes[device_id] = remote
        return remote

    def create_stereo_remote(
        self, device_id: str, communication: CommunicationBridge
    ) -> StereoRemote:
        """Create stereo remote."""
        remote = StereoRemote(device_id, communication)
        self.remotes[device_id] = remote
        return remote

    def create_projector_remote(
        self, device_id: str, communication: CommunicationBridge
    ) -> ProjectorRemote:
        """Create projector remote."""
        remote = ProjectorRemote(device_id, communication)
        self.remotes[device_id] = remote
        return remote

    def get_remote(self, device_id: str) -> RemoteControl:
        """Get existing remote."""
        return self.remotes[device_id]

    def get_all_remotes(self) -> Dict[str, RemoteControl]:
        """Get all created remotes."""
        return self.remotes.copy()


