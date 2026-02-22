"""
Comprehensive tests for the Visitor Pattern.

These tests verify:
1. Visitor pattern with simple elements.
2. Multiple visitors providing different operations.
3. Double dispatch mechanism.
4. Real-world document processing.
5. Visitor composition and chaining.
"""

from __future__ import annotations
import pytest
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


class TestConcreteElements:
    """Tests for concrete element implementations."""

    def test_element_a_creation(self) -> None:
        """Verify creating element A."""
        element = ConcreteElementA("elem_a", "test value")
        
        assert element.get_name() == "elem_a"
        assert element.value == "test value"
        assert element.get_type() == "Element A"

    def test_element_b_creation(self) -> None:
        """Verify creating element B."""
        element = ConcreteElementB("elem_b", 42)
        
        assert element.get_name() == "elem_b"
        assert element.count == 42

    def test_element_a_operation(self) -> None:
        """Verify element A operation."""
        element = ConcreteElementA("test", "hello")
        
        result = element.operation_a()
        
        assert "Operation A" in result
        assert "hello" in result

    def test_element_b_operation(self) -> None:
        """Verify element B operation."""
        element = ConcreteElementB("test", 10)
        
        result = element.operation_b()
        
        assert "Operation B" in result
        assert "10" in result


class TestVisitorPattern:
    """Tests for visitor pattern implementation."""

    def test_visitor_a_visits_element_a(self) -> None:
        """Verify visitor A can visit element A."""
        element = ConcreteElementA("test", "value")
        visitor = ConcreteVisitorA()
        
        result = element.accept(visitor)
        
        assert result is not None
        assert "Operation A" in result

    def test_visitor_a_visits_element_b(self) -> None:
        """Verify visitor A can visit element B."""
        element = ConcreteElementB("test", 5)
        visitor = ConcreteVisitorA()
        
        result = element.accept(visitor)
        
        assert result is not None
        assert "Operation B" in result

    def test_visitor_b_visits_element_a(self) -> None:
        """Verify visitor B can visit element A."""
        element = ConcreteElementA("test", "hello world")
        visitor = ConcreteVisitorB()
        
        result = element.accept(visitor)
        
        assert result is not None
        assert "11" in result  # Length of "hello world"

    def test_visitor_b_visits_element_b(self) -> None:
        """Verify visitor B can visit element B."""
        element = ConcreteElementB("test", 5)
        visitor = ConcreteVisitorB()
        
        result = element.accept(visitor)
        
        assert result is not None
        assert "10" in result  # 5 * 2

    def test_different_visitors_different_results(self) -> None:
        """Verify different visitors produce different results."""
        element_a = ConcreteElementA("test", "hello")
        visitor_a = ConcreteVisitorA()
        visitor_b = ConcreteVisitorB()
        
        result_a = element_a.accept(visitor_a)
        result_b = element_a.accept(visitor_b)
        
        assert result_a != result_b

    def test_visitor_collects_results(self) -> None:
        """Verify visitor can collect multiple results."""
        visitor = ConcreteVisitorA()
        elem1 = ConcreteElementA("a", "first")
        elem2 = ConcreteElementB("b", 10)
        
        elem1.accept(visitor)
        elem2.accept(visitor)
        
        results = visitor.get_results()
        assert len(results) == 2

    def test_visitor_visit_count(self) -> None:
        """Verify visitor tracks visit count."""
        visitor = ConcreteVisitorA()
        elements = [
            ConcreteElementA("a", "test"),
            ConcreteElementB("b", 5),
            ConcreteElementA("c", "more"),
        ]
        
        for element in elements:
            element.accept(visitor)
        
        assert visitor.get_visit_count() == 3

    def test_visitor_b_statistics(self) -> None:
        """Verify visitor B collects statistics."""
        visitor = ConcreteVisitorB()
        elem_a = ConcreteElementA("a", "test")
        elem_b = ConcreteElementB("b", 5)
        
        elem_a.accept(visitor)
        elem_b.accept(visitor)
        
        stats = visitor.get_statistics()
        assert stats["element_a_count"] == 1
        assert stats["element_b_count"] == 1


class TestDocumentElements:
    """Tests for document element implementations."""

    def test_paragraph_creation(self) -> None:
        """Verify creating a paragraph."""
        para = Paragraph("This is a test paragraph.")
        
        assert para.get_type() == "Paragraph"
        assert len(para.text) > 0

    def test_paragraph_word_count(self) -> None:
        """Verify paragraph word count."""
        para = Paragraph("This is a test paragraph")
        
        assert para.get_word_count() == 5

    def test_paragraph_character_count(self) -> None:
        """Verify paragraph character count."""
        para = Paragraph("hello")
        
        assert para.get_character_count() == 5

    def test_image_creation(self) -> None:
        """Verify creating an image."""
        img = Image("test.jpg", 800, 600, "Test image")
        
        assert img.get_type() == "Image"
        assert img.filename == "test.jpg"
        assert img.width == 800
        assert img.height == 600

    def test_image_size_calculation(self) -> None:
        """Verify image size calculation."""
        img = Image("test.jpg", 1000, 1000, "Test")
        
        size_kb = img.get_size_kb()
        assert size_kb > 0

    def test_table_creation(self) -> None:
        """Verify creating a table."""
        headers = ["Name", "Age", "City"]
        rows = [["Alice", "30", "NYC"], ["Bob", "25", "LA"]]
        table = Table(headers, rows)
        
        assert table.get_type() == "Table"
        assert len(table.headers) == 3
        assert len(table.rows) == 2

    def test_table_cell_count(self) -> None:
        """Verify table cell count."""
        headers = ["A", "B", "C"]
        rows = [["a", "b", "c"], ["d", "e", "f"]]
        table = Table(headers, rows)
        
        # Headers + 2 rows of 3 columns each
        assert table.get_cell_count() == 3 + 6

    def test_table_as_tuples(self) -> None:
        """Verify getting table as tuples."""
        headers = ["Name", "Age"]
        rows = [["Alice", "30"]]
        table = Table(headers, rows)
        
        tuples = table.get_data_as_tuples()
        assert len(tuples) == 2
        assert tuples[0] == ("Name", "Age")


class TestDocumentVisitors:
    """Tests for document visitor implementations."""

    def test_pdf_export_visitor(self) -> None:
        """Verify PDF export visitor."""
        para = Paragraph("Test paragraph")
        visitor = PDFExportVisitor()
        
        result = para.accept(visitor)
        
        assert "[PDF" in result

    def test_html_export_visitor(self) -> None:
        """Verify HTML export visitor."""
        para = Paragraph("Test paragraph")
        visitor = HTMLExportVisitor()
        
        result = para.accept(visitor)
        
        assert "<p>" in result
        assert "</p>" in result

    def test_text_analysis_visitor(self) -> None:
        """Verify text analysis visitor."""
        para = Paragraph("hello world test")
        visitor = TextAnalysisVisitor()
        
        result = para.accept(visitor)
        
        assert result["element_type"] == "Paragraph"
        assert result["words"] == 3

    def test_pdf_export_image(self) -> None:
        """Verify PDF export with image."""
        img = Image("test.jpg", 800, 600, "Test")
        visitor = PDFExportVisitor()
        
        result = img.accept(visitor)
        
        assert "[PDF" in result
        assert "test.jpg" in result

    def test_html_export_image(self) -> None:
        """Verify HTML export with image."""
        img = Image("test.jpg", 800, 600, "Test alt")
        visitor = HTMLExportVisitor()
        
        result = img.accept(visitor)
        
        assert "<img" in result
        assert "test.jpg" in result
        assert "Test alt" in result

    def test_html_export_table(self) -> None:
        """Verify HTML export with table."""
        table = Table(["Name", "Age"], [["Alice", "30"]])
        visitor = HTMLExportVisitor()
        
        result = table.accept(visitor)
        
        assert "<table>" in result
        assert "<th>" in result
        assert "<td>" in result


class TestDocument:
    """Tests for document processing."""

    def test_document_creation(self) -> None:
        """Verify creating a document."""
        doc = Document("Test Document")
        
        assert doc.title == "Test Document"
        assert doc.get_element_count() == 0

    def test_add_elements(self) -> None:
        """Verify adding elements to document."""
        doc = Document("Test")
        
        doc.add_element(Paragraph("Text"))
        doc.add_element(Image("img.jpg", 100, 100, "Desc"))
        
        assert doc.get_element_count() == 2

    def test_document_pdf_export(self) -> None:
        """Verify exporting document to PDF."""
        doc = Document("Test")
        doc.add_element(Paragraph("Hello world"))
        doc.add_element(Image("test.jpg", 800, 600, "Test"))
        
        pdf_output = doc.export_pdf()
        
        assert "[PDF" in pdf_output
        assert "TEXT" in pdf_output
        assert "IMAGE" in pdf_output

    def test_document_html_export(self) -> None:
        """Verify exporting document to HTML."""
        doc = Document("Test")
        doc.add_element(Paragraph("Hello world"))
        doc.add_element(Image("test.jpg", 800, 600, "Test"))
        
        html_output = doc.export_html()
        
        assert "<p>" in html_output
        assert "<img" in html_output

    def test_document_analysis(self) -> None:
        """Verify analyzing document."""
        doc = Document("Test")
        doc.add_element(Paragraph("Hello world test"))
        doc.add_element(Image("test.jpg", 800, 600, "Test"))
        doc.add_element(Table(["A", "B"], [["1", "2"]]))
        
        stats = doc.analyze()
        
        assert stats["paragraph_count"] == 1
        assert stats["image_count"] == 1
        assert stats["table_count"] == 1
        assert stats["total_words"] > 0

    def test_document_multiple_paragraphs(self) -> None:
        """Verify document with multiple paragraphs."""
        doc = Document("Report")
        doc.add_element(Paragraph("Introduction paragraph"))
        doc.add_element(Paragraph("Body paragraph"))
        doc.add_element(Paragraph("Conclusion paragraph"))
        
        stats = doc.analyze()
        
        assert stats["paragraph_count"] == 3

    def test_complex_document(self) -> None:
        """Verify complex document with mixed content."""
        doc = Document("Complex")
        
        doc.add_element(Paragraph("Introduction"))
        doc.add_element(Image("fig1.jpg", 640, 480, "Figure 1"))
        doc.add_element(Paragraph("Discussion of figure"))
        doc.add_element(Table(["Month", "Sales"], [["Jan", "100"], ["Feb", "150"]]))
        doc.add_element(Paragraph("Conclusion"))
        
        assert doc.get_element_count() == 5
        
        stats = doc.analyze()
        assert stats["paragraph_count"] == 3
        assert stats["image_count"] == 1
        assert stats["table_count"] == 1

    def test_visitor_composition(self) -> None:
        """Verify applying multiple visitors."""
        doc = Document("Test")
        doc.add_element(Paragraph("Test content"))
        
        pdf = doc.export_pdf()
        html = doc.export_html()
        analysis = doc.analyze()
        
        assert len(pdf) > 0
        assert len(html) > 0
        assert analysis["paragraph_count"] == 1

    def test_empty_document_export(self) -> None:
        """Verify exporting empty document."""
        doc = Document("Empty")
        
        pdf = doc.export_pdf()
        html = doc.export_html()
        analysis = doc.analyze()
        
        assert isinstance(pdf, str)
        assert isinstance(html, str)
        assert analysis["paragraph_count"] == 0
