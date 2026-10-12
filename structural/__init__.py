"""
Structural Patterns

Design patterns that deal with object composition, creating relationships between entities.
These patterns are concerned with how classes and objects are composed to form larger structures
while keeping these structures flexible and efficient. They help ensure that when one part changes,
the entire structures don't need to change, only the composition changes.

This module provides seven fundamental structural patterns:

1. **Adapter** - Convert interface of one class to another clients expect
2. **Bridge** - Decouple abstraction from implementation
3. **Composite** - Compose objects into tree structures
4. **Decorator** - Attach additional responsibilities dynamically
5. **Facade** - Provide unified interface to complex subsystem
6. **Flyweight** - Share objects efficiently for large-scale systems
7. **Proxy** - Provide surrogate or placeholder for another object

Usage Examples:
    # Adapter - interface translation
    from structural import Adapter, Target

    # Bridge - decouple abstraction/implementation
    from structural import Abstraction, Implementor

    # Composite - tree structures
    from structural import Component, Leaf, Composite

    # Decorator - add behavior dynamically
    from structural import Decorator, Component as DecoratorComponent

    # Facade - simplified interface
    from structural import Facade, Subsystem1

    # Flyweight - share objects
    from structural import FlyweightFactory, Flyweight

    # Proxy - control access
    from structural import Proxy, Subject

See README.md for comprehensive comparison and best practices.
"""

# Adapter Pattern
from .adapter.pattern import (
    Adaptee,
    Adapter,
    AdapterRegistry,
    AdapterWithValidation,
    LegacySystem,
    LegacySystemAdapter,
    Target,
    TwoWayAdapter,
)
from .adapter.real_world_example import (
    PaymentProcessor,
    PaymentSystem,
    PayPalAdapter,
    PayPalPaymentGateway,
    StripeAdapter,
    StripePaymentGateway,
)

# Bridge Pattern
from .bridge.pattern import (
    SVGAPI,
)
from .bridge.pattern import Abstraction as BridgeAbstraction
from .bridge.pattern import (
    CanvasAPI,
    Circle,
    ConcreteImplementorA,
    ConcreteImplementorB,
    DrawingAPI,
    Implementor,
    Line,
    Rectangle,
    RefinedAbstraction,
    Shape,
    ShapeComposer,
)
from .bridge.real_world_example import (
    BluetoothBridge,
    CommunicationBridge,
    InfraredBridge,
    ProjectorRemote,
    RemoteControl,
    RemoteControlFactory,
    StereoRemote,
    TVRemote,
    WiFiBridge,
)

# Composite Pattern
from .composite.pattern import (
    Component,
    Composite,
    Department,
    Directory,
    Employee,
    File,
    FileSystemComponent,
    Leaf,
    Menu,
    MenuComponent,
    MenuItem,
    OrganizationComponent,
)
from .composite.real_world_example import (
    BulletList,
    Document,
    DocumentBuilder,
    Heading,
    Paragraph,
    Section,
    TextElement,
)

# Decorator Pattern
from .decorator.pattern import (
    BorderDecorator,
    Coffee,
    CoffeeBuilder,
    CoffeeDecorator,
)
from .decorator.pattern import Component as DecoratorComponent
from .decorator.pattern import (
    CompressionDecorator,
    ConcreteComponent,
    ConcreteDecoratorA,
    ConcreteDecoratorB,
    DataSource,
    DataSourceDecorator,
    Decorator,
    EncryptionDecorator,
    FileDataSource,
    LoggingDecorator,
    MilkDecorator,
    ScrollDecorator,
    ShadowDecorator,
    SimpleCoffee,
    SimpleWidget,
    SugarDecorator,
    VanillaDecorator,
    WhippedCreamDecorator,
    Widget,
    WidgetDecorator,
)
from .decorator.real_world_example import (
    BufferedStreamDecorator,
    CompressionStreamDecorator,
    EncryptionStreamDecorator,
    FileStream,
    Stream,
    StreamDecorator,
)

# Facade Pattern
from .facade.pattern import (
    CacheManager,
    DatabaseConnection,
    Facade,
    InventoryService,
    LogManager,
    NotificationService,
    OrderFacade,
    PaymentGateway,
    RepositoryFacade,
    Subsystem1,
    Subsystem2,
)
from .facade.real_world_example import (
    CPU,
    ComputerFacade,
    HardDrive,
    Memory,
)

# Flyweight Pattern
from .flyweight.pattern import (
    Character,
    CharacterStyle,
    CharacterStyleFactory,
    Flyweight,
    FlyweightFactory,
    Image,
    ImageFactory,
    ImageReference,
    Particle,
    ParticleFactory,
    ParticleInstance,
    Tree,
    TreeFactory,
    TreeType,
)
from .flyweight.real_world_example import (
    Font,
    FontFactory,
    TextRenderer,
)

# Proxy Pattern
from .proxy.pattern import (
    Database,
    DatabaseProxy,
    DataValidator,
)
from .proxy.pattern import Image as ProxyImage
from .proxy.pattern import (
    ImageProxy,
    LoggingProxy,
    ProtectionProxy,
    Proxy,
    RealDatabase,
    RealImage,
    RealService,
    RealSubject,
    Service,
    Subject,
    ValidationProxy,
)
from .proxy.real_world_example import (
    ExpensiveRemoteService,
    RemoteService,
    RemoteServiceProxy,
)

__all__ = [
    # Adapter
    "Target",
    "Adaptee",
    "Adapter",
    "TwoWayAdapter",
    "LegacySystem",
    "LegacySystemAdapter",
    "AdapterWithValidation",
    "AdapterRegistry",
    "PaymentProcessor",
    "StripePaymentGateway",
    "PayPalPaymentGateway",
    "StripeAdapter",
    "PayPalAdapter",
    "PaymentSystem",
    # Bridge
    "Implementor",
    "ConcreteImplementorA",
    "ConcreteImplementorB",
    "BridgeAbstraction",
    "RefinedAbstraction",
    "DrawingAPI",
    "CanvasAPI",
    "SVGAPI",
    "Shape",
    "Circle",
    "Rectangle",
    "Line",
    "ShapeComposer",
    "CommunicationBridge",
    "WiFiBridge",
    "BluetoothBridge",
    "InfraredBridge",
    "RemoteControl",
    "TVRemote",
    "StereoRemote",
    "ProjectorRemote",
    "RemoteControlFactory",
    # Composite
    "Component",
    "Leaf",
    "Composite",
    "FileSystemComponent",
    "File",
    "Directory",
    "OrganizationComponent",
    "Employee",
    "Department",
    "MenuComponent",
    "MenuItem",
    "Menu",
    "TextElement",
    "Paragraph",
    "Heading",
    "BulletList",
    "Section",
    "Document",
    "DocumentBuilder",
    # Decorator
    "DecoratorComponent",
    "ConcreteComponent",
    "Decorator",
    "ConcreteDecoratorA",
    "ConcreteDecoratorB",
    "DataSource",
    "FileDataSource",
    "DataSourceDecorator",
    "EncryptionDecorator",
    "CompressionDecorator",
    "LoggingDecorator",
    "Coffee",
    "SimpleCoffee",
    "CoffeeDecorator",
    "MilkDecorator",
    "SugarDecorator",
    "WhippedCreamDecorator",
    "VanillaDecorator",
    "CoffeeBuilder",
    "Widget",
    "SimpleWidget",
    "WidgetDecorator",
    "BorderDecorator",
    "ScrollDecorator",
    "ShadowDecorator",
    "Stream",
    "FileStream",
    "StreamDecorator",
    "CompressionStreamDecorator",
    "EncryptionStreamDecorator",
    "BufferedStreamDecorator",
    # Facade
    "Subsystem1",
    "Subsystem2",
    "Facade",
    "DatabaseConnection",
    "CacheManager",
    "LogManager",
    "RepositoryFacade",
    "PaymentGateway",
    "NotificationService",
    "InventoryService",
    "OrderFacade",
    "CPU",
    "Memory",
    "HardDrive",
    "ComputerFacade",
    # Flyweight
    "Flyweight",
    "FlyweightFactory",
    "TreeType",
    "Tree",
    "TreeFactory",
    "CharacterStyle",
    "Character",
    "CharacterStyleFactory",
    "Image",
    "ImageReference",
    "ImageFactory",
    "Particle",
    "ParticleInstance",
    "ParticleFactory",
    "Font",
    "FontFactory",
    "TextRenderer",
    # Proxy
    "Subject",
    "RealSubject",
    "Proxy",
    "ProxyImage",
    "RealImage",
    "ImageProxy",
    "Database",
    "RealDatabase",
    "DatabaseProxy",
    "Service",
    "RealService",
    "ProtectionProxy",
    "DataValidator",
    "ValidationProxy",
    "LoggingProxy",
    "RemoteService",
    "ExpensiveRemoteService",
    "RemoteServiceProxy",
]
