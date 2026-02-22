"""
Creational Patterns

Design patterns that deal with object creation mechanisms, trying to create
objects in a manner suitable to the situation. These patterns abstract the
instantiation process to make systems independent of how their objects are
composed and represented.

This module provides five fundamental creational patterns:

1. **Singleton** - Ensure a class has only one instance with global access
2. **Factory Method** - Define creation interface, let subclasses decide
3. **Abstract Factory** - Create families of related objects
4. **Builder** - Construct complex objects step-by-step
5. **Prototype** - Create objects by cloning existing prototypes

Usage Examples:
    # Singleton - single instance
    from creational import SingletonMeta
    
    # Factory Method - deferred instantiation
    from creational import TransportFactory
    
    # Abstract Factory - family of products
    from creational import UIFactory
    
    # Builder - complex object construction
    from creational import HTTPRequestBuilder
    
    # Prototype - object cloning
    from creational import PrototypeRegistry, Document

See README.md for comprehensive comparison and best practices.
"""

# Singleton Pattern
from .singleton.pattern import SingletonMeta, FeatureFlagService

# Factory Method Pattern
from .factory.pattern import (
    Transport,
    HTTPTransport,
    HTTPSTransport,
    FTPTransport,
    WebSocketTransport,
    TransportFactory,
    HTTPFactory,
    HTTPSFactory,
    FTPFactory,
    WebSocketFactory,
    TransportFactoryRegistry,
)

# Abstract Factory Pattern
from .abstract_factory.pattern import (
    Button,
    Checkbox,
    TextInput,
    UIFactory,
    LightUIFactory,
    DarkUIFactory,
    HighContrastUIFactory,
    UIFactoryRegistry,
)

# Builder Pattern
from .builder.pattern import (
    HTTPRequest,
    HTTPRequestBuilder,
    Computer,
    ComputerBuilder,
    RequestTemplates,
    ComputerTemplates,
)

# Prototype Pattern
from .prototype.pattern import (
    Cloneable,
    DocumentSection,
    Document,
    CharacterClass,
    Skill,
    GameCharacter,
    UIComponentType,
    UIStyle,
    UIComponent,
    PrototypeRegistry,
    DocumentTemplateRegistry,
    CharacterTemplateRegistry,
    create_document_templates,
    create_character_templates,
    create_ui_component_templates,
)

__all__ = [
    # Singleton
    "SingletonMeta",
    "FeatureFlagService",
    
    # Factory Method
    "Transport",
    "HTTPTransport",
    "HTTPSTransport",
    "FTPTransport",
    "WebSocketTransport",
    "TransportFactory",
    "HTTPFactory",
    "HTTPSFactory",
    "FTPFactory",
    "WebSocketFactory",
    "TransportFactoryRegistry",
    
    # Abstract Factory
    "Button",
    "Checkbox",
    "TextInput",
    "UIFactory",
    "LightUIFactory",
    "DarkUIFactory",
    "HighContrastUIFactory",
    "UIFactoryRegistry",
    
    # Builder
    "HTTPRequest",
    "HTTPRequestBuilder",
    "Computer",
    "ComputerBuilder",
    "RequestTemplates",
    "ComputerTemplates",
    
    # Prototype
    "Cloneable",
    "DocumentSection",
    "Document",
    "CharacterClass",
    "Skill",
    "GameCharacter",
    "UIComponentType",
    "UIStyle",
    "UIComponent",
    "PrototypeRegistry",
    "DocumentTemplateRegistry",
    "CharacterTemplateRegistry",
    "create_document_templates",
    "create_character_templates",
    "create_ui_component_templates",
]
