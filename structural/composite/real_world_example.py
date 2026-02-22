"""
Real-World Example: Document Structure with Nested Sections.

This example demonstrates the Composite pattern in organizing
a complex document with sections, subsections, paragraphs, and
formatting. The pattern allows treating individual elements and
compositions uniformly.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum


class TextElement(ABC):
    """Abstract base for text elements in document."""

    @abstractmethod
    def get_content(self) -> str:
        """Get rendered content."""
        pass

    @abstractmethod
    def add(self, element: TextElement) -> None:
        """Add child element."""
        pass

    @abstractmethod
    def remove(self, element: TextElement) -> None:
        """Remove child element."""
        pass

    @abstractmethod
    def export_to_html(self) -> str:
        """Export to HTML."""
        pass

    @abstractmethod
    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        pass

    @abstractmethod
    def get_word_count(self) -> int:
        """Get word count."""
        pass


class Paragraph(TextElement):
    """Leaf - represents a paragraph."""

    def __init__(self, text: str) -> None:
        """Initialize paragraph."""
        self.text = text

    def get_content(self) -> str:
        """Get paragraph content."""
        return self.text

    def add(self, element: TextElement) -> None:
        """Not supported for paragraph."""
        raise ValueError("Cannot add to Paragraph")

    def remove(self, element: TextElement) -> None:
        """Not supported for paragraph."""
        raise ValueError("Cannot remove from Paragraph")

    def export_to_html(self) -> str:
        """Export to HTML."""
        return f"<p>{self.text}</p>"

    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        return f"{self.text}\n"

    def get_word_count(self) -> int:
        """Get word count of paragraph."""
        return len(self.text.split())


class Heading(TextElement):
    """Leaf - represents a heading."""

    def __init__(self, level: int, text: str) -> None:
        """Initialize heading."""
        self.level = level
        self.text = text

    def get_content(self) -> str:
        """Get heading content."""
        return self.text

    def add(self, element: TextElement) -> None:
        """Not supported for heading."""
        raise ValueError("Cannot add to Heading")

    def remove(self, element: TextElement) -> None:
        """Not supported for heading."""
        raise ValueError("Cannot remove from Heading")

    def export_to_html(self) -> str:
        """Export to HTML."""
        return f"<h{self.level}>{self.text}</h{self.level}>"

    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        return f"{'#' * self.level} {self.text}\n"

    def get_word_count(self) -> int:
        """Get word count."""
        return len(self.text.split())


class BulletList(TextElement):
    """Composite - represents bulleted list."""

    def __init__(self) -> None:
        """Initialize list."""
        self.items: List[TextElement] = []

    def add(self, element: TextElement) -> None:
        """Add list item."""
        self.items.append(element)

    def remove(self, element: TextElement) -> None:
        """Remove list item."""
        self.items.remove(element)

    def get_content(self) -> str:
        """Get list content."""
        return "\n".join(item.get_content() for item in self.items)

    def export_to_html(self) -> str:
        """Export to HTML."""
        html_items = [f"<li>{item.export_to_html()}</li>" for item in self.items]
        return f"<ul>{''.join(html_items)}</ul>"

    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        md_items = [f"- {item.export_to_markdown().strip()}" for item in self.items]
        return "\n".join(md_items) + "\n"

    def get_word_count(self) -> int:
        """Get total word count."""
        return sum(item.get_word_count() for item in self.items)


class Section(TextElement):
    """Composite - represents document section."""

    def __init__(self, title: str) -> None:
        """Initialize section."""
        self.title = title
        self.children: List[TextElement] = []

    def add(self, element: TextElement) -> None:
        """Add section content."""
        self.children.append(element)

    def remove(self, element: TextElement) -> None:
        """Remove section content."""
        self.children.remove(element)

    def get_content(self) -> str:
        """Get section content."""
        content = [f"Section: {self.title}"]
        for child in self.children:
            content.append(child.get_content())
        return "\n".join(content)

    def export_to_html(self) -> str:
        """Export to HTML."""
        html_content = "".join(child.export_to_html() for child in self.children)
        return f"<section><h1>{self.title}</h1>{html_content}</section>"

    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        md_content = "".join(child.export_to_markdown() for child in self.children)
        return f"# {self.title}\n\n{md_content}"

    def get_word_count(self) -> int:
        """Get total word count."""
        return sum(child.get_word_count() for child in self.children)

    def get_children(self) -> List[TextElement]:
        """Get section children."""
        return self.children.copy()


class Document(TextElement):
    """Composite - represents complete document."""

    def __init__(self, title: str, author: str) -> None:
        """Initialize document."""
        self.title = title
        self.author = author
        self.sections: List[TextElement] = []

    def add(self, element: TextElement) -> None:
        """Add document section."""
        self.sections.append(element)

    def remove(self, element: TextElement) -> None:
        """Remove section."""
        self.sections.remove(element)

    def get_content(self) -> str:
        """Get document content."""
        content = [f"Document: {self.title}", f"Author: {self.author}"]
        for section in self.sections:
            content.append(section.get_content())
        return "\n".join(content)

    def export_to_html(self) -> str:
        """Export to HTML."""
        html_content = "".join(section.export_to_html() for section in self.sections)
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <meta name="author" content="{self.author}">
</head>
<body>
    <h1>{self.title}</h1>
    <p>By {self.author}</p>
    {html_content}
</body>
</html>
        """.strip()

    def export_to_markdown(self) -> str:
        """Export to Markdown."""
        md_content = "".join(section.export_to_markdown() for section in self.sections)
        return f"# {self.title}\n\nAuthor: {self.author}\n\n{md_content}"

    def get_word_count(self) -> int:
        """Get total word count."""
        return sum(section.get_word_count() for section in self.sections)

    def get_metadata(self) -> dict:
        """Get document metadata."""
        return {
            "title": self.title,
            "author": self.author,
            "word_count": self.get_word_count(),
            "section_count": len(self.sections),
        }


class DocumentBuilder:
    """Builder for creating documents with structure."""

    def __init__(self, title: str, author: str) -> None:
        """Initialize builder."""
        self.document = Document(title, author)
        self.current_section: Optional[Section] = None

    def add_section(self, title: str) -> DocumentBuilder:
        """Add new section."""
        self.current_section = Section(title)
        self.document.add(self.current_section)
        return self

    def add_heading(self, level: int, text: str) -> DocumentBuilder:
        """Add heading to current section."""
        if not self.current_section:
            raise ValueError("No section active")
        self.current_section.add(Heading(level, text))
        return self

    def add_paragraph(self, text: str) -> DocumentBuilder:
        """Add paragraph to current section."""
        if not self.current_section:
            raise ValueError("No section active")
        self.current_section.add(Paragraph(text))
        return self

    def add_bullet_list(self, items: List[str]) -> DocumentBuilder:
        """Add bullet list to current section."""
        if not self.current_section:
            raise ValueError("No section active")

        bullet_list = BulletList()
        for item in items:
            bullet_list.add(Paragraph(item))

        self.current_section.add(bullet_list)
        return self

    def build(self) -> Document:
        """Get built document."""
        return self.document


