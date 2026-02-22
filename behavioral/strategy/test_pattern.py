"""
Comprehensive tests for the Strategy Pattern.

These tests verify:
1. Strategy switching and execution.
2. Multiple concrete strategies.
3. Context-strategy interaction.
4. Real-world payment processing.
5. Execution logging and history.
"""

from __future__ import annotations
import pytest
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


class TestContextStrategy:
    """Tests for context-strategy interaction."""

    def test_context_with_strategy_a(self) -> None:
        """Verify context works with Strategy A."""
        strategy = ConcreteStrategyA()
        context = Context(strategy)
        
        assert context.get_strategy_name() == "Strategy A (Reverse/Double)"

    def test_context_with_strategy_b(self) -> None:
        """Verify context works with Strategy B."""
        strategy = ConcreteStrategyB()
        context = Context(strategy)
        
        assert context.get_strategy_name() == "Strategy B (Sort/Square)"

    def test_context_with_strategy_c(self) -> None:
        """Verify context works with Strategy C."""
        strategy = ConcreteStrategyC()
        context = Context(strategy)
        
        assert context.get_strategy_name() == "Strategy C (Unique/Abs)"

    def test_execute_strategy(self) -> None:
        """Verify executing a strategy."""
        strategy = ConcreteStrategyA()
        context = Context(strategy)
        
        result = context.execute_strategy([1, 2, 3])
        
        assert result == [3, 2, 1]

    def test_switch_strategy(self) -> None:
        """Verify switching strategies at runtime."""
        context = Context(ConcreteStrategyA())
        
        assert context.get_strategy_name() == "Strategy A (Reverse/Double)"
        
        context.set_strategy(ConcreteStrategyB())
        
        assert context.get_strategy_name() == "Strategy B (Sort/Square)"

    def test_strategies_produce_different_results(self) -> None:
        """Verify different strategies produce different results."""
        data = [3, 1, 2]
        
        context_a = Context(ConcreteStrategyA())
        context_b = Context(ConcreteStrategyB())
        context_c = Context(ConcreteStrategyC())
        
        result_a = context_a.execute_strategy(data)
        result_b = context_b.execute_strategy(data)
        result_c = context_c.execute_strategy(data)
        
        assert result_a == [2, 1, 3]
        assert result_b == [1, 2, 3]
        # Result C would be unordered set converted to list

    def test_strategy_with_string_data(self) -> None:
        """Verify strategies work with string data."""
        data = "hello"
        
        context_a = Context(ConcreteStrategyA())
        result_a = context_a.execute_strategy(data)
        
        assert result_a == "olleh"

    def test_strategy_with_numeric_data(self) -> None:
        """Verify strategies work with numeric data."""
        data = 5
        
        context_a = Context(ConcreteStrategyA())
        result_a = context_a.execute_strategy(data)
        
        assert result_a == 10

    def test_execution_log(self) -> None:
        """Verify execution is logged."""
        context = Context(ConcreteStrategyA())
        
        context.execute_strategy([1, 2])
        context.execute_strategy("abc")
        
        log = context.get_execution_log()
        assert len(log) == 2
        assert log[0]["strategy"] == "Strategy A (Reverse/Double)"

    def test_strategy_descriptions(self) -> None:
        """Verify strategies have descriptions."""
        strategy_a = ConcreteStrategyA()
        strategy_b = ConcreteStrategyB()
        strategy_c = ConcreteStrategyC()
        
        assert "Reverse" in strategy_a.describe()
        assert "Sort" in strategy_b.describe()
        assert "Unique" in strategy_c.describe()

    def test_get_strategy_returns_current(self) -> None:
        """Verify getting current strategy."""
        strategy = ConcreteStrategyB()
        context = Context(strategy)
        
        assert context.get_strategy() is strategy


class TestPaymentStrategies:
    """Tests for payment processing strategies."""

    def test_credit_card_validation(self) -> None:
        """Verify credit card validation."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        
        assert card.validate_payment_details() is True

    def test_credit_card_invalid_number(self) -> None:
        """Verify credit card rejects invalid number."""
        card = CreditCardStrategy("123", "12/25", "123", "John Doe")
        
        assert card.validate_payment_details() is False

    def test_credit_card_invalid_cvv(self) -> None:
        """Verify credit card rejects invalid CVV."""
        card = CreditCardStrategy("1234567890123456", "12/25", "12", "John Doe")
        
        assert card.validate_payment_details() is False

    def test_credit_card_payment(self) -> None:
        """Verify credit card payment processing."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        
        result = card.process_payment(100.0)
        
        assert result["success"] is True
        assert "transaction_id" in result
        assert result["total_charged"] > 100.0  # Includes fee

    def test_credit_card_refund(self) -> None:
        """Verify credit card refund."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        
        payment = card.process_payment(100.0)
        refund = card.refund(payment["transaction_id"], 100.0)
        
        assert refund["success"] is True
        assert refund["refunded_amount"] == 100.0

    def test_paypal_validation(self) -> None:
        """Verify PayPal validation."""
        paypal = PayPalStrategy("user@example.com", "password123")
        
        assert paypal.validate_payment_details() is True

    def test_paypal_invalid_email(self) -> None:
        """Verify PayPal rejects invalid email."""
        paypal = PayPalStrategy("invalid", "password123")
        
        assert paypal.validate_payment_details() is False

    def test_paypal_invalid_password(self) -> None:
        """Verify PayPal rejects short password."""
        paypal = PayPalStrategy("user@example.com", "123")
        
        assert paypal.validate_payment_details() is False

    def test_paypal_payment(self) -> None:
        """Verify PayPal payment processing."""
        paypal = PayPalStrategy("user@example.com", "password123")
        
        result = paypal.process_payment(100.0)
        
        assert result["success"] is True
        assert "transaction_id" in result

    def test_paypal_refund(self) -> None:
        """Verify PayPal refund."""
        paypal = PayPalStrategy("user@example.com", "password123")
        
        payment = paypal.process_payment(100.0)
        refund = paypal.refund(payment["transaction_id"], 100.0)
        
        assert refund["success"] is True

    def test_cryptocurrency_validation(self) -> None:
        """Verify cryptocurrency validation."""
        crypto = CryptocurrencyStrategy(
            "1A1z7agoat2YLZW51Yz8aS1UNvXLoVUUwt", "BTC"
        )
        
        assert crypto.validate_payment_details() is True

    def test_cryptocurrency_invalid_wallet(self) -> None:
        """Verify cryptocurrency rejects invalid wallet."""
        crypto = CryptocurrencyStrategy("short", "BTC")
        
        assert crypto.validate_payment_details() is False

    def test_cryptocurrency_unsupported_currency(self) -> None:
        """Verify cryptocurrency rejects unsupported currency."""
        crypto = CryptocurrencyStrategy(
            "1A1z7agoat2YLZW51Yz8aS1UNvXLoVUUwt", "INVALID"
        )
        
        assert crypto.validate_payment_details() is False

    def test_cryptocurrency_payment(self) -> None:
        """Verify cryptocurrency payment processing."""
        crypto = CryptocurrencyStrategy(
            "1A1z7agoat2YLZW51Yz8aS1UNvXLoVUUwt", "BTC"
        )
        
        result = crypto.process_payment(100.0)
        
        assert result["success"] is True
        assert "crypto_amount" in result
        assert result["status"] == "pending_confirmation"

    def test_payment_processor_with_credit_card(self) -> None:
        """Verify payment processor with credit card."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        processor = PaymentProcessor(card)
        
        result = processor.pay(100.0)
        
        assert result is True
        assert processor.get_transaction_count() == 1

    def test_payment_processor_switch_method(self) -> None:
        """Verify switching payment methods."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        paypal = PayPalStrategy("user@example.com", "password123")
        
        processor = PaymentProcessor(card)
        processor.pay(100.0)
        
        processor.set_payment_method(paypal)
        processor.pay(50.0)
        
        assert processor.get_transaction_count() == 2

    def test_payment_processor_refund(self) -> None:
        """Verify payment processor refund."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        processor = PaymentProcessor(card)
        
        payment_result = processor.pay(100.0)
        # Get transaction ID from the payment
        payment = card.process_payment(100.0)
        
        refund_result = processor.refund(payment["transaction_id"], 100.0)
        
        assert refund_result is True

    def test_shopping_cart_empty(self) -> None:
        """Verify empty shopping cart."""
        cart = ShoppingCart()
        
        assert cart.get_total() == 0.0

    def test_shopping_cart_add_items(self) -> None:
        """Verify adding items to cart."""
        cart = ShoppingCart()
        
        cart.add_item("Widget", 10.0, 2)
        cart.add_item("Gadget", 25.0, 1)
        
        assert cart.get_total() == 45.0

    def test_shopping_cart_checkout_no_payment(self) -> None:
        """Verify cart checkout without payment method fails."""
        cart = ShoppingCart()
        cart.add_item("Widget", 10.0, 1)
        
        result = cart.checkout()
        
        assert result is False

    def test_shopping_cart_checkout_with_credit_card(self) -> None:
        """Verify cart checkout with credit card."""
        cart = ShoppingCart()
        cart.add_item("Widget", 10.0, 1)
        
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        cart.set_payment_method(card)
        
        result = cart.checkout()
        
        assert result is True

    def test_shopping_cart_checkout_with_paypal(self) -> None:
        """Verify cart checkout with PayPal."""
        cart = ShoppingCart()
        cart.add_item("Widget", 10.0, 1)
        
        paypal = PayPalStrategy("user@example.com", "password123")
        cart.set_payment_method(paypal)
        
        result = cart.checkout()
        
        assert result is True

    def test_shopping_cart_checkout_with_crypto(self) -> None:
        """Verify cart checkout with cryptocurrency."""
        cart = ShoppingCart()
        cart.add_item("Widget", 10.0, 1)
        
        crypto = CryptocurrencyStrategy(
            "1A1z7agoat2YLZW51Yz8aS1UNvXLoVUUwt", "BTC"
        )
        cart.set_payment_method(crypto)
        
        result = cart.checkout()
        
        assert result is True

    def test_payment_method_names(self) -> None:
        """Verify payment method names."""
        card = CreditCardStrategy("1234567890123456", "12/25", "123", "John Doe")
        paypal = PayPalStrategy("user@example.com", "password123")
        crypto = CryptocurrencyStrategy(
            "1A1z7agoat2YLZW51Yz8aS1UNvXLoVUUwt", "BTC"
        )
        
        assert "Credit Card" in card.get_payment_method_name()
        assert "PayPal" in paypal.get_payment_method_name()
        assert "BTC" in crypto.get_payment_method_name()
