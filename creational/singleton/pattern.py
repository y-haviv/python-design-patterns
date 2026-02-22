"""
Thread-safe Singleton pattern implementation using a metaclass.

This module provides a robust, reusable metaclass to enforce the Singleton 
pattern across any class. It ensures that only one instance of a class 
exists in a multi-threaded environment.
"""

from __future__ import annotations
from threading import Lock
from typing import Any, Dict, Optional


class SingletonMeta(type):
    """
    A thread-safe implementation of a Singleton Metaclass.
    
    In Python, the most 'elegant' way to implement a Singleton is via a 
    metaclass, as it encapsulates the creation logic and keeps the 
    business logic of the subclass clean.

    Attributes:
        _instances (Dict[type, Any]): A dictionary mapping classes to 
            their unique instances.
        _lock (Lock): A primitive lock to prevent multiple threads from 
            instantiating the singleton simultaneously.
    """

    _instances: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Check if an instance exists. If not, create one under a thread lock.
        
        This uses the 'Double-Checked Locking' optimization to avoid 
        locking overhead on every call once the instance is created.
        """
        if cls not in cls._instances:
            with cls._lock:
                # Double-check to handle the race condition
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class AppSettings(metaclass=SingletonMeta):
    """
    Example: Global Application Settings.
    
    Demonstrates how to use SingletonMeta to store global configuration 
    that should be consistent across all modules.
    """

    def __init__(self) -> None:
        self._settings: Dict[str, Any] = {
            "environment": "development",
            "version": "1.0.0",
            "log_level": "INFO"
        }

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Retrieve a setting value."""
        return self._settings.get(key, default)

    def update_setting(self, key: str, value: Any) -> None:
        """Update a setting value."""
        self._settings[key] = value


def reset_singletons() -> None:
    """
    Clears all cached singleton instances.
    
    Warning:
        This is primarily for testing purposes (Unit Tests) to ensure 
        that tests remain isolated and do not leak state to each other.
    """
    with SingletonMeta._lock:
        SingletonMeta._instances.clear()