"""
Strategy Pattern (Behavioral)

Define a family of algorithms, encapsulate each one, and make them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.
"""

from .pattern import (
    ConcreteStrategyA,
    ConcreteStrategyB,
    ConcreteStrategyC,
    Context,
    Strategy,
)
from .real_world_example import (
    CreditCardStrategy,
    CryptocurrencyStrategy,
    PaymentProcessor,
    PayPalStrategy,
    ShoppingCart,
)

__all__ = [
    "ConcreteStrategyA",
    "ConcreteStrategyB",
    "ConcreteStrategyC",
    "Context",
    "CreditCardStrategy",
    "CryptocurrencyStrategy",
    "PayPalStrategy",
    "PaymentProcessor",
    "ShoppingCart",
    "Strategy",
]
