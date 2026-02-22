"""Proxy Pattern Implementation (Structural)."""

from typing import Any, Optional
from abc import ABC, abstractmethod


class Subject(ABC):
    """Subject interface."""

    @abstractmethod
    def request(self) -> str:
        pass


class RealSubject(Subject):
    """Real subject - the actual object."""

    def request(self) -> str:
        return "RealSubject: Handling request."


class Proxy(Subject):
    """Proxy - controls access to real subject."""

    def __init__(self, real_subject: RealSubject):
        self._real_subject = real_subject

    def request(self) -> str:
        if self._check_access():
            result = self._real_subject.request()
            return f"Proxy: {result}"
        return "Proxy: Access denied"

    def _check_access(self) -> bool:
        print("Proxy: Checking access...")
        return True


class Image(ABC):
    """Abstract Image interface."""

    @abstractmethod
    def display(self) -> str:
        pass


class RealImage(Image):
    """Real image - loads image data."""

    def __init__(self, filename: str):
        self.filename = filename
        self._load_image()

    def _load_image(self) -> None:
        print(f"Loading image: {self.filename}")

    def display(self) -> str:
        return f"Displaying {self.filename}"


class ImageProxy(Image):
    """Proxy for lazy loading."""

    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[RealImage] = None

    def display(self) -> str:
        if not self._real_image:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()


class Database(ABC):
    """Abstract database interface."""

    @abstractmethod
    def query(self, sql: str) -> str:
        pass


class RealDatabase(Database):
    """Real database connection."""

    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


class DatabaseProxy(Database):
    """Proxy with caching."""

    def __init__(self):
        self._real_db = RealDatabase()
        self._cache = {}

    def query(self, sql: str) -> str:
        if sql in self._cache:
            return f"(Cached) {self._cache[sql]}"
        
        result = self._real_db.query(sql)
        self._cache[sql] = result
        return result


class Service(ABC):
    """Abstract service."""

    @abstractmethod
    def operation(self, data: str) -> str:
        pass


class RealService(Service):
    """Real expensive service."""

    def operation(self, data: str) -> str:
        return f"Service processed: {data}"


class ProtectionProxy(Service):
    """Proxy with authentication."""

    def __init__(self, real_service: RealService, user_role: str = "guest"):
        self._service = real_service
        self._user_role = user_role

    def operation(self, data: str) -> str:
        if not self._has_access():
            return "Access denied: insufficient permissions"
        return self._service.operation(data)

    def _has_access(self) -> bool:
        return self._user_role in ["admin", "user"]


class DataValidator:
    """Validates data."""

    @staticmethod
    def is_valid(data: str) -> bool:
        return len(data) > 0


class ValidationProxy(Service):
    """Proxy with validation."""

    def __init__(self, real_service: RealService):
        self._service = real_service

    def operation(self, data: str) -> str:
        if not DataValidator.is_valid(data):
            return "Invalid data"
        return self._service.operation(data)


class LoggingProxy(Service):
    """Proxy with logging."""

    def __init__(self, real_service: RealService):
        self._service = real_service
        self._log = []

    def operation(self, data: str) -> str:
        self._log.append(f"Operation called with: {data}")
        return self._service.operation(data)

    def get_log(self):
        return self._log


