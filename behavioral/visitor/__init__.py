"""
Visitor Pattern (Behavioral)

Represent an operation to be performed on the elements of an object structure.
Visitor lets you define a new operation without changing the classes of the
elements on which it operates.
"""

from .pattern import (
    ConcreteElementA,
    ConcreteElementB,
    ConcreteVisitorA,
    ConcreteVisitorB,
    Element,
    Visitor,
)
from .real_world_example import (
    Document,
    DocumentElement,
    HTMLExportVisitor,
    Image,
    Paragraph,
    PDFExportVisitor,
    Table,
    TextAnalysisVisitor,
)

__all__ = [
    "Visitor",
    "Element",
    "ConcreteElementA",
    "ConcreteElementB",
    "ConcreteVisitorA",
    "ConcreteVisitorB",
    "DocumentElement",
    "Paragraph",
    "Image",
    "Table",
    "PDFExportVisitor",
    "HTMLExportVisitor",
    "TextAnalysisVisitor",
    "Document",
]
