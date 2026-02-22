"""
Comprehensive tests for the Singleton pattern.

These tests verify:
1. Instance identity (always the same object).
2. Thread-safety during concurrent instantiation.
3. Proper behavior of real-world examples (FeatureFlagService).
4. Isolation between tests using the reset hook.
"""

from __future__ import annotations
import threading
from typing import List
import pytest
from .pattern import AppSettings, reset_singletons
from .real_world_example import FeatureFlagService


@pytest.fixture(autouse=True)
def _clean_singleton_state():
    """
    Fixture to ensure a clean state before and after each test.
    This prevents state leakage between unrelated test cases.
    """
    reset_singletons()
    yield
    reset_singletons()


def test_singleton_identity():
    """Verify that multiple calls return the exact same instance."""
    app_settings_1 = AppSettings()
    app_settings_2 = AppSettings()
    
    assert app_settings_1 is app_settings_2
    assert id(app_settings_1) == id(app_settings_2)


def test_state_consistency():
    """Verify that changes in one reference reflect in all others."""
    s1 = AppSettings()
    s1.update_setting("api_key", "secret_123")
    
    s2 = AppSettings()
    assert s2.get_setting("api_key") == "secret_123"


def test_thread_safety_high_concurrency():
    """
    Stress test for thread safety.
    We spawn 50 threads to instantiate the service simultaneously.
    Only one instance must ever be created.
    """
    instances: List[FeatureFlagService] = []
    start_event = threading.Event()

    def create_instance():
        # Wait for the signal to ensure all threads hit the constructor at once
        start_event.wait()
        instances.append(FeatureFlagService())

    threads = [threading.Thread(target=create_instance) for _ in range(50)]
    
    for t in threads:
        t.start()
        
    # 'Bang!' - Release all threads at the same time
    start_event.set()
    
    for t in threads:
        t.join()

    # All instances in the list should be the exact same object
    assert all(inst is instances[0] for inst in instances)
    assert len(set(id(inst) for inst in instances)) == 1


def test_feature_flag_logic():
    """Verify business logic within a Singleton instance."""
    service = FeatureFlagService({"ai_enabled": True})
    assert service.is_enabled("ai_enabled") is True
    
    service.set_flag("ai_enabled", False)
    # Check via a new 'reference'
    assert FeatureFlagService().is_enabled("ai_enabled") is False