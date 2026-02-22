# Proxy Pattern (Structural)

> **Architectural Level:** Object Access Control  
> **Pythonic Strategy:** Lazy Initialization & Delegation  
> **Production Status:** Critical for Remote Access | Caching | Security

---

## Intent

The Proxy pattern provides a surrogate or placeholder for another object to control access to it. It allows you to manage object creation, access control, caching, logging, or remote access transparently.

---

## Problem

Working with objects that are costly, remote, or require controlled access can cause:

- High cost for creating expensive resources  
- Complexity when accessing objects on remote machines  
- Need for fine-grained access control  
- Desire to cache results of expensive operations  

---

## Solution

Create a proxy object that implements the same interface as the real object and controls access to it.

### Example

```python
class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load_image()

    def load_image(self):
        # Simulate expensive image loading
        print(f"Loading {self.filename}")

    def display(self):
        return f"Displaying {self.filename}"

class ImageProxy:
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None  # Lazy initialization

    def display(self):
        if not self._real_image:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()

# Usage
image = ImageProxy("photo.png")
print(image.display())  # Loads and displays
print(image.display())  # Uses cached object
````

---

## Key Components

| Component   | Role                                                                     |
| ----------- | ------------------------------------------------------------------------ |
| Subject     | Defines a common interface for RealSubject and Proxy                     |
| RealSubject | The actual object implementing the behavior                              |
| Proxy       | Controls access, adds lazy initialization, caching, logging, or security |

---

## Proxy Types

1. **Virtual Proxy:** Delays creation of expensive objects until needed
2. **Protection Proxy:** Controls access based on permissions
3. **Logging Proxy:** Tracks method calls or usage
4. **Caching Proxy:** Stores results to avoid repeated expensive computations
5. **Remote Proxy:** Provides access to objects located on remote systems

---

## Advantages

* Enables lazy object creation
* Controls and restricts access to objects
* Supports caching for performance improvement
* Allows logging or monitoring of object usage

---

## When to Use

* When creating or loading objects is expensive
* When accessing remote services or resources
* When security or permissions need to be enforced
* When caching results improves performance

---

## Summary

The **Proxy pattern** is useful to:

* Control access to objects
* Defer costly operations until necessary
* Add logging, monitoring, or auditing transparently
* Implement caching and improve performance

**Key Principle:** The proxy implements the same interface as the real object, allowing clients to use it interchangeably while managing creation, access, or additional behavior.

