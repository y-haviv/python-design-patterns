"""
Comprehensive tests for the Composite Pattern.

These tests verify:
1. Basic composite structure with leaves and composites.
2. Tree operations (add, remove, traverse).
3. File system simulation.
4. Organization structure.
5. Menu structure.
6. Real-world document structure.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Component,
    Leaf,
    Composite,
    File,
    Directory,
    Employee,
    Department,
    MenuItem,
    Menu,
)
from .real_world_example import (
    TextElement,
    Paragraph,
    Heading,
    BulletList,
    Section,
    Document,
    DocumentBuilder,
)


class TestBasicComposite:
    """Tests for basic composite pattern."""

    def test_leaf_operation(self) -> None:
        """Verify leaf operation."""
        leaf = Leaf("A")
        assert "Leaf(A)" in leaf.operation()

    def test_single_composite(self) -> None:
        """Verify composite with leaves."""
        composite = Composite("composite")
        composite.add(Leaf("A"))
        composite.add(Leaf("B"))

        result = composite.operation()
        assert "Composite(composite)" in result
        assert "Leaf(A)" in result
        assert "Leaf(B)" in result

    def test_nested_composite(self) -> None:
        """Verify nested composite structure."""
        root = Composite("root")
        branch1 = Composite("branch1")
        branch2 = Composite("branch2")

        branch1.add(Leaf("A"))
        branch1.add(Leaf("B"))
        branch2.add(Leaf("C"))

        root.add(branch1)
        root.add(branch2)

        result = root.operation()
        assert "Composite(root)" in result
        assert "Composite(branch1)" in result
        assert "Composite(branch2)" in result

    def test_add_remove_components(self) -> None:
        """Verify adding and removing components."""
        parent = Composite("parent")
        leaf_a = Leaf("A")
        leaf_b = Leaf("B")

        parent.add(leaf_a)
        parent.add(leaf_b)

        assert len(parent.children) == 2

        parent.remove(leaf_a)
        assert len(parent.children) == 1

    def test_get_child(self) -> None:
        """Verify getting child by index."""
        composite = Composite("parent")
        leaf = Leaf("A")

        composite.add(leaf)
        retrieved = composite.get_child(0)

        assert retrieved is leaf
        assert composite.get_child(5) is None


class TestFileSystem:
    """Tests for file system composite."""

    def test_single_file(self) -> None:
        """Verify single file."""
        file = File("document.txt", 1024)

        assert file.get_size() == 1024
        assert "document.txt" in file.display()

    def test_directory_with_files(self) -> None:
        """Verify directory with files."""
        dir_root = Directory("documents")
        dir_root.add(File("file1.txt", 100))
        dir_root.add(File("file2.txt", 200))

        assert dir_root.get_size() == 300

    def test_nested_directories(self) -> None:
        """Verify nested directory structure."""
        root = Directory("root")
        photos = Directory("photos")
        videos = Directory("videos")

        photos.add(File("image1.jpg", 2048))
        photos.add(File("image2.jpg", 1024))

        videos.add(File("movie1.mp4", 1024 * 1024))

        root.add(photos)
        root.add(videos)

        total_size = root.get_size()
        assert total_size == 3072 + (1024 * 1024)

    def test_directory_display(self) -> None:
        """Verify directory display structure."""
        root = Directory("root")
        docs = Directory("documents")
        docs.add(File("readme.txt", 512))

        root.add(docs)

        display = root.display()
        assert "📁 root/" in display
        assert "📁 documents/" in display
        assert "📄 readme.txt" in display

    def test_deep_nesting(self) -> None:
        """Verify deeply nested structure."""
        root = Directory("root")
        level1 = Directory("level1")
        level2 = Directory("level2")
        level3 = Directory("level3")

        level3.add(File("deep_file.txt", 256))
        level2.add(level3)
        level1.add(level2)
        root.add(level1)

        assert root.get_size() == 256


class TestOrganization:
    """Tests for organization structure."""

    def test_single_employee(self) -> None:
        """Verify single employee."""
        emp = Employee("Alice", "Developer", 100000)

        assert emp.get_head_count() == 1
        assert emp.get_budget() == 100000
        assert emp.get_name() == "Alice"

    def test_department_with_employees(self) -> None:
        """Verify department with employees."""
        dept = Department("Engineering", "Bob")
        dept.add_member(Employee("Alice", "Developer", 100000))
        dept.add_member(Employee("Charlie", "Senior Dev", 120000))

        assert dept.get_head_count() == 2
        assert dept.get_budget() == 220000

    def test_nested_departments(self) -> None:
        """Verify nested department structure."""
        company = Department("Company", "CEO")

        eng = Department("Engineering", "VP Eng")
        eng.add_member(Employee("Alice", "Developer", 100000))
        eng.add_member(Employee("Bob", "Developer", 100000))

        sales = Department("Sales", "VP Sales")
        sales.add_member(Employee("Charlie", "Sales Rep", 80000))

        company.add_member(eng)
        company.add_member(sales)

        assert company.get_head_count() == 4
        assert company.get_budget() == 360000

    def test_mixed_structure(self) -> None:
        """Verify mixed structure with employees and departments."""
        company = Department("Company", "CEO")
        company.add_member(Employee("Executive", "CTO", 150000))

        eng = Department("Engineering", "Manager")
        eng.add_member(Employee("Dev1", "Developer", 100000))

        company.add_member(eng)

        assert company.get_head_count() == 3
        assert company.get_budget() == 350000


class TestMenuComposite:
    """Tests for menu composite structure."""

    def test_simple_menu_item(self) -> None:
        """Verify simple menu item."""
        def action():
            return "Action executed"

        item = MenuItem("Save", action)
        assert "Save" in item.display()
        assert item.execute() == "Action executed"

    def test_menu_with_items(self) -> None:
        """Verify menu with items."""
        def save():
            return "Saving"

        def close():
            return "Closing"

        menu = Menu("File")
        menu.add(MenuItem("Save", save))
        menu.add(MenuItem("Close", close))

        assert "File" in menu.display()
        assert "Save" in menu.display()

    def test_nested_menus(self) -> None:
        """Verify nested menu structure."""
        def print_doc():
            return "Printing"

        def print_preview():
            return "Previewing"

        file_menu = Menu("File")
        file_menu.add(MenuItem("Save", lambda: "Save"))

        print_menu = Menu("Print")
        print_menu.add(MenuItem("Print", print_doc))
        print_menu.add(MenuItem("Preview", print_preview))

        file_menu.add(print_menu)

        display = file_menu.display()
        assert "File" in display
        assert "Print" in display


class TestDocumentStructure:
    """Tests for document structure."""

    def test_simple_paragraph(self) -> None:
        """Verify simple paragraph."""
        para = Paragraph("This is a paragraph.")
        assert para.get_content() == "This is a paragraph."
        assert para.get_word_count() == 4

    def test_heading(self) -> None:
        """Verify heading."""
        heading = Heading(1, "Main Title")
        assert heading.get_content() == "Main Title"
        assert "<h1>" in heading.export_to_html()
        assert "# Main Title" in heading.export_to_markdown()

    def test_bullet_list(self) -> None:
        """Verify bullet list."""
        list_item = BulletList()
        list_item.add(Paragraph("Item 1"))
        list_item.add(Paragraph("Item 2"))

        assert "<ul>" in list_item.export_to_html()
        assert "- Item 1" in list_item.export_to_markdown()

    def test_section_with_content(self) -> None:
        """Verify section with content."""
        section = Section("Introduction")
        section.add(Heading(2, "Getting Started"))
        section.add(Paragraph("This is the intro"))

        assert section.get_word_count() == 5

    def test_full_document(self) -> None:
        """Verify full document."""
        doc = Document("My Report", "John Doe")

        intro = Section("Introduction")
        intro.add(Paragraph("This is the introduction"))

        doc.add(intro)

        metadata = doc.get_metadata()
        assert metadata["title"] == "My Report"
        assert metadata["author"] == "John Doe"
        assert metadata["section_count"] == 1

    def test_document_export_html(self) -> None:
        """Verify document HTML export."""
        doc = Document("Test", "Author")
        section = Section("Content")
        section.add(Paragraph("Hello World"))

        doc.add(section)

        html = doc.export_to_html()
        assert "<!DOCTYPE html>" in html
        assert "<h1>Test</h1>" in html
        assert "<p>Hello World</p>" in html

    def test_document_export_markdown(self) -> None:
        """Verify document Markdown export."""
        doc = Document("Test", "Author")
        section = Section("Content")
        section.add(Heading(2, "Subsection"))
        section.add(Paragraph("Hello"))

        doc.add(section)

        md = doc.export_to_markdown()
        assert "# Test" in md
        assert "## Subsection" in md
        assert "Hello" in md

    def test_document_builder(self) -> None:
        """Verify document builder."""
        doc = (
            DocumentBuilder("Report", "Jane Doe")
            .add_section("Introduction")
            .add_heading(2, "Welcome")
            .add_paragraph("Welcome to the report.")
            .add_bullet_list(["Point 1", "Point 2", "Point 3"])
            .add_section("Conclusion")
            .add_paragraph("Thanks for reading.")
            .build()
        )

        assert doc.get_metadata()["section_count"] == 2
        assert doc.get_word_count() > 0

    def test_complex_document_structure(self) -> None:
        """Verify complex document with nested sections."""
        builder = DocumentBuilder("Technical Guide", "Tech Team")

        builder.add_section("Getting Started")
        builder.add_heading(2, "Installation")
        builder.add_paragraph("Download and install the software.")
        builder.add_bullet_list(["Step 1: Download", "Step 2: Install", "Step 3: Configure"])

        builder.add_section("Advanced Topics")
        builder.add_heading(2, "Configuration")
        builder.add_paragraph("Configure advanced settings here.")

        doc = builder.build()

        assert doc.get_metadata()["word_count"] > 0
        assert len(doc.export_to_html()) > 0
        assert len(doc.export_to_markdown()) > 0


