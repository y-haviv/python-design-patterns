"""
Strategy Pattern (Behavioral)

Define a family of algorithms, encapsulate each one, and make them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.
"""

from .pattern import (
    Strategy,
    Context,
    ConcreteStrategyA,
    ConcreteStrategyB,
    ConcreteStrategyC,
)
from .real_world_example import (
    PaymentProcessor,
    CreditCardStrategy,
    PayPalStrategy,
    CryptocurrencyStrategy,
    ShoppingCart,
)

__all__ = [
    "Strategy",
    "Context",
    "ConcreteStrategyA",
    "ConcreteStrategyB",
    "ConcreteStrategyC",
    "PaymentProcessor",
    "CreditCardStrategy",
    "PayPalStrategy",
    "CryptocurrencyStrategy",
    "ShoppingCart",
]
