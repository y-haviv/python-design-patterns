"""Tests for Facade Pattern."""
import pytest
from .pattern import (
    Subsystem1, Subsystem2, Facade,
    RepositoryFacade, OrderFacade
)


class TestBasicFacade:
    def test_facade_simplifies_interface(self):
        sub1 = Subsystem1()
        sub2 = Subsystem2()
        facade = Facade(sub1, sub2)
        
        result = facade.operation()
        assert "Subsystem1" in result
        assert "Subsystem2" in result


class TestRepositoryFacade:
    def test_get_user(self):
        repo = RepositoryFacade()
        user = repo.get_user(1)
        assert user["id"] == 1

    def test_create_user(self):
        repo = RepositoryFacade()
        user = repo.create_user("Alice")
        assert user["name"] == "Alice"


class TestOrderFacade:
    def test_place_order(self):
        facade = OrderFacade()
        result = facade.place_order("user@email.com", "item_1", 99.99)
        assert result["status"] == "confirmed"

    def test_cancel_order(self):
        facade = OrderFacade()
        result = facade.cancel_order("order_1", "item_1", 99.99)
        assert result["status"] == "cancelled"

