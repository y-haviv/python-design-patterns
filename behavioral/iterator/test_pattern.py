"""
Comprehensive tests for the Iterator Pattern.

These tests verify:
1. Basic forward iteration.
2. Reverse iteration.
3. Filtered iteration.
4. Bidirectional iteration.
5. Multiple simultaneous iterators.
6. Iterator reset functionality.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Iterator,
    Iterable,
    ConcreteIterator,
    ConcreteIterable,
    ReverseIterator,
    FilteredIterator,
    BidirectionalIterator,
    LazyIterator,
)
from .real_world_example import (
    Book,
    BookCollection,
    BookIterator,
    ReverseBookIterator,
    FilteredBookIterator,
)


class TestConcreteIterator:
    """Tests for basic forward iteration."""

    def test_iterator_initialization(self) -> None:
        """Verify iterator initializes correctly."""
        collection = ConcreteIterable()
        collection.add_item(1)
        collection.add_item(2)
        
        iterator = collection.create_iterator()
        assert iterator.has_next() is True

    def test_forward_iteration(self) -> None:
        """Verify forward iteration through elements."""
        collection = ConcreteIterable()
        for i in range(1, 6):
            collection.add_item(i)
        
        iterator = collection.create_iterator()
        results = []
        
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [1, 2, 3, 4, 5]

    def test_has_next_at_end(self) -> None:
        """Verify has_next returns False at the end."""
        collection = ConcreteIterable()
        collection.add_item("a")
        collection.add_item("b")
        
        iterator = collection.create_iterator()
        iterator.next()
        iterator.next()
        
        assert iterator.has_next() is False

    def test_iterator_stop_iteration(self) -> None:
        """Verify StopIteration is raised when no more elements."""
        collection = ConcreteIterable()
        collection.add_item(1)
        
        iterator = collection.create_iterator()
        iterator.next()
        
        with pytest.raises(StopIteration):
            iterator.next()

    def test_iterator_reset(self) -> None:
        """Verify iterator can be reset to the beginning."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iterator = collection.create_iterator()
        
        # Iterate through all
        while iterator.has_next():
            iterator.next()
        
        assert iterator.has_next() is False
        
        # Reset
        iterator.reset()
        assert iterator.has_next() is True
        assert iterator.next() == 1


class TestReverseIterator:
    """Tests for reverse iteration."""

    def test_reverse_iterator_basic(self) -> None:
        """Verify reverse iteration works correctly."""
        collection = ConcreteIterable()
        for i in range(1, 6):
            collection.add_item(i)
        
        iterator = collection.create_reverse_iterator()
        results = []
        
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [5, 4, 3, 2, 1]

    def test_reverse_iterator_reset(self) -> None:
        """Verify reverse iterator reset goes to the end."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iterator = collection.create_reverse_iterator()
        iterator.next()
        iterator.next()
        
        iterator.reset()
        assert iterator.next() == 3


class TestFilteredIterator:
    """Tests for filtered iteration."""

    def test_filtered_iterator_basic(self) -> None:
        """Verify filtered iteration returns only matching elements."""
        collection = ConcreteIterable()
        for i in range(1, 11):
            collection.add_item(i)
        
        # Filter for even numbers
        iterator = collection.create_filtered_iterator(
            predicate=lambda x: x % 2 == 0
        )
        
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [2, 4, 6, 8, 10]

    def test_filtered_iterator_no_matches(self) -> None:
        """Verify filtered iterator with no matches."""
        collection = ConcreteIterable()
        for i in range(1, 6):
            collection.add_item(i)
        
        # Filter for values > 100
        iterator = collection.create_filtered_iterator(
            predicate=lambda x: x > 100
        )
        
        assert iterator.has_next() is False

    def test_filtered_iterator_reset(self) -> None:
        """Verify filtered iterator can be reset."""
        collection = ConcreteIterable()
        for i in range(1, 6):
            collection.add_item(i)
        
        iterator = collection.create_filtered_iterator(
            predicate=lambda x: x % 2 == 0
        )
        
        # First pass
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [2, 4]
        
        # Reset and do it again
        iterator.reset()
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [2, 4]


class TestBidirectionalIterator:
    """Tests for bidirectional iteration."""

    def test_bidirectional_forward(self) -> None:
        """Verify forward movement in bidirectional iterator."""
        collection = ConcreteIterable()
        for i in range(1, 6):
            collection.add_item(i)
        
        iterator = BidirectionalIterator(collection)
        
        assert iterator.next() == 1
        assert iterator.next() == 2
        assert iterator.has_next() is True

    def test_bidirectional_backward(self) -> None:
        """Verify backward movement."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iterator = BidirectionalIterator(collection)
        iterator.next()
        iterator.next()
        
        assert iterator.previous() == 2
        assert iterator.previous() == 1

    def test_bidirectional_go_to_end(self) -> None:
        """Verify jumping to the end."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iterator = BidirectionalIterator(collection)
        iterator.go_to_end()
        
        assert iterator.next() == 3

    def test_bidirectional_get_index(self) -> None:
        """Verify getting current index."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iterator = BidirectionalIterator(collection)
        
        assert iterator.get_index() == 0
        iterator.next()
        assert iterator.get_index() == 1


class TestLazyIterator:
    """Tests for lazy evaluation iterators."""

    def test_lazy_iterator_finite(self) -> None:
        """Verify lazy iterator with finite sequence."""
        # Generate squares: 0, 1, 4, 9, 16
        iterator = LazyIterator(lambda i: i ** 2, size=5)
        
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        
        assert results == [0, 1, 4, 9, 16]

    def test_lazy_iterator_infinite(self) -> None:
        """Verify lazy iterator with infinite sequence."""
        # Fibonacci sequence
        fib_cache = {}
        def fib(n):
            if n <= 1:
                return n
            if n in fib_cache:
                return fib_cache[n]
            fib_cache[n] = fib(n - 1) + fib(n - 2)
            return fib_cache[n]
        
        iterator = LazyIterator(fib, size=None)
        
        # Generate first 10 fibonacci numbers
        results = []
        for _ in range(10):
            if iterator.has_next():
                results.append(iterator.next())
        
        assert len(results) == 10

    def test_lazy_iterator_reset(self) -> None:
        """Verify lazy iterator reset."""
        iterator = LazyIterator(lambda i: i * 2, size=3)
        
        # First pass
        results1 = []
        while iterator.has_next():
            results1.append(iterator.next())
        
        # Reset
        iterator.reset()
        
        # Second pass
        results2 = []
        while iterator.has_next():
            results2.append(iterator.next())
        
        assert results1 == results2 == [0, 2, 4]


class TestMultipleSimultaneousIterators:
    """Tests for multiple iterators on the same collection."""

    def test_multiple_iterators_independent(self) -> None:
        """Verify multiple iterators are independent."""
        collection = ConcreteIterable()
        for i in range(1, 4):
            collection.add_item(i)
        
        iter1 = collection.create_iterator()
        iter2 = collection.create_iterator()
        
        assert iter1.next() == 1
        assert iter2.next() == 1
        assert iter1.next() == 2
        assert iter2.next() == 2


class TestBookCollectionExample:
    """Tests for the real-world book collection example."""

    @pytest.fixture
    def library(self) -> BookCollection:
        """Create a test library with sample books."""
        lib = BookCollection()
        lib.add_book(Book("Foundation", "Isaac Asimov", 1951, 255, "Science Fiction"))
        lib.add_book(Book("I, Robot", "Isaac Asimov", 1950, 224, "Science Fiction"))
        lib.add_book(Book("Dune", "Frank Herbert", 1965, 682, "Science Fiction"))
        lib.add_book(Book("1984", "George Orwell", 1949, 328, "Dystopian"))
        lib.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "Classic"))
        return lib

    def test_book_forward_iteration(self, library: BookCollection) -> None:
        """Verify iterating through all books."""
        iterator = library.create_iterator()
        count = 0
        while iterator.has_next():
            iterator.next()
            count += 1
        
        assert count == 5

    def test_book_reverse_iteration(self, library: BookCollection) -> None:
        """Verify reverse iteration through books."""
        iterator = library.create_reverse_iterator()
        first_book = iterator.next()
        
        assert first_book.title == "The Great Gatsby"

    def test_book_filtered_iteration(self, library: BookCollection) -> None:
        """Verify filtering books by genre."""
        iterator = library.create_filtered_iterator(genre="Science Fiction")
        
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        
        assert len(results) == 3
        assert all(b.genre == "Science Fiction" for b in results)

    def test_get_books_by_author(self, library: BookCollection) -> None:
        """Verify getting books by author."""
        asimov_books = library.get_books_by_author("Isaac Asimov")
        
        assert len(asimov_books) == 2
        assert all(b.author == "Isaac Asimov" for b in asimov_books)

    def test_library_length(self, library: BookCollection) -> None:
        """Verify library size."""
        assert len(library) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
