"""
Builder Pattern.

The Builder pattern separates the construction of a complex object from 
its representation, allowing the same construction process to create 
different representations.

Examples:
    Building a complex HTTP request with various options:
    
    >>> from builder.pattern import RequestBuilder
    >>> request = RequestBuilder().with_method("POST").with_header("X-API-Key", "secret").build()
    >>> print(request.construct())
"""
