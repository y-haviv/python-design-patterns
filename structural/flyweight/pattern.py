"""Flyweight Pattern Implementation (Structural)."""

from typing import Dict, Optional


class Flyweight:
    """Flyweight object - stores intrinsic state."""

    def __init__(self, shared_state):
        self._shared_state = shared_state

    def operation(self, unique_state) -> str:
        s = str(self._shared_state)
        u = str(unique_state)
        return f"Flyweight({s}, {u})"


class FlyweightFactory:
    """Factory for creating and managing flyweights."""

    def __init__(self):
        self._flyweights: Dict = {}

    def get_flyweight(self, shared_state) -> Flyweight:
        """Get or create flyweight."""
        key = str(shared_state)
        if key not in self._flyweights:
            self._flyweights[key] = Flyweight(shared_state)
        return self._flyweights[key]

    def get_count(self) -> int:
        """Get number of flyweights."""
        return len(self._flyweights)


class TreeType:
    """Flyweight - tree type with intrinsic state."""

    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, x: int, y: int) -> str:
        return f"Drawing {self.name} at ({x}, {y})"


class Tree:
    """Object with unique state - references a TreeType flyweight."""

    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x = x
        self.y = y
        self.tree_type = tree_type  # Reference to flyweight

    def draw(self) -> str:
        return self.tree_type.draw(self.x, self.y)


class TreeFactory:
    """Factory for trees - manages TreeType flyweights."""

    tree_types: Dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        """Get or create tree type flyweight."""
        key = f"{name}_{color}_{texture}"
        if key not in cls.tree_types:
            cls.tree_types[key] = TreeType(name, color, texture)
        return cls.tree_types[key]

    @classmethod
    def get_flyweight_count(cls) -> int:
        """Get number of unique tree types."""
        return len(cls.tree_types)


class CharacterStyle:
    """Flyweight for character formatting."""

    def __init__(self, font: str, size: int, color: str):
        self.font = font
        self.size = size
        self.color = color

    def apply(self, text: str) -> str:
        return f"[{self.font}:{self.size}px:{self.color}]{text}[/]"


class Character:
    """Object with unique state using flyweight style."""

    def __init__(self, char: str, position: int, style: CharacterStyle):
        self.char = char
        self.position = position
        self.style = style

    def render(self) -> str:
        return self.style.apply(self.char)


class CharacterStyleFactory:
    """Factory for character styles."""

    styles: Dict[str, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int, color: str) -> CharacterStyle:
        """Get or create character style."""
        key = f"{font}_{size}_{color}"
        if key not in cls.styles:
            cls.styles[key] = CharacterStyle(font, size, color)
        return cls.styles[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls.styles)


class Image:
    """Flyweight - shared image object."""

    def __init__(self, file_path: str, width: int, height: int):
        self.file_path = file_path
        self.width = width
        self.height = height
        self.pixel_data = self._load_image()

    def _load_image(self) -> bytes:
        """Simulate loading image (expensive)."""
        return bytes(f"Image:{self.file_path}", 'utf-8')

    def get_info(self) -> str:
        return f"Image: {self.file_path} ({self.width}x{self.height})"


class ImageReference:
    """Reference to image with position data."""

    def __init__(self, image: Image, x: int, y: int, rotation: int = 0):
        self.image = image
        self.x = x
        self.y = y
        self.rotation = rotation

    def get_rendered_info(self) -> str:
        return f"{self.image.get_info()} at ({self.x}, {self.y}), rotation={self.rotation}"


class ImageFactory:
    """Factory for managing image flyweights."""

    images: Dict[str, Image] = {}

    @classmethod
    def get_image(cls, file_path: str, width: int = 100, height: int = 100) -> Image:
        """Get or create image flyweight."""
        if file_path not in cls.images:
            cls.images[file_path] = Image(file_path, width, height)
        return cls.images[file_path]

    @classmethod
    def get_count(cls) -> int:
        return len(cls.images)


class Particle:
    """Flyweight particle - shared state."""

    def __init__(self, color: str, velocity: float, mass: float):
        self.color = color
        self.velocity = velocity
        self.mass = mass

    def render(self, x: int, y: int) -> str:
        return f"Particle: {self.color} at ({x}, {y})"


class ParticleInstance:
    """Particle instance with unique position."""

    def __init__(self, particle: Particle, x: int, y: int):
        self.particle = particle
        self.x = x
        self.y = y

    def update(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def render(self) -> str:
        return self.particle.render(self.x, self.y)


class ParticleFactory:
    """Factory for particle flyweights."""

    particles: Dict[str, Particle] = {}

    @classmethod
    def create_particle(cls, color: str, velocity: float = 1.0, mass: float = 1.0) -> Particle:
        """Get or create particle type."""
        key = f"{color}_{velocity}_{mass}"
        if key not in cls.particles:
            cls.particles[key] = Particle(color, velocity, mass)
        return cls.particles[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls.particles)


