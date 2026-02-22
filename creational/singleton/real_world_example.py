"""
Real-world singleton: A Dynamic Feature Flag Service.

This service ensures a single source of truth for application behavior 
toggles, which is vital for canary releases or model A/B testing in 
production environments.
"""

from __future__ import annotations
from threading import Lock
from typing import Dict, Any, Mapping
from .pattern import SingletonMeta


class FeatureFlagService(metaclass=SingletonMeta):
    """
    Registry for feature flags that ensures data consistency across the app.
    
    This service is thread-safe and can be updated dynamically from 
    external loaders (e.g., JSON config, Remote API).
    """

    def __init__(self, initial_flags: Optional[Mapping[str, bool]] = None) -> None:
        # Note: __init__ will only be called once by the metaclass logic.
        self._flags: Dict[str, bool] = dict(initial_flags or {})
        self._lock = Lock()

    def is_enabled(self, flag: str) -> bool:
        """
        Check if a specific feature flag is enabled.
        
        Args:
            flag: The name of the feature to check.
            
        Returns:
            True if enabled, False otherwise.
        """
        return self._flags.get(flag, False)

    def set_flag(self, flag: str, enabled: bool) -> None:
        """Update a single flag's state safely."""
        with self._lock:
            self._flags[flag] = enabled

    def bulk_update(self, flags: Mapping[str, bool]) -> None:
        """Update multiple flags at once from a dictionary."""
        with self._lock:
            self._flags.update(flags)

    def all_flags(self) -> Dict[str, bool]:
        """Return a copy of the current flag state for inspection."""
        with self._lock:
            return dict(self._flags)


def load_flags_from_config() -> Dict[str, bool]:
    """
    Simulation of an external configuration loader.
    In a real scenario, this might read from a JSON file or a Consul KV store.
    """
    return {
        "use_new_ai_model": True,
        "enable_beta_ui": False,
        "performance_tracing": True
    }