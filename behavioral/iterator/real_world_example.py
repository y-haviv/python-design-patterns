"""
Real-World Example: Book Collection Iterator.

Demonstrates a practical library/bookstore application where books are stored
in a collection and can be iterated over in multiple ways: forward, reverse,
filtered by criteria, etc.
"""

from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass
from .pattern import Iterator, Iterable, ConcreteIterable


@dataclass
class Book:
    """Represents a book in the collection."""
    title: str
    author: str
    year: int
    pages: int
    genre: str

    def __repr__(self) -> str:
        return f"Book('{self.title}' by {self.author}, {self.year})"

    def matches_criteria(self, **criteria) -> bool:
        """Check if book matches all given criteria."""
        for key, value in criteria.items():
            if hasattr(self, key):
                if isinstance(value, str):
                    if value.lower() not in getattr(self, key).lower():
                        return False
                else:
                    if getattr(self, key) != value:
                        return False
        return True


class BookIterator(Iterator[Book]):
    """Standard forward iterator for books."""

    def __init__(self, books: List[Book]) -> None:
        self.books = books
        self.index = 0

    def has_next(self) -> bool:
        return self.index < len(self.books)

    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books")
        book = self.books[self.index]
        self.index += 1
        return book

    def reset(self) -> None:
        self.index = 0


class ReverseBookIterator(Iterator[Book]):
    """Reverse iterator for books."""

    def __init__(self, books: List[Book]) -> None:
        self.books = books
        self.index = len(books) - 1

    def has_next(self) -> bool:
        return self.index >= 0

    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books in reverse")
        book = self.books[self.index]
        self.index -= 1
        return book

    def reset(self) -> None:
        self.index = len(self.books) - 1


class FilteredBookIterator(Iterator[Book]):
    """Iterator that returns only books matching criteria."""

    def __init__(self, books: List[Book], **criteria) -> None:
        """
        Initialize with books and filter criteria.
        
        Usage:
            iterator = FilteredBookIterator(books, genre="Science Fiction", year=2020)
        """
        self.books = books
        self.criteria = criteria
        self.index = 0
        self._find_next_valid()

    def _find_next_valid(self) -> None:
        """Find next book matching criteria."""
        while self.index < len(self.books):
            if self.books[self.index].matches_criteria(**self.criteria):
                break
            self.index += 1

    def has_next(self) -> bool:
        return self.index < len(self.books)

    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books matching criteria")
        book = self.books[self.index]
        self.index += 1
        self._find_next_valid()
        return book

    def reset(self) -> None:
        self.index = 0
        self._find_next_valid()


class BookCollection(Iterable[Book]):
    """Collection of books supporting multiple iteration strategies."""

    def __init__(self) -> None:
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        """Add a book to the collection."""
        self.books.append(book)

    def remove_book(self, book: Book) -> None:
        """Remove a book from the collection."""
        if book in self.books:
            self.books.remove(book)

    def create_iterator(self) -> Iterator[Book]:
        """Create a forward iterator."""
        return BookIterator(self.books)

    def create_reverse_iterator(self) -> Iterator[Book]:
        """Create a reverse iterator."""
        return ReverseBookIterator(self.books)

    def create_filtered_iterator(self, **criteria) -> Iterator[Book]:
        """
        Create a filtered iterator.
        
        Args:
            **criteria: Filtering criteria (genre="Science Fiction", author="Asimov", etc.)
        """
        return FilteredBookIterator(self.books, **criteria)

    def get_books_by_genre(self, genre: str) -> List[Book]:
        """Get all books of a specific genre."""
        return [book for book in self.books if book.genre.lower() == genre.lower()]

    def get_books_by_author(self, author: str) -> List[Book]:
        """Get all books by a specific author."""
        iterator = self.create_filtered_iterator(author=author)
        results = []
        while iterator.has_next():
            results.append(iterator.next())
        return results

    def get_all_books(self) -> List[Book]:
        """Get all books as a list."""
        return self.books.copy()

    def __len__(self) -> int:
        return len(self.books)


def demonstrate_book_collection() -> None:
    """Demonstrate the book collection iterator in action."""
    
    # Create a collection
    library = BookCollection()
    
    # Add books
    books = [
        Book("Foundation", "Isaac Asimov", 1951, 255, "Science Fiction"),
        Book("I, Robot", "Isaac Asimov", 1950, 224, "Science Fiction"),
        Book("The Expanse", "James S.A. Corey", 2011, 561, "Science Fiction"),
        Book("Dune", "Frank Herbert", 1965, 682, "Science Fiction"),
        Book("1984", "George Orwell", 1949, 328, "Dystopian"),
        Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 180, "Classic"),
    ]
    
    for book in books:
        library.add_book(book)
    
    print("=== Book Collection Iterator Demo ===\n")
    
    # Forward iteration
    print("All books (forward):")
    iterator = library.create_iterator()
    count = 0
    while iterator.has_next():
        print(f"  {count + 1}. {iterator.next()}")
        count += 1
    
    # Reverse iteration
    print("\nAll books (reverse):")
    reverse_iter = library.create_reverse_iterator()
    count = 0
    while reverse_iter.has_next():
        print(f"  {count + 1}. {reverse_iter.next()}")
        count += 1
    
    # Filtered iteration
    print("\nScience Fiction books:")
    sci_fi_iter = library.create_filtered_iterator(genre="Science Fiction")
    count = 0
    while sci_fi_iter.has_next():
        print(f"  {count + 1}. {sci_fi_iter.next()}")
        count += 1
    
    # Books by author
    print("\nBooks by Isaac Asimov:")
    asimov_books = library.get_books_by_author("Isaac Asimov")
    for i, book in enumerate(asimov_books, 1):
        print(f"  {i}. {book}")
    
    # Statistics
    print(f"\nTotal books: {len(library)}")
    print(f"Science Fiction books: {len(library.get_books_by_genre('Science Fiction'))}")
