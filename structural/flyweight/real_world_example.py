"""Flyweight Real-World Example: Font Management System."""

from typing import Dict, List


class Font:
    """Flyweight - font properties (memory-intensive)."""

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        # Simulate expensive font data loading
        self.font_data = self._load_font()

    def _load_font(self) -> bytes:
        return b"Font data for " + self.name.encode() + b" size " + str(self.size).encode()

    def render_character(self, char: str) -> str:
        return f"[{self.name}:{self.size}] {char}"


class FontFactory:
    """Factory managing font flyweights."""

    fonts: Dict[str, Font] = {}

    @classmethod
    def get_font(cls, name: str, size: int) -> Font:
        key = f"{name}_{size}"
        if key not in cls.fonts:
            cls.fonts[key] = Font(name, size)
        return cls.fonts[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls.fonts)


class TextRenderer:
    """Renders text using font flyweights."""

    def __init__(self):
        self.text_data: List[tuple] = []

    def add_text(self, text: str, font_name: str, font_size: int, x: int, y: int) -> None:
        """Add text with font info."""
        font = FontFactory.get_font(font_name, font_size)
        self.text_data.append((text, font, x, y))

    def render(self) -> List[str]:
        """Render all text."""
        result = []
        for text, font, x, y in self.text_data:
            result.append(f"At ({x},{y}): {font.render_character(text[0])}")
        return result

