"""
Visitor Pattern Implementation (Behavioral).

Represent an operation to be performed on the elements of an object structure.
Visitor lets you define a new operation without changing the classes of the
elements on which it operates.

Key Components:
- Visitor: Declares a visit method for each type of element.
- ConcreteVisitor: Implements specific operations for each element type.
- Element: Defines an accept method that takes a visitor.
- ConcreteElement: Implements accept to dispatch visitor calls.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
from datetime import datetime


class Visitor(ABC):
    """
    Abstract visitor that declares visit methods for each element type.
    
    Visitors define operations to be performed on elements of a structure
    without changing the element classes.
    """

    @abstractmethod
    def visit_element_a(self, element: ConcreteElementA) -> Any:
        """Visit a ConcreteElementA."""
        pass

    @abstractmethod
    def visit_element_b(self, element: ConcreteElementB) -> Any:
        """Visit a ConcreteElementB."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this visitor."""
        pass


class Element(ABC):
    """
    Abstract element that accepts visitors.
    
    Elements define an accept method that allows visitors to operate
    on them without the element knowing about the specific operations.
    """

    @abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        """Accept a visitor to perform an operation."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this element."""
        pass


class ConcreteElementA(Element):
    """Concrete element A that accepts visitors."""

    def __init__(self, name: str, value: str) -> None:
        """
        Initialize element A.
        
        Args:
            name: Element name.
            value: Element value.
        """
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        """Accept visitor and dispatch to the visitor's method."""
        return visitor.visit_element_a(self)

    def operation_a(self) -> str:
        """Element A specific operation."""
        return f"Operation A on {self.value}"

    def get_name(self) -> str:
        """Get element name."""
        return self.name


class ConcreteElementB(Element):
    """Concrete element B that accepts visitors."""

    def __init__(self, name: str, count: int) -> None:
        """
        Initialize element B.
        
        Args:
            name: Element name.
            count: Element count.
        """
        self.name = name
        self.count = count

    def accept(self, visitor: Visitor) -> Any:
        """Accept visitor and dispatch to the visitor's method."""
        return visitor.visit_element_b(self)

    def operation_b(self) -> str:
        """Element B specific operation."""
        return f"Operation B: {self.count} items"

    def get_name(self) -> str:
        """Get element name."""
        return self.name


class ConcreteVisitorA(Visitor):
    """Concrete visitor A that performs operations on elements."""

    def __init__(self) -> None:
        """Initialize visitor A."""
        self.results: List[str] = []
        self.visit_log: List[Dict[str, Any]] = []

    def visit_element_a(self, element: ConcreteElementA) -> Any:
        """Visit element A."""
        result = f"[VisitorA] Processing ElementA: {element.operation_a()}"
        print(f"  {result}")
        self.results.append(result)
        self.visit_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "ConcreteElementA",
            "element_name": element.get_name(),
            "operation": element.operation_a(),
        })
        return result

    def visit_element_b(self, element: ConcreteElementB) -> Any:
        """Visit element B."""
        result = f"[VisitorA] Processing ElementB: {element.operation_b()}"
        print(f"  {result}")
        self.results.append(result)
        self.visit_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "ConcreteElementB",
            "element_name": element.get_name(),
            "operation": element.operation_b(),
        })
        return result

    def get_name(self) -> str:
        """Get visitor name."""
        return "Visitor A"

    def get_results(self) -> List[str]:
        """Get all visit results."""
        return self.results.copy()

    def get_visit_count(self) -> int:
        """Get number of elements visited."""
        return len(self.visit_log)


class ConcreteVisitorB(Visitor):
    """Concrete visitor B that performs different operations on elements."""

    def __init__(self) -> None:
        """Initialize visitor B."""
        self.results: List[str] = []
        self.statistics: Dict[str, Any] = {"element_a_count": 0, "element_b_count": 0}
        self.visit_log: List[Dict[str, Any]] = []

    def visit_element_a(self, element: ConcreteElementA) -> Any:
        """Visit element A (different operation than VisitorA)."""
        self.statistics["element_a_count"] += 1
        result = f"[VisitorB] ElementA length: {len(element.value)} chars"
        print(f"  {result}")
        self.results.append(result)
        self.visit_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "ConcreteElementA",
            "element_name": element.get_name(),
            "analysis": f"Length: {len(element.value)}",
        })
        return result

    def visit_element_b(self, element: ConcreteElementB) -> Any:
        """Visit element B (different operation than VisitorA)."""
        self.statistics["element_b_count"] += 1
        result = f"[VisitorB] ElementB sum: {element.count * 2}"
        print(f"  {result}")
        self.results.append(result)
        self.visit_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "ConcreteElementB",
            "element_name": element.get_name(),
            "analysis": f"Sum: {element.count * 2}",
        })
        return result

    def get_name(self) -> str:
        """Get visitor name."""
        return "Visitor B"

    def get_results(self) -> List[str]:
        """Get all visit results."""
        return self.results.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Get collected statistics."""
        return self.statistics.copy()

    def get_visit_count(self) -> int:
        """Get number of elements visited."""
        return len(self.visit_log)
