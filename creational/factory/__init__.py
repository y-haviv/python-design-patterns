"""
Factory Method Pattern.

The Factory Method pattern provides a way to create objects without specifying 
the exact classes that will be instantiated. It uses an interface (or abstract class) 
as a contract for creating objects, allowing subclasses to decide the concrete type.

Examples:
    Creating a logger that works with different backends:
    
    >>> from factory.pattern import TransportFactory, HTTPFactory
    >>> factory = HTTPFactory()
    >>> transport = factory.create_transport()
    >>> print(transport.connect())
"""
