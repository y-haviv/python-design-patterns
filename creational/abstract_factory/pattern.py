"""
Abstract Factory Pattern - Structural Implementation.

This module demonstrates the Abstract Factory pattern, which provides an interface 
for creating families of related or dependent objects without specifying their 
concrete classes.

The Abstract Factory pattern is useful when a system needs to be independent 
of how its product families are created, or when you want to ensure that 
related objects are created together.

Key Components:
- Abstract Factory: Declares interface for creating products
- Concrete Factories: Implement the interface to create specific families
- Abstract Products: Declare interfaces for product types in a family
- Concrete Products: Implement specific product types
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Any, Optional


class UITheme(Enum):
    """Enumeration of supported UI themes (product families)."""
    LIGHT = "light"
    DARK = "dark"
    HIGHCONTRAST = "highcontrast"


# ============================================================================
# Abstract Products: UI Components
# ============================================================================


class Button(ABC):
    """
    Abstract Product: Button.
    
    Defines the interface that all button implementations must follow.
    The specific styling and behavior depends on the concrete implementation.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Render the button with theme-specific styling.
        
        Returns:
            A string description of the rendered button.
        """
        pass

    @abstractmethod
    def on_click(self, callback: str) -> str:
        """
        Register a click handler and return confirmation.
        
        Args:
            callback: The name of the callback function to invoke on click.
            
        Returns:
            Confirmation message.
        """
        pass


class Checkbox(ABC):
    """
    Abstract Product: Checkbox.
    
    Defines the interface that all checkbox implementations must follow.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Render the checkbox with theme-specific styling.
        
        Returns:
            A string description of the rendered checkbox.
        """
        pass

    @abstractmethod
    def set_checked(self, value: bool) -> str:
        """
        Set the checkbox state and return confirmation.
        
        Args:
            value: Whether the checkbox should be checked.
            
        Returns:
            Confirmation message.
        """
        pass


class TextInput(ABC):
    """
    Abstract Product: Text Input.
    
    Defines the interface that all text input implementations must follow.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Render the text input with theme-specific styling.
        
        Returns:
            A string description of the rendered input.
        """
        pass

    @abstractmethod
    def set_placeholder(self, text: str) -> str:
        """
        Set placeholder text and return confirmation.
        
        Args:
            text: The placeholder text to display.
            
        Returns:
            Confirmation message.
        """
        pass


# ============================================================================
# Concrete Products: Light Theme
# ============================================================================


class LightButton(Button):
    """
    Concrete Product: Light Theme Button.
    
    Implements a button with light theme styling (light background, dark text).
    """

    def render(self) -> str:
        """Render button with light theme."""
        return (
            "┌─────────┐\n"
            "│ Button  │  (Light Theme: white bg, black text)\n"
            "└─────────┘"
        )

    def on_click(self, callback: str) -> str:
        """Register click handler."""
        return f"Light Theme Button Click Handler '{callback}' registered"


class LightCheckbox(Checkbox):
    """
    Concrete Product: Light Theme Checkbox.
    
    Implements a checkbox with light theme styling.
    """

    def render(self) -> str:
        """Render checkbox with light theme."""
        return "☐ Checkbox (Light Theme: white bg, black border)"

    def set_checked(self, value: bool) -> str:
        """Set checkbox state."""
        symbol = "☑" if value else "☐"
        return f"{symbol} Checkbox set to {'checked' if value else 'unchecked'} (Light Theme)"


class LightTextInput(TextInput):
    """
    Concrete Product: Light Theme Text Input.
    
    Implements a text input with light theme styling.
    """

    def render(self) -> str:
        """Render text input with light theme."""
        return "┌────────────────┐\n│ Type here...   │  (Light Theme)\n└────────────────┘"

    def set_placeholder(self, text: str) -> str:
        """Set placeholder text."""
        return f"Light Theme TextInput placeholder set to '{text}'"


# ============================================================================
# Concrete Products: Dark Theme
# ============================================================================


class DarkButton(Button):
    """
    Concrete Product: Dark Theme Button.
    
    Implements a button with dark theme styling (dark background, light text).
    """

    def render(self) -> str:
        """Render button with dark theme."""
        return (
            "┏━━━━━━━━━┓\n"
            "┃ Button  ┃  (Dark Theme: black bg, white text)\n"
            "┗━━━━━━━━━┛"
        )

    def on_click(self, callback: str) -> str:
        """Register click handler."""
        return f"Dark Theme Button Click Handler '{callback}' registered"


class DarkCheckbox(Checkbox):
    """
    Concrete Product: Dark Theme Checkbox.
    
    Implements a checkbox with dark theme styling.
    """

    def render(self) -> str:
        """Render checkbox with dark theme."""
        return "☑ Checkbox (Dark Theme: black bg, light border)"

    def set_checked(self, value: bool) -> str:
        """Set checkbox state."""
        symbol = "☑" if value else "☐"
        return f"{symbol} Checkbox set to {'checked' if value else 'unchecked'} (Dark Theme)"


class DarkTextInput(TextInput):
    """
    Concrete Product: Dark Theme Text Input.
    
    Implements a text input with dark theme styling.
    """

    def render(self) -> str:
        """Render text input with dark theme."""
        return "┏━━━━━━━━━━━━━━━━┓\n┃ Type here...   ┃  (Dark Theme)\n┗━━━━━━━━━━━━━━━━┛"

    def set_placeholder(self, text: str) -> str:
        """Set placeholder text."""
        return f"Dark Theme TextInput placeholder set to '{text}'"


# ============================================================================
# Concrete Products: High Contrast Theme
# ============================================================================


class HighContrastButton(Button):
    """
    Concrete Product: High Contrast Theme Button.
    
    Implements a button with high contrast styling for accessibility.
    Uses maximum color contrast for readability.
    """

    def render(self) -> str:
        """Render button with high contrast theme."""
        return (
            "┏═════════┓\n"
            "┃ BUTTON  ┃  (High Contrast: yellow on black, large text)\n"
            "┗═════════┛"
        )

    def on_click(self, callback: str) -> str:
        """Register click handler."""
        return f"HIGH CONTRAST Button Click Handler '{callback}' REGISTERED (LOUD AND CLEAR)"


class HighContrastCheckbox(Checkbox):
    """
    Concrete Product: High Contrast Theme Checkbox.
    
    Implements a checkbox with high contrast styling for accessibility.
    """

    def render(self) -> str:
        """Render checkbox with high contrast theme."""
        return "★ CHECKBOX (HIGH CONTRAST: maximum contrast, enlarged borders)"

    def set_checked(self, value: bool) -> str:
        """Set checkbox state."""
        symbol = "★" if value else "☆"
        return f"{symbol} CHECKBOX SET TO {'CHECKED' if value else 'UNCHECKED'} (HIGH CONTRAST)"


class HighContrastTextInput(TextInput):
    """
    Concrete Product: High Contrast Theme Text Input.
    
    Implements a text input with high contrast styling for accessibility.
    """

    def render(self) -> str:
        """Render text input with high contrast theme."""
        return "╔════════════════╗\n║ TYPE HERE (HC) ║  (High Contrast)\n╚════════════════╝"

    def set_placeholder(self, text: str) -> str:
        """Set placeholder text."""
        return f"HIGH CONTRAST TextInput PLACEHOLDER SET TO '{text}'"


# ============================================================================
# Abstract Factory
# ============================================================================


class UIFactory(ABC):
    """
    Abstract Factory.
    
    Declares interface methods for creating abstract products (buttons, 
    checkboxes, text inputs, etc.). Each concrete factory provides 
    theme-specific implementations.
    
    Key Benefit: Ensures that UI components from the same theme family 
    are used together. The client code depends only on this abstract interface,
    not on concrete implementations.
    """

    @abstractmethod
    def create_button(self) -> Button:
        """
        Create a button for this theme.
        
        Returns:
            A Button instance (theme-specific).
        """
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """
        Create a checkbox for this theme.
        
        Returns:
            A Checkbox instance (theme-specific).
        """
        pass

    @abstractmethod
    def create_text_input(self) -> TextInput:
        """
        Create a text input for this theme.
        
        Returns:
            A TextInput instance (theme-specific).
        """
        pass


# ============================================================================
# Concrete Factories
# ============================================================================


class LightThemeFactory(UIFactory):
    """
    Concrete Factory: Light Theme.
    
    Creates a family of UI components styled for light theme.
    All components created by this factory share consistent light styling.
    """

    def create_button(self) -> Button:
        """Create a light-themed button."""
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        """Create a light-themed checkbox."""
        return LightCheckbox()

    def create_text_input(self) -> TextInput:
        """Create a light-themed text input."""
        return LightTextInput()


class DarkThemeFactory(UIFactory):
    """
    Concrete Factory: Dark Theme.
    
    Creates a family of UI components styled for dark theme.
    All components created by this factory share consistent dark styling.
    """

    def create_button(self) -> Button:
        """Create a dark-themed button."""
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        """Create a dark-themed checkbox."""
        return DarkCheckbox()

    def create_text_input(self) -> TextInput:
        """Create a dark-themed text input."""
        return DarkTextInput()


class HighContrastThemeFactory(UIFactory):
    """
    Concrete Factory: High Contrast Theme.
    
    Creates a family of UI components styled for high contrast (accessibility).
    All components created by this factory share consistent high contrast styling
    suitable for users with visual impairments.
    """

    def create_button(self) -> Button:
        """Create a high-contrast-themed button."""
        return HighContrastButton()

    def create_checkbox(self) -> Checkbox:
        """Create a high-contrast-themed checkbox."""
        return HighContrastCheckbox()

    def create_text_input(self) -> TextInput:
        """Create a high-contrast-themed text input."""
        return HighContrastTextInput()


# ============================================================================
# Application & Registry (Enhancement)
# ============================================================================


class Application:
    """
    Application: Uses the Abstract Factory to create UI components.
    
    The key benefit is that the application code depends only on the 
    abstract factory and product interfaces, not on concrete implementations.
    This allows switching themes at runtime without changing application code.
    """

    def __init__(self, factory: UIFactory) -> None:
        """
        Initialize application with a specific theme factory.
        
        Args:
            factory: The UIFactory to use for creating components.
        """
        self._factory = factory
        self._button = factory.create_button()
        self._checkbox = factory.create_checkbox()
        self._text_input = factory.create_text_input()

    def render_ui(self) -> str:
        """
        Render the entire UI using the factory's components.
        
        Returns:
            A string representation of the complete UI.
        """
        ui = "=== APPLICATION UI ===\n"
        ui += f"{self._button.render()}\n\n"
        ui += f"{self._checkbox.render()}\n\n"
        ui += f"{self._text_input.render()}\n"
        ui += "===================="
        return ui

    def interact(self) -> str:
        """
        Demonstrate interactions with UI components.
        
        Returns:
            A string showing interaction results.
        """
        interactions = "=== USER INTERACTIONS ===\n"
        interactions += f"{self._button.on_click('handleSubmit')}\n"
        interactions += f"{self._checkbox.set_checked(True)}\n"
        interactions += f"{self._text_input.set_placeholder('Enter your name')}\n"
        interactions += "=========================="
        return interactions


class UIThemeRegistry:
    """
    Registry Pattern (Enhancement): Manages theme factories.
    
    This registry provides centralized factory management and allows 
    switching themes at runtime without requiring factory knowledge.
    """

    def __init__(self):
        """Initialize registry with available themes."""
        self._factories: Dict[UITheme, UIFactory] = {
            UITheme.LIGHT: LightThemeFactory(),
            UITheme.DARK: DarkThemeFactory(),
            UITheme.HIGHCONTRAST: HighContrastThemeFactory(),
        }

    def get_factory(self, theme: UITheme) -> UIFactory:
        """
        Retrieve a factory for the specified theme.
        
        Args:
            theme: The UITheme enum value.
            
        Returns:
            The corresponding UIFactory instance.
            
        Raises:
            ValueError: If the theme is not registered.
        """
        if theme not in self._factories:
            raise ValueError(f"Unknown theme: {theme}")
        return self._factories[theme]

    def create_application(self, theme: UITheme) -> Application:
        """
        Create an application with the specified theme.
        
        Args:
            theme: The desired UITheme.
            
        Returns:
            An Application instance with theme-specific components.
        """
        factory = self.get_factory(theme)
        return Application(factory)

    def register_factory(self, theme: UITheme, factory: UIFactory) -> None:
        """
        Register a custom factory for a theme.
        
        This allows adding custom themes or replacing existing ones at runtime.
        
        Args:
            theme: The UITheme enum value.
            factory: The UIFactory instance to register.
        """
        self._factories[theme] = factory

    def list_available_themes(self) -> list:
        """
        List all available themes.
        
        Returns:
            A list of available UITheme enum values.
        """
        return list(self._factories.keys())
