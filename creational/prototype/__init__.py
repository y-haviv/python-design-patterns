"""
Prototype Pattern.

The Prototype pattern provides a way to create new objects by copying an existing 
object (prototype) rather than creating from scratch. This is useful when object 
creation is expensive or when you need to create variants of complex objects.

Examples:
    Cloning a document template with customizations:
    
    >>> from creational.prototype.pattern import Document
    >>> template = Document("Template Title")
    >>> document1 = template.clone()
    >>> document1.title = "Custom Title"
"""
