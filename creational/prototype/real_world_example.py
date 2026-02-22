"""
Real-world Prototype: Design System Component Library.

This example demonstrates a design system (like Material Design or Bootstrap) 
where UI components have predefined themes/variants. Instead of creating 
each variant from scratch, prototypes are cloned and customized.

This is commonly used in:
- UI component libraries
- Design system implementations
- Form builders
- Page builders
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from copy import deepcopy


@dataclass
class Color:
    """Color representation."""
    name: str
    hex_code: str
    rgb: tuple = field(default=(0, 0, 0))


@dataclass
class Typography:
    """Typography settings."""
    font_family: str
    sizes: Dict[str, int] = field(default_factory=dict)  # heading1, heading2, body, etc.
    weights: Dict[str, int] = field(default_factory=dict)  # normal, bold, etc.
    line_heights: Dict[str, float] = field(default_factory=dict)


@dataclass
class Spacing:
    """Spacing scale."""
    unit: int = 4  # 4px base unit
    values: Dict[str, int] = field(default_factory=dict)  # xs, sm, md, lg, xl


@dataclass
class DesignTheme:
    """
    Prototype: Design System Theme.
    
    A complete theme definition with colors, typography, spacing, etc.
    Expensive to create, cheap to clone for variations.
    """

    name: str
    colors: Dict[str, Color] = field(default_factory=dict)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    border_radius: Dict[str, int] = field(default_factory=dict)
    shadows: Dict[str, str] = field(default_factory=dict)
    breakpoints: Dict[str, int] = field(default_factory=dict)

    def clone(self) -> DesignTheme:
        """
        Create a deep copy of this theme.
        
        Useful for creating theme variations (light, dark, etc.)
        
        Returns:
            A completely independent copy of this theme.
        """
        return deepcopy(self)

    def get_theme_summary(self) -> str:
        """Get a summary of the theme."""
        summary = f"Theme: {self.name}\n"
        summary += f"Colors: {len(self.colors)}\n"
        summary += f"Spacing values: {len(self.spacing.values)}\n"
        summary += f"Border radiuses: {len(self.border_radius)}\n"
        summary += f"Shadows: {len(self.shadows)}\n"
        return summary


def create_light_theme_prototype() -> DesignTheme:
    """
    Create the light theme prototype (expensive operation).
    
    In reality, this might:
    - Load from a design system server
    - Parse a design tokens file
    - Query a design database
    - Load and process large SVG assets
    
    Returns:
        A complete light theme prototype.
    """
    light_theme = DesignTheme(name="Light Theme")

    # Colors
    light_theme.colors = {
        "primary": Color("Primary Blue", "#0066CC"),
        "secondary": Color("Secondary Gray", "#666666"),
        "success": Color("Success Green", "#00AA00"),
        "warning": Color("Warning Yellow", "#FFAA00"),
        "error": Color("Error Red", "#CC0000"),
        "background": Color("Background", "#FFFFFF"),
        "surface": Color("Surface", "#F5F5F5"),
        "text": Color("Text", "#000000"),
    }

    # Typography
    light_theme.typography = Typography(
        font_family="Inter, sans-serif",
        sizes={
            "h1": 32,
            "h2": 28,
            "h3": 24,
            "h4": 20,
            "body": 16,
            "caption": 12,
        },
        weights={
            "normal": 400,
            "medium": 500,
            "bold": 700,
        },
        line_heights={
            "tight": 1.2,
            "normal": 1.5,
            "relaxed": 1.8,
        }
    )

    # Spacing
    light_theme.spacing.values = {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
        "2xl": 48,
    }

    # Border radius
    light_theme.border_radius = {
        "none": 0,
        "sm": 4,
        "md": 8,
        "lg": 12,
        "full": 9999,
    }

    # Shadows
    light_theme.shadows = {
        "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
        "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "lg": "0 10px 15px rgba(0, 0, 0, 0.1)",
        "xl": "0 20px 25px rgba(0, 0, 0, 0.15)",
    }

    # Breakpoints
    light_theme.breakpoints = {
        "xs": 0,
        "sm": 640,
        "md": 768,
        "lg": 1024,
        "xl": 1280,
        "2xl": 1536,
    }

    return light_theme


def create_dark_theme_from_light(light_prototype: DesignTheme) -> DesignTheme:
    """
    Create a dark theme by cloning and modifying the light theme.
    
    Instead of creating from scratch (expensive), we clone the light
    prototype and modify specific colors.
    
    Args:
        light_prototype: The light theme prototype to base on.
        
    Returns:
        A dark theme variant.
    """
    dark_theme = light_prototype.clone()
    dark_theme.name = "Dark Theme"

    # Invert colors
    dark_theme.colors = {
        "primary": Color("Primary Blue", "#6699FF"),
        "secondary": Color("Secondary Gray", "#AAAAAA"),
        "success": Color("Success Green", "#66FF66"),
        "warning": Color("Warning Yellow", "#FFDD66"),
        "error": Color("Error Red", "#FF6666"),
        "background": Color("Background", "#1A1A1A"),
        "surface": Color("Surface", "#2D2D2D"),
        "text": Color("Text", "#FFFFFF"),
    }

    # Adjust shadows for dark mode
    dark_theme.shadows = {
        "sm": "0 1px 2px rgba(0, 0, 0, 0.3)",
        "md": "0 4px 6px rgba(0, 0, 0, 0.4)",
        "lg": "0 10px 15px rgba(0, 0, 0, 0.5)",
        "xl": "0 20px 25px rgba(0, 0, 0, 0.6)",
    }

    return dark_theme


def create_high_contrast_theme_from_light(light_prototype: DesignTheme) -> DesignTheme:
    """
    Create a high-contrast theme for accessibility.
    
    Args:
        light_prototype: The light theme prototype to base on.
        
    Returns:
        A high-contrast theme variant.
    """
    hc_theme = light_prototype.clone()
    hc_theme.name = "High Contrast Theme"

    # Maximum contrast colors
    hc_theme.colors = {
        "primary": Color("Primary", "#0000FF"),
        "secondary": Color("Secondary", "#000000"),
        "success": Color("Success", "#008000"),
        "warning": Color("Warning", "#FFFF00"),
        "error": Color("Error", "#FF0000"),
        "background": Color("Background", "#FFFFFF"),
        "surface": Color("Surface", "#CCCCCC"),
        "text": Color("Text", "#000000"),
    }

    # Increase font sizes for accessibility
    hc_theme.typography.sizes = {
        "h1": 40,
        "h2": 36,
        "h3": 32,
        "h4": 28,
        "body": 18,
        "caption": 16,
    }

    # Bolder shadows for better visibility
    hc_theme.shadows = {
        "sm": "0 2px 4px rgba(0, 0, 0, 0.8)",
        "md": "0 6px 12px rgba(0, 0, 0, 0.8)",
        "lg": "0 12px 24px rgba(0, 0, 0, 0.8)",
        "xl": "0 24px 48px rgba(0, 0, 0, 0.8)",
    }

    return hc_theme


def create_compact_theme_from_light(light_prototype: DesignTheme) -> DesignTheme:
    """
    Create a compact theme for space-constrained interfaces.
    
    Args:
        light_prototype: The light theme prototype to base on.
        
    Returns:
        A compact theme variant.
    """
    compact_theme = light_prototype.clone()
    compact_theme.name = "Compact Theme"

    # Reduce font sizes
    compact_theme.typography.sizes = {
        "h1": 24,
        "h2": 20,
        "h3": 18,
        "h4": 16,
        "body": 13,
        "caption": 11,
    }

    # Reduce spacing
    compact_theme.spacing.values = {
        "xs": 2,
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16,
        "2xl": 24,
    }

    # Reduce border radius
    compact_theme.border_radius = {
        "none": 0,
        "sm": 2,
        "md": 4,
        "lg": 6,
        "full": 9999,
    }

    return compact_theme


class ThemeLibrary:
    """
    Manages multiple theme prototypes and provides variants through cloning.
    
    This demonstrates the registry pattern combined with Prototype pattern
    for efficient theme management.
    """

    def __init__(self):
        """Initialize theme library."""
        # Create prototype themes (expensive)
        self._light_prototype = create_light_theme_prototype()

        # Store prototypes
        self._prototypes: Dict[str, DesignTheme] = {
            "light": self._light_prototype,
            "dark": create_dark_theme_from_light(self._light_prototype),
            "high_contrast": create_high_contrast_theme_from_light(self._light_prototype),
            "compact": create_compact_theme_from_light(self._light_prototype),
        }

    def get_theme(self, theme_name: str) -> DesignTheme:
        """
        Get a theme (returns the prototype; clone if you need to modify).
        
        Args:
            theme_name: Name of the theme.
            
        Returns:
            The theme prototype.
        """
        if theme_name not in self._prototypes:
            raise ValueError(f"Theme '{theme_name}' not found")
        return self._prototypes[theme_name]

    def create_theme_variant(self, template_name: str, name: str) -> DesignTheme:
        """
        Create a custom theme variant by cloning a template.
        
        Args:
            template_name: Name of the template theme to clone.
            name: Name for the new variant.
            
        Returns:
            A cloned theme ready for customization.
        """
        template = self.get_theme(template_name)
        variant = template.clone()
        variant.name = name
        return variant

    def list_available_themes(self) -> List[str]:
        """List all available theme names."""
        return list(self._prototypes.keys())

    def get_theme_clone(self, theme_name: str) -> DesignTheme:
        """
        Get an independent clone of a theme for modification.
        
        Args:
            theme_name: Name of the theme to clone.
            
        Returns:
            A deep copy of the theme.
        """
        theme = self.get_theme(theme_name)
        return theme.clone()


def demonstrate_theme_system() -> List[str]:
    """
    Demonstrate the theme system with cloning and variants.
    
    Returns:
        A list of theme demonstrations.
    """
    results = []

    # Create base prototype (expensive operation, done once)
    light_prototype = create_light_theme_prototype()
    results.append(f"Created light theme prototype: {light_prototype.get_theme_summary()}")

    # Create variants by cloning (cheap operations)
    dark_theme = create_dark_theme_from_light(light_prototype)
    results.append(f"Created dark theme variant via clone: {dark_theme.get_theme_summary()}")

    # Use the library
    library = ThemeLibrary()
    results.append(f"Theme library initialized with themes: {', '.join(library.list_available_themes())}")

    # Get and customize a theme
    custom_theme = library.get_theme_clone("light")
    custom_theme.name = "Custom Corporate Theme"
    custom_theme.colors["primary"] = Color("Corporate Blue", "#003366")
    results.append(f"Created custom theme: {custom_theme.get_theme_summary()}")

    return results
