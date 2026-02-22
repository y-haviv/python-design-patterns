# Visitor Pattern (Behavioral)

> **Architectural Level:** Object Structure Operations  
> **Pythonic Strategy:** Double Dispatch for Externalized Operations  
> **Production Status:** Complex Operations | Separation of Concerns | Extensively Documented

---

## Also Known As

Visitor

---

## Intent

Represent an operation to be performed on the elements of an object structure without modifying the classes of those elements.

The Visitor pattern allows you to define new operations independently of the object structure by placing the operation logic inside visitor objects rather than inside the element classes themselves.

---

## Problem

Complex object structures often require multiple unrelated operations. Implementing these operations directly inside element classes leads to rigid and difficult-to-maintain designs.

### Common Issues

- **Operation Proliferation:** Each new operation requires modifying every element class.
- **Violation of Open/Closed Principle:** Adding operations requires changing existing code.
- **Scattered Logic:** Related operations are distributed across multiple classes.
- **Tight Coupling:** Elements become coupled to all supported operations.
- **Poor Maintainability:** Changes require coordination across many classes.

### Real-World Scenario (Anti-Pattern)

Document elements implementing export and analysis logic directly:

```python
class Paragraph:

    def __init__(self, text):
        self.text = text

    def to_pdf(self):
        pass

    def to_html(self):
        pass

    def analyze(self):
        pass
````

Adding new operations requires modifying all element classes.

---

## Solution

Move operations into separate visitor classes and allow elements to accept visitors.

```python
class Paragraph:

    def accept(self, visitor):
        return visitor.visit_paragraph(self)


class PDFExportVisitor:

    def visit_paragraph(self, element):
        pass


class HTMLExportVisitor:

    def visit_paragraph(self, element):
        pass
```

New operations are implemented as new visitor classes without modifying element classes.

---

## Structure

```
ObjectStructure
 └── Elements

Element
 └── accept(visitor)

ConcreteElementA
ConcreteElementB
ConcreteElementC

Visitor
 ├── visit_element_a()
 ├── visit_element_b()
 └── visit_element_c()

ConcreteVisitorA
ConcreteVisitorB
ConcreteVisitorC
```

---

## Key Components

### Visitor

Declares visit methods for each element type.

### ConcreteVisitor

Implements operations for specific element types.

### Element

Defines the accept method for visitors.

### ConcreteElement

Implements accept and delegates to the correct visitor method.

### ObjectStructure

Maintains a collection of elements and allows visitors to operate on them.

---

## Benefits

### Open/Closed Principle for Operations

New operations can be added without modifying element classes.

### Separation of Concerns

Element classes focus on structure, while visitors implement behavior.

### Logical Grouping

Related operations are grouped together.

### Improved Maintainability

Changes to operations do not affect element implementation.

### Reusability

Visitors can be reused across multiple object structures.

---

## Trade-offs

### Difficult to Add New Element Types

Adding new elements requires updating all visitor classes.

### Increased Complexity

Introduces additional classes and abstraction.

### Reduced Encapsulation

Visitors may require access to internal element details.

### Double Dispatch Requirement

Correct method resolution depends on both element and visitor types.

### Less Natural in Python

Python often provides simpler alternatives using dynamic typing.

---

## Real-World Example

This implementation demonstrates document processing with multiple operations.

### Elements

* Paragraph
* Image
* Table

### Visitors

* PDFExportVisitor
* HTMLExportVisitor
* TextAnalysisVisitor

### Example

```python
document = Document("Report")

document.add_element(Paragraph("Introduction"))
document.add_element(Image("chart.jpg", 800, 600, "Chart"))
document.add_element(Table(["A", "B"], [["1", "2"]]))

pdf_output = document.export_pdf()

html_output = document.export_html()

analysis = document.analyze()
```

Each operation is implemented without modifying element classes.

---

## When to Use

Use the Visitor pattern when:

* Object structures are stable
* Operations change frequently
* Many unrelated operations must be applied
* You want to avoid polluting element classes
* Operations should be grouped logically

Common use cases:

* Abstract Syntax Tree processing
* Document export systems
* Compilers and interpreters
* Reporting systems
* Graphics rendering systems

---

## When Not to Use

Avoid the Visitor pattern when:

* Element types change frequently
* Only a few operations exist
* Simplicity is preferred over extensibility
* Object structure is small
* Encapsulation must be strictly preserved

---

## Pattern Relationships

### Composite

Visitor often operates on Composite structures.

### Iterator

Iterator may be used to traverse elements.

### Strategy

Strategy encapsulates interchangeable algorithms, while Visitor applies operations across object structures.

### Chain of Responsibility

Chain handles sequential processing, Visitor handles structural operations.

---

## Python-Specific Considerations

### Dynamic Typing Alternatives

Python allows simpler alternatives using functions and dynamic dispatch.

### Function-Based Visitors

Functions can replace visitor classes in simpler cases.

### Flexible Dispatch

Python's dynamic nature reduces the need for formal visitor implementations.

### Practical Usage

Visitor is most useful when strict structure and extensibility are required.

---

## Example Usage

```python
element = ConcreteElementA("data")

visitor = ConcreteVisitorA()

result = element.accept(visitor)


document = Document("Example")

document.add_element(element)

visitor = PDFExportVisitor()

for element in document.elements:
    element.accept(visitor)
```

---

## Implementation Notes

### Accept Method

Elements must implement accept and call the appropriate visitor method.

### Visitor Interface

All visit methods should be defined.

### Result Handling

Visitors may return results or maintain internal state.

### Traversal Responsibility

Traversal logic is typically managed by the object structure.

### Consistency

Ensure naming conventions remain consistent across visitors and elements.

---

## Related Patterns

* Composite
* Iterator
* Strategy
* Template Method

---

## Comparison: Visitor vs Alternatives

| Approach            | Advantages                 | Disadvantages             | Best Use Case                         |
| ------------------- | -------------------------- | ------------------------- | ------------------------------------- |
| Visitor             | Easy to add operations     | Hard to add elements      | Stable structure, evolving operations |
| Methods on Elements | Simple design              | Hard to extend operations | Few operations                        |
| Functions           | Flexible and Pythonic      | Less structured           | Simple and dynamic systems            |
| Strategy            | Easy algorithm replacement | No structural traversal   | Algorithm selection                   |

---

## Common Mistakes

### Missing Visit Methods

Visitor classes must implement all required methods.

### Breaking Encapsulation

Avoid exposing unnecessary internal details.

### Excessive Visitor Creation

Reuse visitor instances when possible.

### Mixing Responsibilities

Keep traversal logic separate from visitor logic.

### Using Visitor Unnecessarily

Do not use Visitor when simpler alternatives are sufficient.

---

## Python vs Traditional Implementation

The Visitor pattern is more common in statically typed languages.

Python often uses alternative approaches:

```python
def export_pdf(element):

    if isinstance(element, Paragraph):
        pass

    elif isinstance(element, Image):
        pass


def accept(element, visitor_function):

    return visitor_function(element)
```

Use the formal Visitor pattern when architectural clarity and extensibility are primary goals.

---

## Summary

The Visitor pattern externalizes operations performed on object structures into separate visitor classes.

This improves extensibility, maintainability, and organization when working with stable object structures and evolving operations.

It is most valuable in systems where operations frequently change but element structures remain stable.

