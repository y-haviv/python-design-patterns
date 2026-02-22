"""
Real-World Example: Document Processing with Multiple Export Formats.

Demonstrates how different document elements can be processed by different
visitors to generate different output formats (PDF, HTML, statistics).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime


class DocumentElement(ABC):
    """Abstract base for document elements."""

    @abstractmethod
    def accept(self, visitor: DocumentVisitor) -> Any:
        """Accept a visitor to process this element."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Get the type of this element."""
        pass


class Paragraph(DocumentElement):
    """Represents a paragraph element in a document."""

    def __init__(self, text: str) -> None:
        """
        Initialize a paragraph.
        
        Args:
            text: The paragraph text.
        """
        self.text = text

    def accept(self, visitor: DocumentVisitor) -> Any:
        """Accept a visitor."""
        return visitor.visit_paragraph(self)

    def get_type(self) -> str:
        """Get element type."""
        return "Paragraph"

    def get_word_count(self) -> int:
        """Get word count in paragraph."""
        return len(self.text.split())

    def get_character_count(self) -> int:
        """Get character count in paragraph."""
        return len(self.text)


class Image(DocumentElement):
    """Represents an image element in a document."""

    def __init__(self, filename: str, width: int, height: int, alt_text: str) -> None:
        """
        Initialize an image.
        
        Args:
            filename: Image file name.
            width: Image width in pixels.
            height: Image height in pixels.
            alt_text: Alternative text for accessibility.
        """
        self.filename = filename
        self.width = width
        self.height = height
        self.alt_text = alt_text

    def accept(self, visitor: DocumentVisitor) -> Any:
        """Accept a visitor."""
        return visitor.visit_image(self)

    def get_type(self) -> str:
        """Get element type."""
        return "Image"

    def get_size_kb(self) -> float:
        """Get estimated image size in KB."""
        # Rough estimate: 2 bytes per pixel
        return (self.width * self.height * 2) / 1024


class Table(DocumentElement):
    """Represents a table element in a document."""

    def __init__(
        self, headers: List[str], rows: List[List[str]]
    ) -> None:
        """
        Initialize a table.
        
        Args:
            headers: Column headers.
            rows: Table rows as list of lists.
        """
        self.headers = headers
        self.rows = rows

    def accept(self, visitor: DocumentVisitor) -> Any:
        """Accept a visitor."""
        return visitor.visit_table(self)

    def get_type(self) -> str:
        """Get element type."""
        return "Table"

    def get_cell_count(self) -> int:
        """Get total number of cells."""
        return len(self.headers) + (len(self.headers) * len(self.rows))

    def get_data_as_tuples(self) -> List[Tuple[str, ...]]:
        """Get table data as tuples."""
        result = [tuple(self.headers)]
        for row in self.rows:
            result.append(tuple(row))
        return result


class DocumentVisitor(ABC):
    """Abstract visitor for document elements."""

    @abstractmethod
    def visit_paragraph(self, element: Paragraph) -> Any:
        """Visit a paragraph element."""
        pass

    @abstractmethod
    def visit_image(self, element: Image) -> Any:
        """Visit an image element."""
        pass

    @abstractmethod
    def visit_table(self, element: Table) -> Any:
        """Visit a table element."""
        pass

    @abstractmethod
    def get_result(self) -> Any:
        """Get the final result of the visitor."""
        pass

    @abstractmethod
    def get_visitor_name(self) -> str:
        """Get visitor name."""
        pass


class PDFExportVisitor(DocumentVisitor):
    """Visitor that exports document elements to PDF format."""

    def __init__(self) -> None:
        """Initialize PDF export visitor."""
        self.output: List[str] = []
        self.page_number = 1
        self.element_count = 0

    def visit_paragraph(self, element: Paragraph) -> Any:
        """Export paragraph to PDF."""
        self.element_count += 1
        pdf_line = f"[PDF Page {self.page_number}] TEXT: {element.text[:50]}..."
        self.output.append(pdf_line)
        print(f"  ✓ PDF: Exported paragraph ({element.get_word_count()} words)")
        return pdf_line

    def visit_image(self, element: Image) -> Any:
        """Export image to PDF."""
        self.element_count += 1
        pdf_line = (
            f"[PDF Page {self.page_number}] IMAGE: {element.filename} "
            f"({element.width}x{element.height}px)"
        )
        self.output.append(pdf_line)
        print(f"  ✓ PDF: Embedded image {element.filename}")
        return pdf_line

    def visit_table(self, element: Table) -> Any:
        """Export table to PDF."""
        self.element_count += 1
        pdf_line = (
            f"[PDF Page {self.page_number}] TABLE: {len(element.headers)} cols, "
            f"{len(element.rows)} rows"
        )
        self.output.append(pdf_line)
        print(f"  ✓ PDF: Formatted table ({element.get_cell_count()} cells)")
        return pdf_line

    def get_result(self) -> str:
        """Get PDF output."""
        return "\n".join(self.output)

    def get_visitor_name(self) -> str:
        """Get visitor name."""
        return "PDF Export Visitor"


class HTMLExportVisitor(DocumentVisitor):
    """Visitor that exports document elements to HTML format."""

    def __init__(self) -> None:
        """Initialize HTML export visitor."""
        self.output: List[str] = []
        self.element_count = 0

    def visit_paragraph(self, element: Paragraph) -> Any:
        """Export paragraph to HTML."""
        self.element_count += 1
        html_line = f"<p>{element.text}</p>"
        self.output.append(html_line)
        print(f"  ✓ HTML: Generated <p> tag")
        return html_line

    def visit_image(self, element: Image) -> Any:
        """Export image to HTML."""
        self.element_count += 1
        html_line = (
            f'<img src="{element.filename}" alt="{element.alt_text}" '
            f'width="{element.width}" height="{element.height}" />'
        )
        self.output.append(html_line)
        print(f"  ✓ HTML: Generated <img> tag")
        return html_line

    def visit_table(self, element: Table) -> Any:
        """Export table to HTML."""
        self.element_count += 1
        table_html = "<table>\n  <tr>"
        for header in element.headers:
            table_html += f"<th>{header}</th>"
        table_html += "</tr>\n"
        
        for row in element.rows:
            table_html += "  <tr>"
            for cell in row:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>\n"
        
        table_html += "</table>"
        self.output.append(table_html)
        print(f"  ✓ HTML: Generated <table>")
        return table_html

    def get_result(self) -> str:
        """Get HTML output."""
        return "\n".join(self.output)

    def get_visitor_name(self) -> str:
        """Get visitor name."""
        return "HTML Export Visitor"


class TextAnalysisVisitor(DocumentVisitor):
    """Visitor that analyzes document elements."""

    def __init__(self) -> None:
        """Initialize text analysis visitor."""
        self.statistics: Dict[str, Any] = {
            "paragraph_count": 0,
            "total_words": 0,
            "total_characters": 0,
            "image_count": 0,
            "total_image_size_kb": 0.0,
            "table_count": 0,
            "total_cells": 0,
        }
        self.element_count = 0
        self.analysis_log: List[Dict[str, Any]] = []

    def visit_paragraph(self, element: Paragraph) -> Any:
        """Analyze paragraph."""
        self.element_count += 1
        word_count = element.get_word_count()
        char_count = element.get_character_count()
        
        self.statistics["paragraph_count"] += 1
        self.statistics["total_words"] += word_count
        self.statistics["total_characters"] += char_count
        
        analysis = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "Paragraph",
            "words": word_count,
            "characters": char_count,
        }
        self.analysis_log.append(analysis)
        
        print(f"  ✓ Analysis: Paragraph ({word_count} words, {char_count} chars)")
        return analysis

    def visit_image(self, element: Image) -> Any:
        """Analyze image."""
        self.element_count += 1
        size_kb = element.get_size_kb()
        
        self.statistics["image_count"] += 1
        self.statistics["total_image_size_kb"] += size_kb
        
        analysis = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "Image",
            "filename": element.filename,
            "dimensions": f"{element.width}x{element.height}",
            "estimated_size_kb": round(size_kb, 2),
        }
        self.analysis_log.append(analysis)
        
        print(f"  ✓ Analysis: Image ({element.width}x{element.height}, ~{size_kb:.2f}KB)")
        return analysis

    def visit_table(self, element: Table) -> Any:
        """Analyze table."""
        self.element_count += 1
        cell_count = element.get_cell_count()
        
        self.statistics["table_count"] += 1
        self.statistics["total_cells"] += cell_count
        
        analysis = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "element_type": "Table",
            "columns": len(element.headers),
            "rows": len(element.rows),
            "total_cells": cell_count,
        }
        self.analysis_log.append(analysis)
        
        print(f"  ✓ Analysis: Table ({len(element.headers)}x{len(element.rows)}, {cell_count} cells)")
        return analysis

    def get_result(self) -> Dict[str, Any]:
        """Get analysis statistics."""
        return self.statistics.copy()

    def get_visitor_name(self) -> str:
        """Get visitor name."""
        return "Text Analysis Visitor"

    def display_statistics(self) -> None:
        """Display analysis statistics."""
        print("\n=== Document Analysis ===")
        for key, value in self.statistics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")


class Document:
    """
    Represents a document containing multiple elements.
    
    Demonstrates how visitors can operate on complex object structures.
    """

    def __init__(self, title: str) -> None:
        """
        Initialize a document.
        
        Args:
            title: Document title.
        """
        self.title = title
        self.elements: List[DocumentElement] = []

    def add_element(self, element: DocumentElement) -> None:
        """Add element to document."""
        self.elements.append(element)
        print(f"  Added {element.get_type()} to document")

    def accept_visitor(self, visitor: DocumentVisitor) -> Any:
        """Apply a visitor to all elements in the document."""
        print(f"\n[Document] Processing with {visitor.get_visitor_name()}:")
        results = []
        for element in self.elements:
            result = element.accept(visitor)
            results.append(result)
        return results

    def export_pdf(self) -> str:
        """Export document to PDF format."""
        print(f"\n=== Exporting to PDF: {self.title} ===")
        visitor = PDFExportVisitor()
        self.accept_visitor(visitor)
        return visitor.get_result()

    def export_html(self) -> str:
        """Export document to HTML format."""
        print(f"\n=== Exporting to HTML: {self.title} ===")
        visitor = HTMLExportVisitor()
        self.accept_visitor(visitor)
        return visitor.get_result()

    def analyze(self) -> Dict[str, Any]:
        """Analyze document tokens."""
        print(f"\n=== Analyzing Document: {self.title} ===")
        visitor = TextAnalysisVisitor()
        self.accept_visitor(visitor)
        visitor.display_statistics()
        return visitor.get_result()

    def get_element_count(self) -> int:
        """Get number of elements in document."""
        return len(self.elements)

    def display_structure(self) -> None:
        """Display document structure."""
        print(f"\n=== Document Structure: {self.title} ===")
        for i, element in enumerate(self.elements, 1):
            print(f"  {i}. {element.get_type()}")
