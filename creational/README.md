# Creational Patterns

> Design patterns that deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

## Overview

Creational patterns are concerned with the process of object creation. They abstract the instantiation process to make systems independent of how their objects are composed and represented. This becomes important as systems evolve to depend more on object composition than inheritance.

The key insight of creational patterns is that you should not instantiate objects directly using classes. Instead, you should use abstract mechanisms that decouple the client code from the specific classes being instantiated. This allows systems to be independent of how objects are created, combined, and represented.

### Why Creational Patterns Matter

#### Problem Without Creational Patterns

When object creation is tightly coupled to specific classes:
- **Hard to extend:** Adding new types requires modifying client code
- **Complex instantiation:** Clients must know all the details
- **Inflexible:** Difficult to introduce variations or alternatives
- **Difficult testing:** Can't easily mock or substitute implementations
- **Violates Single Responsibility:** Classes handle both business logic and creation

#### Advantages of Creational Patterns

- **Abstraction:** Hide concrete class details from clients
- **Flexibility:** Introduce new object types without changing existing code
- **Encapsulation:** Centralize object creation logic
- **Consistency:** Ensure objects are created following specific rules
- **Testability:** Can mock or substitute implementations for testing

---

## Pattern Catalog

### 1. **Singleton** - One Instance to Rule Them All

Ensure a class has only one instance and provide a global point of access to it.

| Aspect | Details |
|--------|---------|
| **Intent** | Ensure single instance with controlled access |
| **Problem** | Need exactly one object globally accessible |
| **Solution** | Prevent multiple instances through class design |
| **Use Cases** | Configuration managers, databases, loggers, file systems |
| **Complexity** | Low |

#### Key Characteristics

```
┌─────────────────────┐
│    Singleton        │
├─────────────────────┤
│ - _instance         │
│ - __new__()         │ (Thread-safe creation)
│ - get_instance()    │
└─────────────────────┘
```

**When to use:**
- Exactly one object needed (logger, database connection pool, thread pool)
- Global access required
- Must be thread-safe in multi-threaded environments

**Implementation strategies:**
- Eager initialization (created at class load time)
- Lazy initialization (created on first access)
- Thread-safe lazy initialization (double-checked locking)
- Metaclass approach (most Pythonic)

**Real-world example:**
```python
class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

See [singleton/README.md](singleton/README.md) for full details.

---

### 2. **Factory Method** - Instantiation Delegation

Define an interface for creating an object, but let subclasses decide which class to instantiate.

| Aspect | Details |
|--------|---------|
| **Intent** | Defer object creation to subclasses |
| **Problem** | Need to create objects of different types without knowing exact classes |
| **Solution** | Define factory interface, implement in subclasses |
| **Use Cases** | UI frameworks, document processors, transport layer, database drivers |
| **Complexity** | Medium |

#### Key Characteristics

```
┌──────────────────────────┐
│   Creator (Abstract)     │
├──────────────────────────┤
│ + factory_method()       │◄─── Deferred to subclasses
│ + business_logic()       │
└──────────────────────────┘
           △
           │ Inheritance
┌──────────────────────────────────────┐
│        ConcreteCreator               │
├──────────────────────────────────────┤
│ + factory_method()                   │◄─── Returns ConcreteProduct
│    return ConcreteProduct()          │
└──────────────────────────────────────┘
```

**When to use:**
- Client doesn't know exact object type needed
- Object creation is complex or algorithm-specific
- Multiple subclasses need different object types
- Decoupling client from concrete classes is important

**Implementation strategies:**
- Simple factory method in each subclass
- Factory registry for dynamic type selection
- Factory with templates for pre-built configurations

**Real-world example:**
```python
class TransportFactory:
    def create_transport(self) -> Transport:
        raise NotImplementedError()

class HTTPFactory(TransportFactory):
    def create_transport(self) -> Transport:
        return HTTPTransport()
```

**Comparison with Abstract Factory:**
- Factory Method: Creates single products
- Abstract Factory: Creates families of related products

See [factory/README.md](factory/README.md) for full details.

---

### 3. **Abstract Factory** - Family Creator

Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

| Aspect | Details |
|--------|---------|
| **Intent** | Create families of related objects together |
| **Problem** | Need related objects to work together consistently |
| **Solution** | Define factory interface that creates entire families |
| **Use Cases** | UI themes, database abstraction, rendering engines, operating system components |
| **Complexity** | High |

#### Key Characteristics

```
┌────────────────────┐
│   UIFactory        │◄─── Abstract Factory Interface
├────────────────────┤
│ + create_button()  │
│ + create_input()   │
│ + create_checkbox()│
└────────────────────┘
           △
           │
┌─────────────────────────────────────────┐
│      LightThemeFactory                  │
├─────────────────────────────────────────┤
│ + create_button() → LightButton         │◄─── Button family
│ + create_input() → LightInput           │◄─── Input family
│ + create_checkbox() → LightCheckbox     │◄─── Checkbox family
└─────────────────────────────────────────┘
```

**When to use:**
- Multiple families of related objects exist
- Objects from same family must work together
- System should be independent of object creation
- Need to swap entire families (e.g., themes, database backends)

**Implementation strategies:**
- Separate abstract factory for each family
- Factory registry for selecting active family
- Context object tracking current factory

**Real-world examples:**

1. **UI Themes:**
   - Light theme: LightButton, LightCheckbox, LightInput
   - Dark theme: DarkButton, DarkCheckbox, DarkInput
   - Each theme is a family of coordinated components

2. **Database Support:**
   - PostgreSQL family: PostgreSQLConnection, PostgreSQLQueryBuilder
   - MySQL family: MySQLConnection, MySQLQueryBuilder
   - Consistent API regardless of database choice

**Comparison with Factory Method:**
- Factory Method: Single product per factory
- Abstract Factory: Multiple related products per factory

See [abstract_factory/README.md](abstract_factory/README.md) for full details.

---

### 4. **Builder** - Complex Object Construction

Separate the construction of a complex object from its representation, allowing the same construction process to create different representations.

| Aspect | Details |
|--------|---------|
| **Intent** | Construct complex objects step-by-step |
| **Problem** | Constructing object with many optional parameters is complex and error-prone |
| **Solution** | Use fluent interface to build objects incrementally |
| **Use Cases** | Request/response objects, configuration objects, query builders, UI builders |
| **Complexity** | Medium-High |

#### Key Characteristics

```
┌──────────────────────────────┐
│     Product (Complex)        │
├──────────────────────────────┤
│ - parameter1                 │
│ - parameter2                 │
│ - parameter3                 │
│ - ...                        │
└──────────────────────────────┘
           △
           │ Built by
┌──────────────────────────────┐
│        Builder               │
├──────────────────────────────┤
│ + with_parameter1()          │◄─── Fluent interface
│ + with_parameter2()          │     (returns self)
│ + build() → Product          │
└──────────────────────────────┘
```

**When to use:**
- Object has many optional parameters
- Constructor would have too many parameters
- Object construction involves complex initialization
- Object representation varies but construction process is similar
- Need immutable objects with flexible initialization

**Implementation strategies:**
- Fluent builder with method chaining
- Builder with templates/directors for pre-built configurations
- Immutable object with builder pattern

**Real-world examples:**

1. **HTTP Request Builder:**
   ```python
   request = (HTTPRequestBuilder()
       .with_url("http://api.example.com")
       .with_method("POST")
       .with_header("Authorization", "Bearer token")
       .with_json_body({"key": "value"})
       .build())
   ```

2. **SQL Query Builder:**
   ```python
   query = (QueryBuilder()
       .select("id", "name", "email")
       .from_("users")
       .where("age > 18")
       .order_by("name")
       .limit(10)
       .build())
   ```

**Comparison with Factory Method:**
- Factory Method: Quick object creation
- Builder: Gradual construction with configuration

See [builder/README.md](builder/README.md) for full details.

---

### 5. **Prototype** - Clone and Modify

Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

| Aspect | Details |
|--------|---------|
| **Intent** | Create objects by cloning prototypes |
| **Problem** | Creating objects is expensive; want to reuse existing well-configured objects |
| **Solution** | Copy existing objects rather than creating from scratch |
| **Use Cases** | Design system themes, game entity templates, document templates, configuration presets |
| **Complexity** | Medium |

#### Key Characteristics

```
┌──────────────────────────┐
│     Prototype            │
├──────────────────────────┤
│ + clone() → Prototype    │◄─── Deep copy
│ + get_property()         │
│ + set_property()         │
└──────────────────────────┘
           △
           │ Implements
┌──────────────────────────┐
│  PrototypeRegistry       │
├──────────────────────────┤
│ - prototypes: Dict       │
│ + register()             │◄─── Store templates
│ + clone()                │◄─── Create copies
│ + list_prototypes()      │
└──────────────────────────┘
```

**When to use:**
- Object creation is expensive (complex initialization, database queries)
- Need many similar objects with minor variations
- Object state is important and should be preserved
- Want to avoid subclassing for different configurations

**Implementation strategies:**
- Shallow copy (for simple objects)
- Deep copy (for complex nested objects)
- Clone registry for centralized template management
- Specialized registries for different object types

**Real-world examples:**

1. **Design System Themes:**
   - Create light theme prototype
   - Clone and modify for dark theme
   - Clone and modify for high-contrast theme
   All based on single light theme prototype

2. **Game Character Templates:**
   - Create warrior template with base stats
   - Clone for each new warrior instance
   - Customize specific warrior attributes

3. **Document Templates:**
   - Annual report template with standard sections
   - Clone for yearly reports, modify title/date
   - Preserve consistent structure

**Key Implementation Detail - Deep Copy:**
```python
def clone(self):
    """Create independent deep copy."""
    # Must use deepcopy for nested objects
    return deepcopy(self)
```

See [prototype/README.md](prototype/README.md) for full details.

---

## Decision Tree: Which Pattern to Use?

```
Need to control object creation?
│
├─ YES: Is exactly ONE instance required?
│   └─ YES → Use SINGLETON
│   └─ NO: Proceed below
│
└─ NO: How many related objects do clients need?
    │
    ├─ One object type, clients shouldn't know concrete class
    │   └─ Use FACTORY METHOD
    │
    ├─ Multiple related objects that must work together
    │   └─ Use ABSTRACT FACTORY
    │
    ├─ Single complex object with many optional parameters
    │   └─ Use BUILDER
    │
    └─ Creating objects is expensive, reuse existing templates
        └─ Use PROTOTYPE
```

### Selection Criteria

| Criterion | Pattern |
|-----------|---------|
| **Single instance required** | Singleton |
| **Unknown concrete class at runtime** | Factory Method |
| **Need multiple related objects** | Abstract Factory |
| **Many optional parameters** | Builder |
| **Object creation is expensive** | Prototype |
| **Want immutable objects** | Builder + Prototype |
| **Deferred initialization** | Singleton, Lazy Factory |
| **Runtime flexibility** | Factory Method, Abstract Factory |

---

## Pattern Relationships

### Complementary Patterns

Creational patterns often work together:

1. **Abstract Factory + Factory Method:**
   - Abstract Factory typically uses Factory Method internally
   - Each concrete factory implements factory method

2. **Builder + Factory Method:**
   - Factory Method for simple objects
   - Builder for complex object configurations

3. **Singleton + Repository:**
   - Singleton pattern for single data access point
   - Often combined with Repository pattern

4. **Prototype + Factory:**
   - Prototype for cloning templates
   - Factory registry for managing prototypes

5. **Builder + Singleton:**
   - Singleton configuration manager
   - Builder for constructing complex requests using config

### Anti-patterns Avoided

1. **All objects are singletons:** Leads to global state and tight coupling
2. **Multiple factory levels:** Unnecessary complexity
3. **Over-abstraction:** Too many interfaces for simple tasks
4. **Conflicting patterns:** Don't mix incompatible creation strategies in same class

---

## Best Practices

### General Principles

1. **Encapsulation First**
   ```python
   # ✓ Good: Hide creation details
   user = UserFactory.create_admin(name="Alice")
   
   # ✗ Bad: Expose creation details
   user = User(name="Alice", role="admin", permissions=[...])
   ```

2. **Use Interfaces/ABCs**
   ```python
   # ✓ Good: Depend on abstraction
   def process(factory: TransportFactory) -> None:
       transport = factory.create_transport()
   
   # ✗ Bad: Depend on concrete class
   def process(factory: HTTPFactory) -> None:
       transport = factory.create_transport()
   ```

3. **Minimize Coupling**
   ```python
   # ✓ Good: Factory returns interface
   def get_factory() -> DataFactory:
       ...
   
   # ✗ Bad: Direct class dependencies
   factory = PostgreSQLFactory()
   ```

4. **Provide Sensible Defaults**
   ```python
   # ✓ Good: Builder with defaults
   request = HTTPRequestBuilder().build()  # Uses sensible defaults
   
   # ✗ Bad: Incomplete objects
   request = HTTPRequest()  # What values does it have?
   ```

### Pattern-Specific Best Practices

#### Singleton

- ✓ Use for: Configuration, logging, database pools
- ✓ Make thread-safe if multi-threaded
- ✗ Avoid: Application state, user data
- ✗ Don't expose as global without careful design

#### Factory Method

- ✓ Use one factory per product type
- ✓ Keep factory methods focused
- ✓ Use registry for dynamic selection
- ✗ Don't create God factories (handles too many types)

#### Abstract Factory

- ✓ Keep families closely related
- ✓ Use factory registry for switching implementations
- ✓ Ensure products are truly compatible
- ✗ Don't mix unrelated products in same family

#### Builder

- ✓ Return `self` for method chaining
- ✓ Provide sensible defaults
- ✓ Use for 4+ optional parameters
- ✓ Consider immutability of built objects
- ✗ Don't use for objects with few parameters

#### Prototype

- ✓ Use for expensive-to-create objects
- ✓ Use deep copy for nested objects
- ✓ Maintain prototype registry
- ✓ Clone before returning to prevent external modification
- ✗ Don't use shallow copy for complex nested objects

### Code Organization

```
creational/
├── singleton/
│   ├── __init__.py
│   ├── pattern.py           # Core pattern implementation
│   ├── README.md            # Detailed documentation
│   ├── real_world_example.py # Practical example
│   └── test_pattern.py      # Comprehensive tests
│
├── factory/
│   ├── __init__.py
│   ├── pattern.py
│   ├── README.md
│   ├── real_world_example.py
│   └── test_pattern.py
│
└── ... (other patterns follow same structure)
```

---

## Common Implementation Patterns

### Registry Pattern

Used across all patterns for centralized management:

```python
class PatternRegistry:
    """Manage pattern instances/templates."""
    
    def __init__(self):
        self._registry: dict[str, Any] = {}
    
    def register(self, name: str, item: Any) -> None:
        self._registry[name] = item
    
    def get(self, name: str) -> Any | None:
        return self._registry.get(name)
    
    def list_items(self) -> list[str]:
        return list(self._registry.keys())
```

### Template Pattern Integration

Directors and templates for pre-configured objects:

```python
class Builder:
    """Base builder with template support."""
    
    def build(self) -> Product:
        raise NotImplementedError()

class Director:
    """Pre-builds common configurations."""
    
    def __init__(self, builder: Builder):
        self.builder = builder
    
    def build_standard_config(self) -> Product:
        # Sequence of builder calls
        self.builder.step1()
        self.builder.step2()
        return self.builder.build()
```

### Fluent Interface

Used in builders for readable object construction:

```python
request = (HTTPRequestBuilder()
    .with_url(url)
    .with_method("POST")
    .with_headers(headers)
    .with_body(body)
    .build())
```

---

## Performance Considerations

### Singleton
- **Initialization time:** O(1) amortized
- **Access time:** O(1)
- **Memory:** Single instance overhead

### Factory Method
- **Creation time:** O(n) where n = subclass count
- **Lookup time:** O(1) with registry, O(n) without
- **Memory:** Factory per type

### Abstract Factory
- **Creation time:** O(1) per product
- **Lookup time:** O(1) with registry
- **Memory:** Set of related factories

### Builder
- **Construction time:** O(m) where m = builder steps
- **Build time:** O(c) where c = complexity
- **Memory:** Builder object (temporary)

### Prototype
- **Cloning time:** O(n) where n = object size
- **Initialization savings:** Significant for complex objects
- **Memory:** Original + clones

---

## Common Pitfalls and Solutions

### Pitfall 1: Over-abstraction

**Problem:** Using patterns for simple objects
```python
# ✗ Too much abstraction
factory = SimpleFactory()
object = factory.create()
```

**Solution:** Use patterns only when beneficial
```python
# ✓ Direct instantiation for simple cases
object = SimpleClass(param)

# Use pattern when justified
manager = DataFactory.get_manager(database_type)
```

### Pitfall 2: Rigid Class Hierarchies

**Problem:** Factory hierarchy too deep
```python
# ✗ Too many levels
Factory > ConcreteFactory > SpecificFactory
```

**Solution:** Use composition over inheritance
```python
# ✓ Registry for flexibility
registry = FactoryRegistry()
factory = registry.get("type")
```

### Pitfall 3: Creating God Objects

**Problem:** One factory/builder handles everything
```python
# ✗ God factory
class SuperFactory:
    def create_anything(self): ...
```

**Solution:** Separate concerns
```python
# ✓ Focused factories
class TransportFactory: ...
class DatabaseFactory: ...
```

### Pitfall 4: Shallow Copy Issues

**Problem:** Prototype not deep copying nested objects
```python
# ✗ Shallow copy (modifications affect original)
def clone(self):
    return copy.copy(self)
```

**Solution:** Use deep copy for complex objects
```python
# ✓ Deep copy for nested objects
def clone(self):
    return copy.deepcopy(self)
```

### Pitfall 5: Inconsistent Interfaces

**Problem:** Different factories create incompatible objects
```python
# ✗ Incompatible families
factory1.create_button()  # Returns ButtonV1
factory2.create_button()  # Returns ButtonV2
```

**Solution:** Enforce interface contracts
```python
# ✓ Same interface
factory1.create_ui_component()  # Returns UIComponent
factory2.create_ui_component()  # Returns UIComponent
```

---

## Testing Creational Patterns

### Key Test Scenarios

1. **Object Identity**
   - Singleton: Only one instance exists
   - Other patterns: Multiple instances possible

2. **Independence**
   - Factory: Each instance independent
   - Prototype: Clones don't affect originals
   - Builder: Built objects have correct state

3. **Interface Compliance**
   - Products implement required interface
   - Factories produce compatible products

4. **Registry Operations**
   - Registration, retrieval, removal
   - List operations

5. **Thread Safety**
   - Multiple threads get correct instances
   - No race conditions

### Example Test Structure

```python
class TestFactoryMethod:
    def test_creates_correct_type(self):
        factory = HTTPFactory()
        product = factory.create()
        assert isinstance(product, Transport)
    
    def test_each_call_returns_new_instance(self):
        factory = HTTPFactory()
        obj1 = factory.create()
        obj2 = factory.create()
        assert obj1 is not obj2
    
    def test_product_is_usable(self):
        factory = HTTPFactory()
        transport = factory.create()
        assert transport.is_available()
```

---

## Quick Reference

### When to Use Each Pattern

| Scenario | Pattern | Why |
|----------|---------|-----|
| Global configuration needed | Singleton | Need single access point |
| Hide concrete class from client | Factory Method | Decouple client from implementation |
| Related objects must work together | Abstract Factory | Ensure compatibility |
| Complex multi-step construction | Builder | Reduce parameter complexity |
| Cloning expensive-to-create objects | Prototype | Save initialization cost |
| Multiple implementations | Any factory pattern | Allow swapping implementations |
| Immutable objects with flexible config | Builder | Immutability + flexibility |
| Centralized object management | Singleton + Registry | Control and access |

---

## See Also

- [Singleton Pattern - Wikipedia](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Factory Method Pattern - Wikipedia](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [Abstract Factory Pattern - Wikipedia](https://en.wikipedia.org/wiki/Abstract_factory_pattern)
- [Builder Pattern - Wikipedia](https://en.wikipedia.org/wiki/Builder_pattern)
- [Prototype Pattern - Wikipedia](https://en.wikipedia.org/wiki/Prototype_pattern)
- [singleton/README.md](singleton/README.md)
- [factory/README.md](factory/README.md)
- [abstract_factory/README.md](abstract_factory/README.md)
- [builder/README.md](builder/README.md)
- [prototype/README.md](prototype/README.md)

---

## Further Reading

### Related Design Patterns

- **Structural Patterns:** Facade, Bridge, Adapter (often work with creational patterns)
- **Behavioral Patterns:** Strategy, State, Command (often used with created objects)
- **Architectural Patterns:** Repository, Dependency Injection, Service Locator

### Best Practice Resources

1. "Design Patterns: Elements of Reusable Object-Oriented Software" - Gang of Four
2. "Head First Design Patterns"
3. Python Documentation: [abc module](https://docs.python.org/3/library/abc.html), [copy module](https://docs.python.org/3/library/copy.html)

---

## Summary

Creational patterns provide powerful ways to manage object creation in your Python applications. By abstracting the instantiation process:

- **Decoupling:** Classes and clients aren't tightly bound to each other
- **Flexibility:** Easy to introduce new types without changing existing code
- **Maintainability:** Object creation logic is centralized and manageable
- **Scalability:** Systems can grow without increasing complexity
- **Testability:** Objects can be replaced with mocks for testing

Use the decision tree and best practices in this guide to select and implement the right pattern for your specific scenario. Remember: patterns are tools, not goals. Use them when they solve real problems, not just for the sake of using patterns.
