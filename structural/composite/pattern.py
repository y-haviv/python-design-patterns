"""
Composite Pattern Implementation (Structural).

Compose objects into tree structures to represent part-whole hierarchies.
Composite lets clients treat individual objects and compositions of objects uniformly.
Used when you need to work with objects that form a tree structure, and want to treat
composite objects and leaf objects uniformly.

Key Components:
- Component: Abstract base for leaf and composite objects.
- Leaf: Represents leaf node with no children.
- Composite: Represents node that can contain children.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any


class Component(ABC):
    """
    Abstract Component interface for both leaf and composite objects.
    
    This is what clients work with. It defines operations that both 
    Leaf and Composite objects support.
    """

    @abstractmethod
    def operation(self) -> str:
        """Perform operation on component."""
        pass

    def add(self, component: Component) -> None:
        """Add child component (optional, for composite only)."""
        pass

    def remove(self, component: Component) -> None:
        """Remove child component (optional, for composite only)."""
        pass

    def get_child(self, index: int) -> Optional[Component]:
        """Get child at index (optional, for composite only)."""
        return None


class Leaf(Component):
    """
    Leaf Component - represents leaf node in tree.
    
    A leaf has no children. It implements operations from the Component interface.
    """

    def __init__(self, name: str) -> None:
        """Initialize leaf."""
        self.name = name

    def operation(self) -> str:
        """Perform operation on leaf."""
        return f"Leaf({self.name})"


class Composite(Component):
    """
    Composite Component - represents node that can contain children.
    
    Can have child components (both leaf and composite). Implements
    tree operations and delegates operations to children.
    """

    def __init__(self, name: str) -> None:
        """Initialize composite."""
        self.name = name
        self.children: List[Component] = []

    def add(self, component: Component) -> None:
        """Add child component."""
        self.children.append(component)

    def remove(self, component: Component) -> None:
        """Remove child component."""
        self.children.remove(component)

    def get_child(self, index: int) -> Optional[Component]:
        """Get child at index."""
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

    def operation(self) -> str:
        """Perform operation on composite and all children."""
        results = [f"Composite({self.name})"]
        for child in self.children:
            results.append(child.operation())
        return f"[{', '.join(results)}]"

    def get_children(self) -> List[Component]:
        """Get all children."""
        return self.children.copy()


class FileSystemComponent(ABC):
    """
    Abstract base for file system components (files and directories).
    """

    @abstractmethod
    def get_size(self) -> int:
        """Get size of component in bytes."""
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display component structure."""
        pass

    @abstractmethod
    def get_path(self) -> str:
        """Get path representation."""
        pass


class File(FileSystemComponent):
    """
    Leaf - represents a file in file system.
    """

    def __init__(self, name: str, size: int) -> None:
        """Initialize file."""
        self.name = name
        self.size = size

    def get_size(self) -> int:
        """Get file size."""
        return self.size

    def display(self, indent: int = 0) -> str:
        """Display file."""
        return " " * indent + f"📄 {self.name} ({self.size} bytes)"

    def get_path(self) -> str:
        """Get file path."""
        return self.name


class Directory(FileSystemComponent):
    """
    Composite - represents a directory in file system.
    """

    def __init__(self, name: str) -> None:
        """Initialize directory."""
        self.name = name
        self.components: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        """Add file or directory."""
        self.components.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        """Remove file or directory."""
        self.components.remove(component)

    def get_size(self) -> int:
        """Get total size of directory and contents."""
        total = 0
        for component in self.components:
            total += component.get_size()
        return total

    def display(self, indent: int = 0) -> str:
        """Display directory structure recursively."""
        lines = [" " * indent + f"📁 {self.name}/"]
        for component in self.components:
            lines.append(component.display(indent + 2))
        return "\n".join(lines)

    def get_path(self) -> str:
        """Get directory path."""
        return f"{self.name}/"

    def get_children(self) -> List[FileSystemComponent]:
        """Get all direct children."""
        return self.components.copy()


class OrganizationComponent(ABC):
    """
    Abstract component for organizational hierarchy.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Get component name."""
        pass

    @abstractmethod
    def get_head_count(self) -> int:
        """Get number of people in component."""
        pass

    @abstractmethod
    def get_budget(self) -> float:
        """Get total budget."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Get description."""
        pass


class Employee(OrganizationComponent):
    """
    Leaf - represents individual employee.
    """

    def __init__(self, name: str, title: str, salary: float) -> None:
        """Initialize employee."""
        self.name = name
        self.title = title
        self.salary = salary

    def get_name(self) -> str:
        """Get employee name."""
        return self.name

    def get_head_count(self) -> int:
        """Individual has headcount of 1."""
        return 1

    def get_budget(self) -> float:
        """Get employee salary."""
        return self.salary

    def describe(self) -> str:
        """Describe employee."""
        return f"{self.name} ({self.title}) - ${self.salary:,.2f}"


class Department(OrganizationComponent):
    """
    Composite - represents department that contains employees and sub-departments.
    """

    def __init__(self, name: str, manager: str) -> None:
        """Initialize department."""
        self.name = name
        self.manager = manager
        self.members: List[OrganizationComponent] = []

    def add_member(self, member: OrganizationComponent) -> None:
        """Add employee or sub-department."""
        self.members.append(member)

    def remove_member(self, member: OrganizationComponent) -> None:
        """Remove employee or sub-department."""
        self.members.remove(member)

    def get_name(self) -> str:
        """Get department name."""
        return self.name

    def get_head_count(self) -> int:
        """Get total headcount in department (recursive)."""
        total = 0
        for member in self.members:
            total += member.get_head_count()
        return total

    def get_budget(self) -> float:
        """Get total budget (recursive)."""
        total = 0.0
        for member in self.members:
            total += member.get_budget()
        return total

    def describe(self) -> str:
        """Describe department and its members recursively."""
        lines = [f"Department: {self.name} (Manager: {self.manager})"]
        for member in self.members:
            lines.append(f"  - {member.describe()}")
        return "\n".join(lines)

    def get_members(self) -> List[OrganizationComponent]:
        """Get direct members."""
        return self.members.copy()


class MenuComponent(ABC):
    """
    Abstract component for menu structure.
    """

    @abstractmethod
    def add(self, component: MenuComponent) -> None:
        """Add menu item or submenu."""
        pass

    @abstractmethod
    def remove(self, component: MenuComponent) -> None:
        """Remove menu item or submenu."""
        pass

    @abstractmethod
    def display(self, depth: int = 0) -> str:
        """Display menu."""
        pass

    @abstractmethod
    def execute(self) -> str:
        """Execute menu action."""
        pass


class MenuItem(MenuComponent):
    """
    Leaf - represents menu item with action.
    """

    def __init__(self, name: str, action: callable) -> None:
        """Initialize menu item."""
        self.name = name
        self.action = action

    def add(self, component: MenuComponent) -> None:
        """Not supported for leaf."""
        raise ValueError("Cannot add to MenuItem")

    def remove(self, component: MenuComponent) -> None:
        """Not supported for leaf."""
        raise ValueError("Cannot remove from MenuItem")

    def display(self, depth: int = 0) -> str:
        """Display menu item."""
        return "  " * depth + f"• {self.name}"

    def execute(self) -> str:
        """Execute menu item action."""
        return self.action()


class Menu(MenuComponent):
    """
    Composite - represents submenu that can contain items and other submenus.
    """

    def __init__(self, name: str) -> None:
        """Initialize menu."""
        self.name = name
        self.items: List[MenuComponent] = []

    def add(self, component: MenuComponent) -> None:
        """Add menu item or submenu."""
        self.items.append(component)

    def remove(self, component: MenuComponent) -> None:
        """Remove menu item or submenu."""
        self.items.remove(component)

    def display(self, depth: int = 0) -> str:
        """Display menu recursively."""
        lines = ["  " * depth + f"▸ {self.name}"]
        for item in self.items:
            lines.append(item.display(depth + 1))
        return "\n".join(lines)

    def execute(self) -> str:
        """Cannot execute composite menu."""
        results = [f"Executing menu: {self.name}"]
        for item in self.items:
            results.append(item.execute())
        return "\n".join(results)

    def get_items(self) -> List[MenuComponent]:
        """Get direct items."""
        return self.items.copy()


