"""
Singleton Pattern
================

Ensures a class has only one instance and provides a global point of access to it.

Included in this package:
- SingletonMeta: The core metaclass for enforcing singleton behavior.
- AppSettings: A basic usage example for global configurations.
- FeatureFlagService: A complex, real-world scenario for shared state.
"""

from .pattern import SingletonMeta, AppSettings
from .real_world_example import FeatureFlagService

__all__ = ["SingletonMeta", "AppSettings", "FeatureFlagService"]