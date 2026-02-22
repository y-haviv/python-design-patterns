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
    Target,
    Adaptee,
    Adapter,
    TwoWayAdapter,
    LegacySystem,
    LegacySystemAdapter,
    AdapterWithValidation,
    AdapterRegistry,
    PaymentProcessor,
    StripePaymentGateway,
    PayPalPaymentGateway,
    StripeAdapter,
    PayPalAdapter,
    PaymentSystem,
)

# Bridge Pattern
from .bridge.pattern import (
    Implementor,
    ConcreteImplementorA,
    ConcreteImplementorB,
    Abstraction as BridgeAbstraction,
    RefinedAbstraction,
    DrawingAPI,
    CanvasAPI,
    SVGAPI,
    Shape,
    Circle,
    Rectangle,
    Line,
    ShapeComposer,
    CommunicationBridge,
    WiFiBridge,
    BluetoothBridge,
    InfraredBridge,
    RemoteControl,
    TVRemote,
    StereoRemote,
    ProjectorRemote,
    RemoteControlFactory,
)

# Composite Pattern
from .composite.pattern import (
    Component,
    Leaf,
    Composite,
    FileSystemComponent,
    File,
    Directory,
    OrganizationComponent,
    Employee,
    Department,
    MenuComponent,
    MenuItem,
    Menu,
    TextElement,
    Paragraph,
    Heading,
    BulletList,
    Section,
    Document,
    DocumentBuilder,
)

# Decorator Pattern
from .decorator.pattern import (
    Component as DecoratorComponent,
    ConcreteComponent,
    Decorator,
    ConcreteDecoratorA,
    ConcreteDecoratorB,
    DataSource,
    FileDataSource,
    DataSourceDecorator,
    EncryptionDecorator,
    CompressionDecorator,
    LoggingDecorator,
    Coffee,
    SimpleCoffee,
    CoffeeDecorator,
    MilkDecorator,
    SugarDecorator,
    WhippedCreamDecorator,
    VanillaDecorator,
    CoffeeBuilder,
    Widget,
    SimpleWidget,
    WidgetDecorator,
    BorderDecorator,
    ScrollDecorator,
    ShadowDecorator,
    Stream,
    FileStream,
    StreamDecorator,
    CompressionStreamDecorator,
    EncryptionStreamDecorator,
    BufferedStreamDecorator,
)

# Facade Pattern
from .facade.pattern import (
    Subsystem1,
    Subsystem2,
    Facade,
    DatabaseConnection,
    CacheManager,
    LogManager,
    RepositoryFacade,
    PaymentGateway,
    NotificationService,
    InventoryService,
    OrderFacade,
    CPU,
    Memory,
    HardDrive,
    ComputerFacade,
)

# Flyweight Pattern
from .flyweight.pattern import (
    Flyweight,
    FlyweightFactory,
    TreeType,
    Tree,
    TreeFactory,
    CharacterStyle,
    Character,
    CharacterStyleFactory,
    Image,
    ImageReference,
    ImageFactory,
    Particle,
    ParticleInstance,
    ParticleFactory,
    Font,
    FontFactory,
    TextRenderer,
)

# Proxy Pattern
from .proxy.pattern import (
    Subject,
    RealSubject,
    Proxy,
    Image as ProxyImage,
    RealImage,
    ImageProxy,
    Database,
    RealDatabase,
    DatabaseProxy,
    Service,
    RealService,
    ProtectionProxy,
    DataValidator,
    ValidationProxy,
    LoggingProxy,
    RemoteService,
    ExpensiveRemoteService,
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
