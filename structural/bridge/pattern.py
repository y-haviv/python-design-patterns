"""
Bridge Pattern Implementation (Structural).

Decouple an abstraction from its implementation so the two can vary independently.
The Bridge pattern is useful when you want to avoid permanent binding between 
abstraction and implementation, and when changes in the implementation should not 
affect clients, and sharing of implementation is desired by multiple objects.

Key Components:
- Abstraction: Defines the high-level interface used by clients.
- RefinedAbstraction: Extends the Abstraction interface.
- Implementor: Defines the low-level interface for platform-specific operations.
- ConcreteImplementor: Implements the Implementor interface for a specific platform.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class Implementor(ABC):
    """
    Implementor interface - defines platform-specific operations.
    
    This is the low-level interface that different implementations 
    must provide. It represents the implementation side of the bridge.
    """

    @abstractmethod
    def operation_impl(self) -> str:
        """Perform implementation-specific operation."""
        pass


class ConcreteImplementorA(Implementor):
    """
    Concrete Implementor A - specific platform/implementation.
    
    This represents one way something could be implemented 
    (e.g., Windows platform, PostgreSQL database, etc.).
    """

    def operation_impl(self) -> str:
        """Provide implementation for platform A."""
        return "ConcreteImplementorA: Here's the result on platform A."


class ConcreteImplementorB(Implementor):
    """
    Concrete Implementor B - different platform/implementation.
    
    This represents another way something could be implemented 
    (e.g., Linux platform, MySQL database, etc.).
    """

    def operation_impl(self) -> str:
        """Provide implementation for platform B."""
        return "ConcreteImplementorB: Here's the result on platform B."


class Abstraction:
    """
    Abstraction - defines the high-level interface for clients.
    
    This is the interface that clients interact with. It maintains 
    a reference to an Implementor but doesn't depend on concrete 
    implementations. Changes to the implementation don't affect 
    this abstraction.
    """

    def __init__(self, implementor: Implementor) -> None:
        """
        Initialize with an implementation.
        
        Args:
            implementor: The implementation to use.
        """
        self._implementor = implementor

    def operation(self) -> str:
        """Perform abstraction's operation using implementor."""
        return f"Abstraction: {self._implementor.operation_impl()}"

    def set_implementor(self, implementor: Implementor) -> None:
        """Change implementation at runtime."""
        self._implementor = implementor


class RefinedAbstraction(Abstraction):
    """
    Refined Abstraction - extends the abstraction with more specifics.
    
    Provides additional functionality on top of the basic abstraction 
    while still using the bridged implementor for platform-specific work.
    """

    def operation(self) -> str:
        """Perform refined operation."""
        base_result = self._implementor.operation_impl()
        return f"RefinedAbstraction: Extended functionality with ({base_result})"

    def extended_operation(self) -> str:
        """Additional refined operation."""
        return f"RefinedAbstraction: Extended implementation detail: {self._implementor.operation_impl()}"


class DrawingAPI(ABC):
    """
    Implementor interface for drawing operations.
    
    Represents different drawing implementations (Canvas, SVG, etc.).
    """

    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> str:
        """Draw a circle."""
        pass

    @abstractmethod
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> str:
        """Draw a rectangle."""
        pass

    @abstractmethod
    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> str:
        """Draw a line."""
        pass


class CanvasAPI(DrawingAPI):
    """
    Concrete Implementor - Canvas drawing implementation.
    
    Uses Canvas API for rendering (e.g., HTML5 Canvas).
    """

    def draw_circle(self, x: float, y: float, radius: float) -> str:
        """Draw circle on canvas."""
        return f"Canvas: Drawing circle at ({x}, {y}) with radius {radius}"

    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> str:
        """Draw rectangle on canvas."""
        return f"Canvas: Drawing rectangle at ({x}, {y}) {width}x{height}"

    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> str:
        """Draw line on canvas."""
        return f"Canvas: Drawing line from ({x1}, {y1}) to ({x2}, {y2})"


class SVGAPI(DrawingAPI):
    """
    Concrete Implementor - SVG drawing implementation.
    
    Uses SVG for rendering (vector graphics).
    """

    def draw_circle(self, x: float, y: float, radius: float) -> str:
        """Draw circle in SVG."""
        return f'SVG: <circle cx="{x}" cy="{y}" r="{radius}" />'

    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> str:
        """Draw rectangle in SVG."""
        return f'SVG: <rect x="{x}" y="{y}" width="{width}" height="{height}" />'

    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> str:
        """Draw line in SVG."""
        return f'SVG: <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'


class Shape:
    """
    Abstraction - represents a geometric shape.
    
    This is what clients interact with. The bridge pattern allows 
    different shape types to work with different drawing implementations.
    """

    def __init__(self, drawing_api: DrawingAPI) -> None:
        """Initialize with drawing implementation."""
        self._drawing_api = drawing_api

    def draw(self) -> str:
        """Draw the shape."""
        raise NotImplementedError

    def set_drawing_api(self, api: DrawingAPI) -> None:
        """Change drawing implementation."""
        self._drawing_api = api


class Circle(Shape):
    """
    Refined Abstraction - a circle shape.
    
    Knows how to draw itself using the bridged drawing API.
    """

    def __init__(self, x: float, y: float, radius: float, drawing_api: DrawingAPI) -> None:
        """Initialize circle with position and size."""
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> str:
        """Draw the circle using the drawing API."""
        return self._drawing_api.draw_circle(self.x, self.y, self.radius)

    def resize(self, new_radius: float) -> None:
        """Resize the circle."""
        self.radius = new_radius


class Rectangle(Shape):
    """
    Refined Abstraction - a rectangle shape.
    
    Knows how to draw itself using the bridged drawing API.
    """

    def __init__(
        self, x: float, y: float, width: float, height: float, drawing_api: DrawingAPI
    ) -> None:
        """Initialize rectangle with position and dimensions."""
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self) -> str:
        """Draw the rectangle using the drawing API."""
        return self._drawing_api.draw_rectangle(self.x, self.y, self.width, self.height)

    def scale(self, factor: float) -> None:
        """Scale the rectangle."""
        self.width *= factor
        self.height *= factor


class Line(Shape):
    """
    Refined Abstraction - a line shape.
    
    Knows how to draw itself using the bridged drawing API.
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float, drawing_api: DrawingAPI) -> None:
        """Initialize line with endpoints."""
        super().__init__(drawing_api)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self) -> str:
        """Draw the line using the drawing API."""
        return self._drawing_api.draw_line(self.x1, self.y1, self.x2, self.y2)

    def extend(self, dx: float, dy: float) -> None:
        """Extend the line."""
        self.x2 += dx
        self.y2 += dy


class ShapeComposer:
    """
    Composes multiple shapes for drawing.
    
    Demonstrates how bridge pattern allows flexible composition.
    """

    def __init__(self, api: DrawingAPI) -> None:
        """Initialize with drawing API."""
        self.shapes: List[Shape] = []
        self.api = api

    def add_shape(self, shape: Shape) -> None:
        """Add shape to composer."""
        shape.set_drawing_api(self.api)
        self.shapes.append(shape)

    def draw_all(self) -> List[str]:
        """Draw all shapes."""
        return [shape.draw() for shape in self.shapes]

    def switch_api(self, new_api: DrawingAPI) -> None:
        """Switch drawing implementation for all shapes."""
        self.api = new_api
        for shape in self.shapes:
            shape.set_drawing_api(new_api)

    def draw_all_with_new_api(self) -> List[str]:
        """Redraw all shapes with current API."""
        return self.draw_all()


