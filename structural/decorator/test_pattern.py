"""Tests for Decorator Pattern."""
import pytest
from .pattern import (
    ConcreteComponent, ConcreteDecoratorA, ConcreteDecoratorB,
    FileDataSource, EncryptionDecorator, CompressionDecorator, LoggingDecorator,
    SimpleCoffee, MilkDecorator, SugarDecorator, CoffeeBuilder,
    SimpleWidget, BorderDecorator, ScrollDecorator
)


class TestBasicDecorator:
    def test_decorator_adds_behavior(self):
        component = ConcreteComponent()
        assert component.operation() == "ConcreteComponent"
        
        decorated = ConcreteDecoratorA(component)
        assert "ConcreteDecoratorA" in decorated.operation()

    def test_multiple_decorators(self):
        component = ConcreteComponent()
        decorated = ConcreteDecoratorA(ConcreteDecoratorB(component))
        result = decorated.operation()
        assert "ConcreteDecoratorA" in result
        assert "ConcreteDecoratorB" in result


class TestDataSourceDecorator:
    def test_encryption_decorator(self):
        source = FileDataSource("test.txt")
        encrypted = EncryptionDecorator(source)
        
        encrypted.write_data("hello")
        result = encrypted.read_data()
        assert result == "hello"

    def test_compression_decorator(self):
        source = FileDataSource("test.txt")
        compressed = CompressionDecorator(source)
        
        compressed.write_data("hello world")
        result = compressed.read_data()
        assert result == "helloworld"

    def test_logging_decorator(self):
        source = FileDataSource("test.txt")
        logged = LoggingDecorator(source)
        
        logged.write_data("data")
        logged.read_data()
        
        log = logged.get_log()
        assert len(log) == 2


class TestCoffeeDecorator:
    def test_simple_coffee(self):
        coffee = SimpleCoffee()
        assert coffee.get_cost() == 2.0
        assert "Simple" in coffee.get_description()

    def test_coffee_with_milk(self):
        coffee = SimpleCoffee()
        milk_coffee = MilkDecorator(coffee)
        assert milk_coffee.get_cost() == 2.5
        assert "Milk" in milk_coffee.get_description()

    def test_multiple_decorators(self):
        coffee = SimpleCoffee()
        coffee = MilkDecorator(coffee)
        coffee = SugarDecorator(coffee)
        
        assert coffee.get_cost() == 2.75
        assert "Milk" in coffee.get_description()
        assert "Sugar" in coffee.get_description()

    def test_coffee_builder(self):
        coffee = (CoffeeBuilder()
                  .add_milk()
                  .add_sugar()
                  .build())
        
        assert coffee.get_cost() == 2.75


class TestWidgetDecorator:
    def test_widget_with_border(self):
        widget = SimpleWidget("Text")
        bordered = BorderDecorator(widget)
        
        assert "+----+" in bordered.render()

    def test_widget_with_multiple_decorators(self):
        widget = SimpleWidget("Text")
        widget = BorderDecorator(widget)
        widget = ScrollDecorator(widget)
        
        result = widget.render()
        assert "[" in result
        assert "]" in result


