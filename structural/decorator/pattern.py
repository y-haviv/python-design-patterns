"""
Decorator Pattern Implementation (Structural).

Attach additional responsibilities to an object dynamically, keeping the same interface.
Provides a flexible alternative to subclassing for extending functionality.
Allows behavior to be added to objects without modifying their classes.

Key Components:
- Component: Interface for the object being decorated.
- ConcreteComponent: Original object we're wrapping.
- Decorator: Abstract class conforming to Component interface.
- ConcreteDecorator: Adds specific behavior/responsibility.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime


class Component(ABC):
    """Abstract Component interface."""

    @abstractmethod
    def operation(self) -> str:
        """Perform operation."""
        pass


class ConcreteComponent(Component):
    """Concrete Component - original object."""

    def operation(self) -> str:
        """Return basic operation result."""
        return "ConcreteComponent"


class Decorator(Component):
    """
    Decorator abstract class.
    
    Maintains reference to Component and delegates to it,
    while potentially adding additional behavior.
    """

    def __init__(self, component: Component) -> None:
        """Initialize with component to decorate."""
        self._component = component

    def operation(self) -> str:
        """Delegate to wrapped component."""
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """Concrete Decorator A - adds specific behavior."""

    def operation(self) -> str:
        """Extend component operation with behavior A."""
        return f"ConcreteDecoratorA({self._component.operation()})"


class ConcreteDecoratorB(Decorator):
    """Concrete Decorator B - adds different behavior."""

    def operation(self) -> str:
        """Extend component operation with behavior B."""
        return f"ConcreteDecoratorB({self._component.operation()})"


class DataSource(ABC):
    """Abstract DataSource interface."""

    @abstractmethod
    def write_data(self, data: str) -> None:
        """Write data."""
        pass

    @abstractmethod
    def read_data(self) -> str:
        """Read data."""
        pass


class FileDataSource(DataSource):
    """Concrete DataSource - file storage."""

    def __init__(self, filename: str) -> None:
        """Initialize with filename."""
        self.filename = filename
        self.data: str = ""

    def write_data(self, data: str) -> None:
        """Write data to file (simulated)."""
        self.data = data

    def read_data(self) -> str:
        """Read data from file (simulated)."""
        return self.data


class DataSourceDecorator(DataSource):
    """
    Abstract decorator for DataSource.
    
    Wraps another DataSource and potentially adds behavior.
    """

    def __init__(self, datasource: DataSource) -> None:
        """Initialize with datasource to decorate."""
        self.datasource = datasource

    def write_data(self, data: str) -> None:
        """Delegate write to wrapped datasource."""
        self.datasource.write_data(data)

    def read_data(self) -> str:
        """Delegate read to wrapped datasource."""
        return self.datasource.read_data()


class EncryptionDecorator(DataSourceDecorator):
    """Decorator that adds encryption."""

    def write_data(self, data: str) -> None:
        """Encrypt before writing."""
        encrypted = self._encrypt(data)
        super().write_data(encrypted)

    def read_data(self) -> str:
        """Read and decrypt."""
        encrypted = super().read_data()
        return self._decrypt(encrypted)

    def _encrypt(self, data: str) -> str:
        """Simple encryption simulation."""
        return "".join(chr(ord(c) + 1) for c in data)

    def _decrypt(self, data: str) -> str:
        """Simple decryption simulation."""
        return "".join(chr(ord(c) - 1) for c in data)


class CompressionDecorator(DataSourceDecorator):
    """Decorator that adds compression."""

    def write_data(self, data: str) -> None:
        """Compress before writing."""
        compressed = self._compress(data)
        super().write_data(compressed)

    def read_data(self) -> str:
        """Read and decompress."""
        compressed = super().read_data()
        return self._decompress(compressed)

    def _compress(self, data: str) -> str:
        """Simple compression simulation."""
        return data.replace(" ", "")

    def _decompress(self, data: str) -> str:
        """Simple decompression simulation."""
        return data


class LoggingDecorator(DataSourceDecorator):
    """Decorator that adds logging."""

    def __init__(self, datasource: DataSource) -> None:
        """Initialize with datasource."""
        super().__init__(datasource)
        self.log: List[str] = []

    def write_data(self, data: str) -> None:
        """Log write operation."""
        timestamp = datetime.now().isoformat()
        self.log.append(f"WRITE at {timestamp}: {len(data)} bytes")
        super().write_data(data)

    def read_data(self) -> str:
        """Log read operation."""
        timestamp = datetime.now().isoformat()
        result = super().read_data()
        self.log.append(f"READ at {timestamp}: {len(result)} bytes")
        return result

    def get_log(self) -> List[str]:
        """Get operation log."""
        return self.log.copy()


class Coffee(ABC):
    """Abstract Coffee component."""

    @abstractmethod
    def get_cost(self) -> float:
        """Get coffee cost."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get description."""
        pass


class SimpleCoffee(Coffee):
    """Concrete Coffee - simple coffee."""

    def get_cost(self) -> float:
        """Return base cost."""
        return 2.0

    def get_description(self) -> str:
        """Get description."""
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    """Abstract Coffee Decorator."""

    def __init__(self, coffee: Coffee) -> None:
        """Initialize with coffee."""
        self.coffee = coffee

    def get_cost(self) -> float:
        """Delegate to wrapped coffee."""
        return self.coffee.get_cost()

    def get_description(self) -> str:
        """Delegate to wrapped coffee."""
        return self.coffee.get_description()


class MilkDecorator(CoffeeDecorator):
    """Decorator adding milk."""

    def get_cost(self) -> float:
        """Add milk cost."""
        return self.coffee.get_cost() + 0.5

    def get_description(self) -> str:
        """Add milk to description."""
        return f"{self.coffee.get_description()}, Milk"


class SugarDecorator(CoffeeDecorator):
    """Decorator adding sugar."""

    def get_cost(self) -> float:
        """Add sugar cost."""
        return self.coffee.get_cost() + 0.25

    def get_description(self) -> str:
        """Add sugar to description."""
        return f"{self.coffee.get_description()}, Sugar"


class WhippedCreamDecorator(CoffeeDecorator):
    """Decorator adding whipped cream."""

    def get_cost(self) -> float:
        """Add whipped cream cost."""
        return self.coffee.get_cost() + 0.7

    def get_description(self) -> str:
        """Add whipped cream to description."""
        return f"{self.coffee.get_description()}, Whipped Cream"


class VanillaDecorator(CoffeeDecorator):
    """Decorator adding vanilla."""

    def get_cost(self) -> float:
        """Add vanilla cost."""
        return self.coffee.get_cost() + 0.3

    def get_description(self) -> str:
        """Add vanilla to description."""
        return f"{self.coffee.get_description()}, Vanilla"


class CoffeeBuilder:
    """Builder for creating decorated coffee."""

    def __init__(self) -> None:
        """Initialize with simple coffee."""
        self.coffee: Coffee = SimpleCoffee()

    def add_milk(self) -> CoffeeBuilder:
        """Add milk decorator."""
        self.coffee = MilkDecorator(self.coffee)
        return self

    def add_sugar(self) -> CoffeeBuilder:
        """Add sugar decorator."""
        self.coffee = SugarDecorator(self.coffee)
        return self

    def add_whipped_cream(self) -> CoffeeBuilder:
        """Add whipped cream decorator."""
        self.coffee = WhippedCreamDecorator(self.coffee)
        return self

    def add_vanilla(self) -> CoffeeBuilder:
        """Add vanilla decorator."""
        self.coffee = VanillaDecorator(self.coffee)
        return self

    def build(self) -> Coffee:
        """Get built coffee."""
        return self.coffee

    def get_description(self) -> str:
        """Get coffee description."""
        return self.coffee.get_description()

    def get_cost(self) -> float:
        """Get total cost."""
        return self.coffee.get_cost()


class Widget(ABC):
    """Abstract widget component."""

    @abstractmethod
    def render(self) -> str:
        """Render widget."""
        pass


class SimpleWidget(Widget):
    """Simple widget."""

    def __init__(self, text: str) -> None:
        """Initialize with text."""
        self.text = text

    def render(self) -> str:
        """Render text."""
        return self.text


class WidgetDecorator(Widget):
    """Abstract widget decorator."""

    def __init__(self, widget: Widget) -> None:
        """Initialize with widget."""
        self.widget = widget

    def render(self) -> str:
        """Delegate rendering."""
        return self.widget.render()


class BorderDecorator(WidgetDecorator):
    """Decorator adding border."""

    def render(self) -> str:
        """Add border to render."""
        content = self.widget.render()
        return f"+----+\n| {content} |\n+----+"


class ScrollDecorator(WidgetDecorator):
    """Decorator adding scrollbars."""

    def render(self) -> str:
        """Add scrollbars."""
        content = self.widget.render()
        return f"[{content}]"


class ShadowDecorator(WidgetDecorator):
    """Decorator adding shadow."""

    def render(self) -> str:
        """Add shadow effect."""
        content = self.widget.render()
        lines = content.split("\n")
        result = []
        for line in lines:
            result.append(f"  {line}")
        result.append("  ~~~")
        return "\n".join(result)


