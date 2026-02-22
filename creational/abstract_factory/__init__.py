"""
Abstract Factory Pattern.

The Abstract Factory pattern provides an interface for creating families 
of related or dependent objects without specifying their concrete classes.

Examples:
    Creating UI elements for different operating systems:
    
    >>> from abstract_factory.pattern import OSFactory, WindowsUIFactory
    >>> factory = WindowsUIFactory()
    >>> button = factory.create_button()
    >>> checkbox = factory.create_checkbox()
"""
