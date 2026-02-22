# Adapter Pattern (Structural)

> **Architectural Level:** Object Structure  
> **Pythonic Strategy:** Duck Typing and Composition  
> **Production Status:** Widely Used | Framework Standard | Best Practice

---

## Also Known As

- Wrapper

---

## Intent

Convert the interface of a class into another interface that clients expect. The Adapter pattern allows classes with incompatible interfaces to work together by introducing an intermediate adapter that translates between them.

This is a structural design pattern focused on interoperability and reuse without modifying existing source code.

---

## Problem

In many real-world systems, you must interact with components that expose incompatible interfaces. Direct integration leads to tight coupling, fragile code, or duplication.

### Common Scenarios

- **Legacy System Integration**  
  Existing legacy systems expose outdated APIs incompatible with modern code.

- **Third-Party Library Integration**  
  External libraries provide useful functionality but use interfaces that differ from your application's expectations.

- **Multiple Vendors or Providers**  
  Different vendors implement similar functionality using different APIs, such as payment gateways or cloud providers.

- **Interface Evolution**  
  Dependencies change their interface over time, breaking existing integrations.

### Example: Multiple Payment Providers

Each provider exposes a different interface:

```python
# Stripe API
stripe.charge_card(amount_cents=10000, card_token="tok_123")

# PayPal API
paypal.create_payment(total="100.00", currency="USD")

# Square API
square.charge(amount_money=100, source_id="nonce_123")
````

Your application should interact with all providers using a unified interface.

---

## Solution

The Adapter pattern introduces an adapter class that translates between interfaces.

The adapter:

1. Implements the interface expected by the client (Target)
2. Wraps the incompatible class (Adaptee)
3. Translates method calls, parameters, and return values

This allows the client to remain independent of the adaptee implementation.

---

## Structure

### Participants

| Component   | Description                                            |
| ----------- | ------------------------------------------------------ |
| **Target**  | Interface expected by the client                       |
| **Adapter** | Converts the Target interface to the Adaptee interface |
| **Adaptee** | Existing class with incompatible interface             |
| **Client**  | Uses objects through the Target interface              |

### Structural Diagram

```
Client
  |
  v
Target Interface
  ^
  |
Adapter
  |
  v
Adaptee
```

---

## Implementation Variants

### Object Adapter (Composition) — Recommended

Uses composition to wrap the adaptee.

**Advantages**

* Flexible
* Works with subclasses
* Idiomatic in Python

**Disadvantages**

* Requires an additional object

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float):
        pass


class StripeAdapter(PaymentProcessor):

    def __init__(self, stripe_gateway):
        self.stripe = stripe_gateway

    def process_payment(self, amount: float):
        return self.stripe.charge_card(int(amount * 100))
```

---

### Class Adapter (Inheritance)

Uses inheritance to adapt behavior.

**Advantages**

* Fewer objects

**Disadvantages**

* Less flexible
* Tight coupling
* Multiple inheritance complexity
* Less idiomatic in Python

```python
class StripeAdapter(PaymentProcessor, StripeGateway):

    def process_payment(self, amount: float):
        return self.charge_card(int(amount * 100))
```

---

### Default Adapter

Provides default implementations for selective overriding.

```python
class DefaultPaymentProcessor(PaymentProcessor):

    def process_payment(self, amount: float):
        return {"status": "success"}

    def refund(self, transaction_id: str):
        return {"status": "refunded"}


class CustomAdapter(DefaultPaymentProcessor):

    def __init__(self, gateway):
        self.gateway = gateway
```

---

## Implementation Guidelines

### When to Use

Use the Adapter pattern when:

* Integrating legacy systems
* Integrating third-party libraries
* Supporting multiple providers with different interfaces
* Creating a unified abstraction layer
* Preserving existing code without modification

### When to Avoid

Avoid using the Adapter pattern when:

* The original code can be modified directly
* The adaptee is simple and used only once
* The abstraction adds unnecessary complexity

---

## Implementation Steps

```python
from abc import ABC, abstractmethod

# Target interface
class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        pass


# Adaptee
class LegacyPaymentGateway:

    def charge(self, cents: int):
        return {"success": True}


# Adapter
class LegacyAdapter(PaymentProcessor):

    def __init__(self, legacy_gateway: LegacyPaymentGateway):
        self.gateway = legacy_gateway

    def process_payment(self, amount: float) -> dict:
        return self.gateway.charge(int(amount * 100))


# Client usage
processor: PaymentProcessor = LegacyAdapter(LegacyPaymentGateway())
result = processor.process_payment(99.99)
```

---

## Advantages and Disadvantages

### Advantages

* Decouples client from implementation details
* Enables reuse of existing code
* Improves flexibility and extensibility
* Supports the Open/Closed Principle
* Supports the Single Responsibility Principle

### Disadvantages

* Adds abstraction layers
* Introduces additional objects
* Slight performance overhead
* May increase system complexity

---

## Real-World Applications

### Payment Gateways

```python
class PayPalAdapter(PaymentProcessor):

    def __init__(self, paypal_api):
        self.api = paypal_api

    def process_payment(self, amount: float):
        return self.api.create_payment(total=str(amount))
```

---

### Database Drivers

```python
class DatabaseConnection(ABC):

    @abstractmethod
    def execute_query(self, query: str):
        pass


class MySQLAdapter(DatabaseConnection):

    def __init__(self, driver):
        self.driver = driver

    def execute_query(self, query: str):
        return self.driver.query(query)
```

---

### Cloud Storage Providers

```python
class CloudStorage(ABC):

    @abstractmethod
    def upload_file(self, key: str, data: bytes):
        pass


class S3Adapter(CloudStorage):

    def __init__(self, client):
        self.client = client

    def upload_file(self, key: str, data: bytes):
        return self.client.put_object(Key=key, Body=data)
```

---

## Comparison with Related Patterns

| Pattern   | Purpose                                 | Difference                |
| --------- | --------------------------------------- | ------------------------- |
| Bridge    | Separate abstraction and implementation | Designed upfront          |
| Decorator | Add behavior dynamically                | Focuses on behavior       |
| Proxy     | Control access                          | Focuses on access         |
| Facade    | Simplify subsystem                      | Focuses on simplification |

---

## Common Pitfalls

### Unnecessary Adapters

Adapters should only be used when interfaces are incompatible.

### Mixing Responsibilities

Adapters should perform translation only, not business logic.

### Information Loss

Ensure data integrity during translation.

---

## Best Practices

### Recommended

* Prefer composition over inheritance
* Keep adapters focused and minimal
* Clearly document purpose and mapping
* Preserve semantic behavior
* Validate adapted data

### Avoid

* Embedding business logic in adapters
* Modifying adaptee behavior
* Hiding adaptation errors
* Introducing unnecessary abstraction

---

## Standard Library Examples

Python frequently uses adapter-like behavior:

```python
from io import StringIO

file_like = StringIO("example")
```

StringIO adapts strings to behave like file objects.

---

## Summary

The Adapter pattern enables interoperability between incompatible interfaces without modifying existing code.

It is especially useful for:

* Legacy integration
* Third-party library integration
* Multi-provider support
* Interface abstraction

**Key Principle:**
Encapsulate interface translation in a dedicated adapter to maintain clean, flexible, and maintainable system architecture.

