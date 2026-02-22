"""
Prototype Pattern - Structural Implementation.

This module demonstrates the Prototype pattern, which provides a way to create 
new objects by copying an existing object (the prototype) rather than creating 
them from scratch.

Key Concepts:
- Prototype: An object that will be cloned to create new instances.
- Clone: Create a copy of the prototype (shallow or deep copy).
- Registry: Store and manage prototype instances for easy access.

The Prototype pattern is useful when:
- Object creation is expensive (complex initialization, database queries, etc.)
- You need to create many instances with similar state
- You want to avoid tight coupling to concrete classes
- You need to support undo/redo functionality
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Type
from datetime import datetime
from enum import Enum


# ============================================================================
# Prototype Interface & Basic Implementations
# ============================================================================


class Cloneable(ABC):
    """
    Prototype Interface: Defines the contract for cloneable objects.
    
    Any class that implements this interface can be used as a prototype.
    """

    @abstractmethod
    def clone(self) -> Cloneable:
        """
        Create a clone of this object.
        
        Returns:
            A copy of this object.
        """
        pass


# ============================================================================
# Example 1: Document Prototype
# ============================================================================


@dataclass
class DocumentSection:
    """Represents a section within a document."""
    title: str
    content: str
    page_number: int


@dataclass
class Document(Cloneable):
    """
    Prototype: Document.
    
    A complex object that is expensive to create from scratch
    (might involve database queries, file I/O, complex parsing).
    """

    title: str
    author: str
    content: str = ""
    sections: List[DocumentSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)

    def clone(self) -> Document:
        """
        Clone the document.
        
        Uses deepcopy to ensure nested objects are also copied,
        preventing unintended modifications to the original.
        
        Returns:
            A deep copy of this document.
        """
        return deepcopy(self)

    def add_section(self, section: DocumentSection) -> None:
        """Add a section to the document."""
        self.sections.append(section)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the document."""
        self.tags.append(tag)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata key-value pair."""
        self.metadata[key] = value

    def get_summary(self) -> str:
        """Get a summary of the document."""
        return (
            f"Document: {self.title}\n"
            f"Author: {self.author}\n"
            f"Sections: {len(self.sections)}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Metadata: {len(self.metadata)} entries"
        )


# ============================================================================
# Example 2: Game Character Prototype
# ============================================================================


class CharacterClass(Enum):
    """Game character classes."""
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    RANGER = "Ranger"
    PALADIN = "Paladin"


@dataclass
class Skill:
    """Represents a character skill."""
    name: str
    damage: int
    cooldown: float  # Seconds
    mana_cost: int


@dataclass
class GameCharacter(Cloneable):
    """
    Prototype: Game Character.
    
    A complex object representing a game character with equipment,
    skills, and inventory. Creating a new character from scratch
    might require loading from databases or APIs.
    """

    name: str
    character_class: CharacterClass
    level: int = 1
    experience: int = 0
    health: int = 100
    mana: int = 50
    
    # Equipment
    main_weapon: str = "Iron Sword"
    armor_type: str = "Leather Armor"
    
    # Skills
    skills: List[Skill] = field(default_factory=list)
    
    # Inventory
    inventory: Dict[str, int] = field(default_factory=dict)  # item: quantity
    
    # Stats
    strength: int = 10
    agility: int = 10
    intelligence: int = 10
    wisdom: int = 10
    
    # Progress
    quests_completed: int = 0
    achievements: List[str] = field(default_factory=list)

    def clone(self) -> GameCharacter:
        """
        Clone the character.
        
        Creates a new character with the same equipment, skills, and stats.
        Useful for creating character variants or templates.
        
        Returns:
            A deep copy of this character.
        """
        return deepcopy(self)

    def add_skill(self, skill: Skill) -> None:
        """Learn a new skill."""
        self.skills.append(skill)

    def add_inventory_item(self, item: str, quantity: int = 1) -> None:
        """Add an item to inventory."""
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def equip_weapon(self, weapon: str) -> None:
        """Equip a weapon."""
        self.main_weapon = weapon

    def level_up(self) -> None:
        """Increase character level."""
        self.level += 1
        self.health += 10
        self.mana += 5
        self.strength += 1
        self.agility += 1
        self.intelligence += 1
        self.wisdom += 1

    def get_status(self) -> str:
        """Get character status summary."""
        return (
            f"{self.name} - Level {self.level} {self.character_class.value}\n"
            f"Health: {self.health} | Mana: {self.mana}\n"
            f"Strength: {self.strength} | Agility: {self.agility} | "
            f"Intelligence: {self.intelligence} | Wisdom: {self.wisdom}\n"
            f"Equipped: {self.main_weapon} / {self.armor_type}\n"
            f"Skills: {len(self.skills)} | Inventory Items: {sum(self.inventory.values())}\n"
            f"Quests Completed: {self.quests_completed}"
        )


# ============================================================================
# Example 3: UI Component Prototype
# ============================================================================


class UIComponentType(Enum):
    """Types of UI components."""
    BUTTON = "Button"
    TEXT_INPUT = "TextInput"
    CHECKBOX = "Checkbox"
    DROPDOWN = "Dropdown"
    PANEL = "Panel"


@dataclass
class UIStyle:
    """Styling for UI components."""
    background_color: str = "#FFFFFF"
    text_color: str = "#000000"
    border_color: str = "#CCCCCC"
    border_width: int = 1
    font_size: int = 12
    font_family: str = "Arial"
    padding: int = 5
    margin: int = 5


@dataclass
class UIComponent(Cloneable):
    """
    Prototype: UI Component.
    
    Represents a reusable UI component that can be cloned to create
    new instances with similar styling and configuration.
    """

    component_type: UIComponentType
    id: str
    label: str = ""
    width: int = 100
    height: int = 30
    x_position: int = 0
    y_position: int = 0
    
    style: UIStyle = field(default_factory=UIStyle)
    is_enabled: bool = True
    is_visible: bool = True
    
    # Component-specific properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Event handlers
    handlers: Dict[str, str] = field(default_factory=dict)  # event: handler_name

    def clone(self) -> UIComponent:
        """
        Clone the UI component with its styling and configuration.
        
        Returns:
            A deep copy of this component.
        """
        cloned = deepcopy(self)
        # Generate a new ID for the cloned component
        cloned.id = f"{cloned.id}_clone_{int(datetime.now().timestamp())}"
        return cloned

    def set_position(self, x: int, y: int) -> None:
        """Set the component position."""
        self.x_position = x
        self.y_position = y

    def set_size(self, width: int, height: int) -> None:
        """Set the component size."""
        self.width = width
        self.height = height

    def set_property(self, key: str, value: Any) -> None:
        """Set a component-specific property."""
        self.properties[key] = value

    def bind_handler(self, event: str, handler_name: str) -> None:
        """Bind a handler to an event."""
        self.handlers[event] = handler_name

    def get_info(self) -> str:
        """Get component information."""
        return (
            f"{self.component_type.value} [ID: {self.id}]\n"
            f"Label: {self.label}\n"
            f"Position: ({self.x_position}, {self.y_position})\n"
            f"Size: {self.width}x{self.height}\n"
            f"Enabled: {self.is_enabled} | Visible: {self.is_visible}\n"
            f"Style: {self.style.background_color} bg, "
            f"{self.style.text_color} text"
        )


# ============================================================================
# Prototype Registry (Enhancement)
# ============================================================================


class PrototypeRegistry:
    """
    Registry Pattern Enhancement: Manages prototype instances.
    
    Stores prototypes and allows easy access for cloning.
    This is particularly useful when you have many prototypes
    and need to manage them centrally.
    
    Example use case:
    - Game engine storing character templates
    - UI framework storing component templates
    - Document system storing document templates
    """

    def __init__(self):
        """Initialize the registry."""
        self._prototypes: Dict[str, Cloneable] = {}

    def register(self, name: str, prototype: Cloneable) -> None:
        """
        Register a prototype with a name.
        
        Args:
            name: Identifier for the prototype.
            prototype: The prototype object to register.
        """
        self._prototypes[name] = prototype

    def get(self, name: str) -> Optional[Cloneable]:
        """
        Retrieve a registered prototype by name.
        
        Args:
            name: The prototype identifier.
            
        Returns:
            The registered prototype or None if not found.
        """
        return self._prototypes.get(name)

    def clone(self, name: str) -> Optional[Cloneable]:
        """
        Clone a registered prototype.
        
        Args:
            name: The prototype identifier.
            
        Returns:
            A clone of the registered prototype, or None if not found.
        """
        prototype = self.get(name)
        if prototype:
            return prototype.clone()
        return None

    def unregister(self, name: str) -> None:
        """
        Unregister a prototype.
        
        Args:
            name: The prototype identifier to remove.
        """
        if name in self._prototypes:
            del self._prototypes[name]

    def list_prototypes(self) -> List[str]:
        """
        Get a list of all registered prototype names.
        
        Returns:
            List of prototype identifiers.
        """
        return list(self._prototypes.keys())

    def clear(self) -> None:
        """Clear all registered prototypes."""
        self._prototypes.clear()


# ============================================================================
# Document Template Registry (Specialized Registry)
# ============================================================================


class DocumentTemplateRegistry(PrototypeRegistry):
    """
    Specialized Registry: For managing document templates.
    
    Provides convenient methods for registering and accessing
    document prototypes.
    """

    def register_template(self, template_name: str, template: Document) -> None:
        """Register a document template."""
        self.register(template_name, template)

    def create_from_template(self, template_name: str) -> Optional[Document]:
        """
        Create a new document from a registered template.
        
        Args:
            template_name: The name of the template to use.
            
        Returns:
            A new document cloned from the template.
        """
        return self.clone(template_name)

    def list_templates(self) -> List[str]:
        """List all available templates."""
        return self.list_prototypes()


# ============================================================================
# Game Character Template Registry (Specialized Registry)
# ============================================================================


class CharacterTemplateRegistry(PrototypeRegistry):
    """
    Specialized Registry: For managing game character templates.
    
    Provides convenient methods for creating character instances from templates.
    """

    def register_class_template(self, class_name: CharacterClass, template: GameCharacter) -> None:
        """Register a character template for a specific class."""
        self.register(class_name.value.lower(), template)

    def create_character_from_class(self, character_class: CharacterClass) -> Optional[GameCharacter]:
        """
        Create a new character instance from a class template.
        
        Args:
            character_class: The character class.
            
        Returns:
            A new character cloned from the template.
        """
        character = self.clone(character_class.value.lower())
        if character:
            # Give the cloned character a unique name (in practice, user would input this)
            character.name = f"New {character_class.value}"
        return character

    def list_available_classes(self) -> List[str]:
        """List all available character class templates."""
        return self.list_prototypes()


# ============================================================================
# Template Factory Functions
# ============================================================================


def create_document_templates() -> DocumentTemplateRegistry:
    """
    Factory function: Create and populate a document template registry.
    
    Returns:
        A DocumentTemplateRegistry with pre-defined templates.
    """
    registry = DocumentTemplateRegistry()

    # Report template
    report_template = Document(
        title="Annual Report",
        author="Company",
        content="",
        tags=["report", "official"]
    )
    report_template.set_metadata("confidential", True)
    report_template.set_metadata("retention_years", 7)
    registry.register_template("annual_report", report_template)

    # Memo template
    memo_template = Document(
        title="MEMO",
        author="Management",
        tags=["memo", "internal"]
    )
    memo_template.set_metadata("type", "internal_communication")
    registry.register_template("memo", memo_template)

    # Letter template
    letter_template = Document(
        title="Letter",
        author="Company",
        tags=["letter", "formal"]
    )
    letter_template.set_metadata("requires_signature", True)
    registry.register_template("formal_letter", letter_template)

    return registry


def create_character_templates() -> CharacterTemplateRegistry:
    """
    Factory function: Create and populate a character template registry.
    
    Returns:
        A CharacterTemplateRegistry with pre-defined class templates.
    """
    registry = CharacterTemplateRegistry()

    # Warrior template
    warrior = GameCharacter(
        name="Warrior Template",
        character_class=CharacterClass.WARRIOR,
        health=120,
        mana=20,
        strength=15,
        agility=8,
        intelligence=6,
        wisdom=10,
        main_weapon="Great Sword",
        armor_type="Plate Armor"
    )
    warrior.add_skill(Skill("Slash", damage=30, cooldown=1.5, mana_cost=10))
    warrior.add_skill(Skill("Shield Bash", damage=20, cooldown=2.0, mana_cost=15))
    registry.register_class_template(CharacterClass.WARRIOR, warrior)

    # Mage template
    mage = GameCharacter(
        name="Mage Template",
        character_class=CharacterClass.MAGE,
        health=60,
        mana=100,
        strength=6,
        agility=8,
        intelligence=16,
        wisdom=13,
        main_weapon="Staff",
        armor_type="Cloth Armor"
    )
    mage.add_skill(Skill("Fireball", damage=40, cooldown=2.0, mana_cost=40))
    mage.add_skill(Skill("Frost Bolt", damage=35, cooldown=1.8, mana_cost=35))
    registry.register_class_template(CharacterClass.MAGE, mage)

    # Rogue template
    rogue = GameCharacter(
        name="Rogue Template",
        character_class=CharacterClass.ROGUE,
        health=75,
        mana=30,
        strength=10,
        agility=16,
        intelligence=9,
        wisdom=8,
        main_weapon="Dagger",
        armor_type="Leather Armor"
    )
    rogue.add_skill(Skill("Backstab", damage=45, cooldown=2.0, mana_cost=30))
    rogue.add_skill(Skill("Evasion", damage=0, cooldown=1.0, mana_cost=20))
    registry.register_class_template(CharacterClass.ROGUE, rogue)

    return registry


def create_ui_component_templates() -> PrototypeRegistry:
    """
    Factory function: Create and populate a UI component template registry.
    
    Returns:
        A PrototypeRegistry with pre-defined UI component templates.
    """
    registry = PrototypeRegistry()

    # Primary Button template
    primary_button = UIComponent(
        component_type=UIComponentType.BUTTON,
        id="btn_primary",
        label="Click Me",
        width=120,
        height=40,
        style=UIStyle(
            background_color="#0066CC",
            text_color="#FFFFFF",
            border_color="#004488",
            border_width=2,
            font_size=14
        )
    )
    primary_button.bind_handler("click", "on_button_click")
    registry.register("primary_button", primary_button)

    # Text Input template
    text_input = UIComponent(
        component_type=UIComponentType.TEXT_INPUT,
        id="txt_input",
        label="Enter text:",
        width=300,
        height=35,
        style=UIStyle(
            background_color="#FFFFFF",
            text_color="#000000",
            border_color="#AAAAAA",
            border_width=1,
            font_size=12
        )
    )
    text_input.set_property("placeholder", "Enter your input here...")
    registry.register("text_input", text_input)

    # Checkbox template
    checkbox = UIComponent(
        component_type=UIComponentType.CHECKBOX,
        id="chk_agree",
        label="I agree",
        width=20,
        height=20,
        style=UIStyle(
            background_color="#FFFFFF",
            border_color="#666666",
            border_width=1
        )
    )
    checkbox.set_property("checked", False)
    registry.register("checkbox", checkbox)

    return registry
