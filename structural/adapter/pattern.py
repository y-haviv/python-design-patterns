"""
Adapter Pattern Implementation (Structural).

Convert the interface of a class into another interface clients expect.
Adapter lets classes work together that couldn't otherwise because of 
incompatible interfaces. Useful when integrating legacy systems or 
third-party libraries with incompatible interfaces.

Key Components:
- Target: Interface expected by clients.
- Adapter: Adapts the incompatible interface of an Adaptee to the Target.
- Adaptee: The class with the incompatible interface.
- Client: Uses objects conforming to the Target interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Target(ABC):
    """
    Target interface expected by clients.
    
    This is the interface that clients want to use. Any class that 
    implements this interface can be used by the client.
    """

    @abstractmethod
    def request(self) -> str:
        """Process a request in the expected format."""
        pass


class Adaptee:
    """
    Adaptee class with an incompatible interface.
    
    This class provides functionality but uses a different interface 
    than what clients expect. It needs to be adapted to work with 
    the Target interface.
    
    Example:
        A legacy library with a specific API that doesn't match 
        the client's expectations.
    """

    def specific_request(self) -> str:
        """Return data using a different interface."""
        return "Specific request from Adaptee"

    def get_data_in_format(self, format_type: str) -> Dict[str, Any]:
        """Return data in a specific format."""
        if format_type == "json":
            return {"type": "adaptee", "message": "Data from legacy system"}
        elif format_type == "xml":
            return {"xml": "<adaptee><message>Data</message></adaptee>"}
        return {"raw": self.specific_request()}


class Adapter(Target):
    """
    Adapter that converts Adaptee's interface to Target's interface.
    
    This is the class adapter implementation using inheritance.
    It adapts the incompatible Adaptee so it can work with code 
    expecting the Target interface.
    """

    def __init__(self, adaptee: Adaptee) -> None:
        """
        Initialize the adapter with an Adaptee instance.
        
        Args:
            adaptee: The object with incompatible interface to adapt.
        """
        self.adaptee = adaptee

    def request(self) -> str:
        """
        Adapt the Adaptee's specific request to the Target interface.
        
        This method translates calls from the Target interface to 
        the Adaptee's interface.
        """
        # Translate Target interface to Adaptee interface
        adaptee_data = self.adaptee.get_data_in_format("json")
        message = adaptee_data.get("message", "")
        return f"Adapted response: {message}"


class TwoWayAdapter(Target):
    """
    Two-way adapter that can work with both Adaptee and Target.
    
    This adapter allows bidirectional adaptation, enabling code to 
    work with either interface seamlessly.
    """

    def __init__(self, adaptee: Adaptee | None = None) -> None:
        """Initialize with optional Adaptee."""
        self.adaptee = adaptee

    def request(self) -> str:
        """Process request in Target format."""
        if self.adaptee:
            return self.adaptee.specific_request()
        return "Default response"

    def set_adaptee(self, adaptee: Adaptee) -> None:
        """Set or change the Adaptee."""
        self.adaptee = adaptee

    def get_adaptee_specific_request(self) -> str:
        """Get response in Adaptee's format."""
        if self.adaptee:
            return self.adaptee.specific_request()
        return "No adaptee set"


class LegacySystem:
    """
    Another legacy system with yet another incompatible interface.
    
    Demonstrates adapting multiple different legacy systems.
    """

    def get_information(self) -> str:
        """Legacy API with different naming convention."""
        return "Information from legacy system"

    def execute_operation(self, operation_code: str) -> str:
        """Execute legacy operations."""
        if operation_code == "OP001":
            return "Operation 001 executed"
        return "Unknown operation"


class LegacySystemAdapter(Target):
    """Adapter to integrate LegacySystem with modern Target interface."""

    def __init__(self, legacy_system: LegacySystem) -> None:
        """Initialize with LegacySystem instance."""
        self.legacy_system = legacy_system

    def request(self) -> str:
        """Adapt legacy system to Target interface."""
        legacy_info = self.legacy_system.get_information()
        operation_result = self.legacy_system.execute_operation("OP001")
        return f"{legacy_info} - {operation_result}"


class ClassAdapter(Target):
    """
    Class adapter using multiple inheritance.
    
    Inherits from both Target (the interface we want) and Adaptee 
    (the implementation we need to adapt).
    
    Note: This approach is less preferred in Python. The object 
    adapter (composition-based) is generally better.
    """

    def request(self) -> str:
        """Provide Target interface using adapted behavior."""
        # This would inherit from both Target and Adaptee
        return "Class-based adaptation"


class AdapterWithValidation(Target):
    """
    Enhanced adapter that adds validation and transformation logic.
    
    Demonstrates how adapters can do more than just interface translation—
    they can also validate, transform, and enrich data.
    """

    def __init__(self, adaptee: Adaptee) -> None:
        """Initialize with Adaptee."""
        self.adaptee = adaptee
        self.validation_errors: List[str] = []

    def request(self) -> str:
        """Adapt with validation and transformation."""
        self.validation_errors.clear()

        # Get data from adaptee
        adaptee_data = self.adaptee.get_data_in_format("json")

        # Validate
        if not self._validate(adaptee_data):
            error_msg = "; ".join(self.validation_errors)
            return f"Validation failed: {error_msg}"

        # Transform
        transformed = self._transform(adaptee_data)
        return f"Validated and transformed: {transformed}"

    def _validate(self, data: Dict[str, Any]) -> bool:
        """Validate the adapted data."""
        if not isinstance(data, dict):
            self.validation_errors.append("Data must be a dictionary")
            return False
        if "message" not in data:
            self.validation_errors.append("Missing 'message' field")
            return False
        return True

    def _transform(self, data: Dict[str, Any]) -> str:
        """Transform the adapted data."""
        message = data.get("message", "")
        return message.upper()


class AdapterRegistry:
    """
    Registry pattern for managing multiple adapters.
    
    Dynamically creates and manages adapters based on adaptee types.
    Useful when you need to adapt many different legacy systems.
    """

    def __init__(self) -> None:
        """Initialize the adapter registry."""
        self._adapters: Dict[str, Any] = {}

    def register_adapter(self, adaptee_type: str, adapter_class: type) -> None:
        """Register an adapter for a specific adaptee type."""
        self._adapters[adaptee_type] = adapter_class

    def create_adapter(self, adaptee_type: str, adaptee: Any) -> Target:
        """Create an adapter instance for the given adaptee."""
        if adaptee_type not in self._adapters:
            raise ValueError(f"No adapter registered for type: {adaptee_type}")

        adapter_class = self._adapters[adaptee_type]
        return adapter_class(adaptee)

    def get_registered_adapters(self) -> List[str]:
        """Get list of registered adapter types."""
        return list(self._adapters.keys())


