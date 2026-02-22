"""
Visitor Pattern (Behavioral)

Represent an operation to be performed on the elements of an object structure.
Visitor lets you define a new operation without changing the classes of the
elements on which it operates.
"""

from .pattern import (
    Visitor,
    Element,
    ConcreteElementA,
    ConcreteElementB,
    ConcreteVisitorA,
    ConcreteVisitorB,
)
from .real_world_example import (
    DocumentElement,
    Paragraph,
    Image,
    Table,
    PDFExportVisitor,
    HTMLExportVisitor,
    TextAnalysisVisitor,
    Document,
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
