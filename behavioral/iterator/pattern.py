"""
Iterator Pattern Implementation (Behavioral).

Provides a way to access the elements of an aggregate object sequentially 
without exposing its underlying representation. Decouples the traversal logic 
from the collection, allowing multiple simultaneous iterators and alternative 
traversal strategies.

Key Components:
- Iterator: Abstract interface for traversing elements.
- ConcreteIterator: Implements the Iterator interface for a specific collection.
- Iterable: Abstract interface that returns an iterator.
- ConcreteIterable: Implements the Iterable interface (the collection itself).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class Iterator(ABC, Generic[T]):
    """
    Abstract interface for iterating over a collection.
    
    Defines the methods that any iterator must support to traverse
    a collection sequentially.
    """

    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements to iterate over."""
        pass

    @abstractmethod
    def next(self) -> T:
        """Get the next element in the iteration."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the iterator to the beginning."""
        pass


class Iterable(ABC, Generic[T]):
    """
    Abstract interface for objects that can be iterated over.
    
    Responsible for creating and returning an iterator that can 
    traverse the collection.
    """

    @abstractmethod
    def create_iterator(self) -> Iterator[T]:
        """Create an iterator for this collection."""
        pass


class ConcreteIterator(Iterator[T]):
    """
    Concrete iterator that traverses a specific collection.
    
    Maintains a current position and provides methods to move through
    the collection. Can be implemented for any internal representation
    (arrays, linked lists, trees, etc.).
    
    Attributes:
        collection: The collection being iterated.
        index: Current position in the collection.
    """

    def __init__(self, collection: ConcreteIterable[T]) -> None:
        """Initialize iterator with a collection."""
        self.collection = collection
        self.index = 0

    def has_next(self) -> bool:
        """Check if there are more elements."""
        return self.index < len(self.collection.items)

    def next(self) -> T:
        """Get the next element."""
        if not self.has_next():
            raise StopIteration("No more elements in the collection")
        
        element = self.collection.items[self.index]
        self.index += 1
        return element

    def reset(self) -> None:
        """Reset iterator to the beginning."""
        self.index = 0


class ReverseIterator(Iterator[T]):
    """
    Iterator that traverses a collection in reverse order.
    
    Demonstrates how different iteration strategies can be implemented
    by creating different iterator classes for the same collection.
    """

    def __init__(self, collection: ConcreteIterable[T]) -> None:
        """Initialize reverse iterator with a collection."""
        self.collection = collection
        self.index = len(collection.items) - 1

    def has_next(self) -> bool:
        """Check if there are more elements in reverse."""
        return self.index >= 0

    def next(self) -> T:
        """Get the next element in reverse order."""
        if not self.has_next():
            raise StopIteration("No more elements in the collection")
        
        element = self.collection.items[self.index]
        self.index -= 1
        return element

    def reset(self) -> None:
        """Reset iterator to the end."""
        self.index = len(self.collection.items) - 1


class FilteredIterator(Iterator[T]):
    """
    Iterator that only returns elements matching a predicate.
    
    Demonstrates filtering during iteration without creating a new collection.
    This is more memory-efficient for large collections.
    """

    def __init__(
        self, 
        collection: ConcreteIterable[T], 
        predicate: callable
    ) -> None:
        """
        Initialize filtered iterator.
        
        Args:
            collection: The collection to iterate over.
            predicate: Function that returns True for elements to include.
        """
        self.collection = collection
        self.predicate = predicate
        self.index = 0
        self._find_next_valid()

    def _find_next_valid(self) -> None:
        """Find the next element that matches the predicate."""
        while self.index < len(self.collection.items):
            if self.predicate(self.collection.items[self.index]):
                break
            self.index += 1

    def has_next(self) -> bool:
        """Check if there are more matching elements."""
        return self.index < len(self.collection.items)

    def next(self) -> T:
        """Get the next matching element."""
        if not self.has_next():
            raise StopIteration("No more matching elements")
        
        element = self.collection.items[self.index]
        self.index += 1
        self._find_next_valid()
        return element

    def reset(self) -> None:
        """Reset iterator to the beginning."""
        self.index = 0
        self._find_next_valid()


class ConcreteIterable(Iterable[T]):
    """
    Concrete collection that implements the Iterable interface.
    
    This represents the aggregate object that can be iterated over.
    It can create iterators on demand, supporting multiple simultaneous
    iterators and different iteration strategies.
    
    Attributes:
        items: The elements stored in this collection.
    """

    def __init__(self) -> None:
        """Initialize an empty collection."""
        self.items: List[T] = []

    def add_item(self, item: T) -> None:
        """Add an item to the collection."""
        self.items.append(item)

    def remove_item(self, item: T) -> None:
        """Remove an item from the collection."""
        if item in self.items:
            self.items.remove(item)

    def create_iterator(self) -> Iterator[T]:
        """Create a forward iterator for this collection."""
        return ConcreteIterator(self)

    def create_reverse_iterator(self) -> Iterator[T]:
        """Create a reverse iterator for this collection."""
        return ReverseIterator(self)

    def create_filtered_iterator(self, predicate: callable) -> Iterator[T]:
        """
        Create a filtered iterator for this collection.
        
        Args:
            predicate: Function that determines which elements to include.
                      Should return True for elements to include.
        """
        return FilteredIterator(self, predicate)

    def get_items(self) -> List[T]:
        """Get all items in the collection."""
        return self.items.copy()

    def __len__(self) -> int:
        """Get the number of items in the collection."""
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        """Support index access."""
        return self.items[index]


class BidirectionalIterator(Iterator[T]):
    """
    Iterator that can move both forward and backward through a collection.
    
    Demonstrates more advanced iteration with additional navigation methods.
    """

    def __init__(self, collection: ConcreteIterable[T]) -> None:
        """Initialize bidirectional iterator."""
        self.collection = collection
        self.index = 0

    def has_next(self) -> bool:
        """Check if there are elements ahead."""
        return self.index < len(self.collection.items) - 1

    def has_previous(self) -> bool:
        """Check if there are elements behind."""
        return self.index > 0

    def next(self) -> T:
        """Move to the next element."""
        if self.index >= len(self.collection.items):
            raise StopIteration("No more elements")
        element = self.collection.items[self.index]
        self.index += 1
        return element

    def previous(self) -> T:
        """Move to the previous element."""
        if self.index <= 0:
            raise StopIteration("No previous elements")
        self.index -= 1
        return self.collection.items[self.index]

    def reset(self) -> None:
        """Reset to the beginning."""
        self.index = 0

    def go_to_end(self) -> None:
        """Jump to the end of the collection."""
        self.index = len(self.collection.items) - 1

    def get_index(self) -> int:
        """Get current index."""
        return self.index


class LazyIterator(Iterator[T]):
    """
    Iterator that computes elements on-demand.
    
    Useful for large or infinite sequences where you don't want to
    compute or store all elements upfront.
    """

    def __init__(self, generator_func: callable, size: Optional[int] = None) -> None:
        """
        Initialize a lazy iterator.
        
        Args:
            generator_func: Function that takes index and returns value.
            size: Optional size of the sequence (None for infinite).
        """
        self.generator_func = generator_func
        self.size = size
        self.index = 0

    def has_next(self) -> bool:
        """Check if there are more elements."""
        if self.size is None:
            return True  # Infinite sequence
        return self.index < self.size

    def next(self) -> T:
        """Compute and return the next element."""
        if not self.has_next():
            raise StopIteration("Sequence exhausted")
        
        element = self.generator_func(self.index)
        self.index += 1
        return element

    def reset(self) -> None:
        """Reset to the beginning."""
        self.index = 0
