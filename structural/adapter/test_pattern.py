"""
Comprehensive tests for the Adapter Pattern.

These tests verify:
1. Basic adapter functionality with single adaptee.
2. Two-way adapter capabilities.
3. Multiple adaptees with different adapters.
4. Adapter with validation and transformation.
5. Real-world payment processing scenario.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Target,
    Adaptee,
    Adapter,
    TwoWayAdapter,
    LegacySystem,
    LegacySystemAdapter,
    AdapterWithValidation,
    AdapterRegistry,
)
from .real_world_example import (
    PaymentProcessor,
    StripePaymentGateway,
    PayPalPaymentGateway,
    StripeAdapter,
    PayPalAdapter,
    PaymentSystem,
)


class TestBasicAdapter:
    """Tests for basic Adapter functionality."""

    def test_adapter_converts_interface(self) -> None:
        """Verify adapter converts incompatible interface."""
        adaptee = Adaptee()
        adapter = Adapter(adaptee)

        result = adapter.request()

        assert isinstance(result, str)
        assert "Adapted response" in result

    def test_adapter_implements_target_interface(self) -> None:
        """Verify adapter is instance of Target."""
        adaptee = Adaptee()
        adapter = Adapter(adaptee)

        assert isinstance(adapter, Target)

    def test_adaptee_specific_interface(self) -> None:
        """Verify adaptee can still use its original interface."""
        adaptee = Adaptee()

        result = adaptee.specific_request()

        assert result == "Specific request from Adaptee"

    def test_adapter_accesses_adaptee_methods(self) -> None:
        """Verify adapter can access adaptee methods."""
        adaptee = Adaptee()
        adapter = Adapter(adaptee)

        adaptee_result = adapter.adaptee.specific_request()

        assert adaptee_result == "Specific request from Adaptee"


class TestTwoWayAdapter:
    """Tests for two-way adapter functionality."""

    def test_two_way_adapter_without_adaptee(self) -> None:
        """Verify two-way adapter works without adaptee."""
        adapter = TwoWayAdapter()

        result = adapter.request()

        assert result == "Default response"

    def test_two_way_adapter_with_adaptee(self) -> None:
        """Verify two-way adapter works with adaptee."""
        adaptee = Adaptee()
        adapter = TwoWayAdapter(adaptee)

        result = adapter.request()

        assert result == "Specific request from Adaptee"

    def test_set_adaptee_dynamically(self) -> None:
        """Verify adaptee can be set dynamically."""
        adapter = TwoWayAdapter()
        assert adapter.request() == "Default response"

        adaptee = Adaptee()
        adapter.set_adaptee(adaptee)

        assert adapter.request() == "Specific request from Adaptee"

    def test_get_adaptee_specific_request(self) -> None:
        """Verify getting adaptee-specific responses."""
        adaptee = Adaptee()
        adapter = TwoWayAdapter(adaptee)

        result = adapter.get_adaptee_specific_request()

        assert result == "Specific request from Adaptee"

    def test_get_adaptee_specific_request_no_adaptee(self) -> None:
        """Verify handling when adaptee is not set."""
        adapter = TwoWayAdapter()

        result = adapter.get_adaptee_specific_request()

        assert result == "No adaptee set"


class TestLegacySystemAdapter:
    """Tests for adapting legacy systems."""

    def test_legacy_system_direct_interface(self) -> None:
        """Verify legacy system can be used directly."""
        legacy = LegacySystem()

        result = legacy.get_information()

        assert "legacy system" in result

    def test_legacy_system_adapter(self) -> None:
        """Verify legacy system adapter converts interface."""
        legacy = LegacySystem()
        adapter = LegacySystemAdapter(legacy)

        result = adapter.request()

        assert isinstance(adapter, Target)
        assert "legacy system" in result
        assert "Operation 001" in result

    def test_legacy_system_adapter_integrates_results(self) -> None:
        """Verify adapter integrates multiple legacy method results."""
        legacy = LegacySystem()
        adapter = LegacySystemAdapter(legacy)

        result = adapter.request()

        # Should contain both pieces of information
        info = legacy.get_information()
        operation = legacy.execute_operation("OP001")

        assert info in result
        assert operation in result


class TestAdapterWithValidation:
    """Tests for adapter with validation and transformation."""

    def test_adapter_validates_data(self) -> None:
        """Verify adapter validates adapted data."""
        adaptee = Adaptee()
        adapter = AdapterWithValidation(adaptee)

        result = adapter.request()

        assert "Validated" in result or "Validation" in result

    def test_adapter_transformation(self) -> None:
        """Verify adapter transforms data."""
        adaptee = Adaptee()
        adapter = AdapterWithValidation(adaptee)

        result = adapter.request()

        # Should contain transformed (uppercase) data
        assert any(c.isupper() for c in result)

    def test_validation_errors_cleared(self) -> None:
        """Verify validation errors are cleared between calls."""
        adaptee = Adaptee()
        adapter = AdapterWithValidation(adaptee)

        adapter.request()
        errors_count_1 = len(adapter.validation_errors)

        adapter.request()
        errors_count_2 = len(adapter.validation_errors)

        # Errors should be the same (cleared between calls)
        assert errors_count_1 == errors_count_2


class TestAdapterRegistry:
    """Tests for adapter registry functionality."""

    def test_register_adapter(self) -> None:
        """Verify registering adapters."""
        registry = AdapterRegistry()

        registry.register_adapter("adaptee", Adapter)

        adapters = registry.get_registered_adapters()
        assert "adaptee" in adapters

    def test_create_adapter_from_registry(self) -> None:
        """Verify creating adapter from registry."""
        registry = AdapterRegistry()
        registry.register_adapter("adaptee", Adapter)

        adaptee = Adaptee()
        adapter = registry.create_adapter("adaptee", adaptee)

        assert isinstance(adapter, Target)

    def test_create_adapter_unregistered_type(self) -> None:
        """Verify error when creating unregistered adapter."""
        registry = AdapterRegistry()

        adaptee = Adaptee()
        with pytest.raises(ValueError):
            registry.create_adapter("unknown", adaptee)

    def test_register_multiple_adapters(self) -> None:
        """Verify registering multiple different adapters."""
        registry = AdapterRegistry()

        registry.register_adapter("type1", Adapter)
        registry.register_adapter("type2", TwoWayAdapter)
        registry.register_adapter("type3", LegacySystemAdapter)

        adapters = registry.get_registered_adapters()
        assert len(adapters) == 3
        assert "type1" in adapters
        assert "type2" in adapters
        assert "type3" in adapters


class TestStripeAdapter:
    """Tests for Stripe payment adapter."""

    def test_stripe_adapter_process_payment(self) -> None:
        """Verify Stripe adapter processes payments."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        result = adapter.process_payment(100.0, "customer_1", "Test payment")

        assert result["success"]
        assert result["amount"] == 100.0
        assert result["provider"] == "stripe"
        assert "transaction_id" in result

    def test_stripe_adapter_get_transaction_status(self) -> None:
        """Verify Stripe adapter gets transaction status."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        payment_result = adapter.process_payment(50.0, "customer_2", "Status test")
        transaction_id = payment_result["transaction_id"]

        status = adapter.get_transaction_status(transaction_id)

        assert status == "completed"

    def test_stripe_adapter_refund(self) -> None:
        """Verify Stripe adapter refunds payments."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        payment_result = adapter.process_payment(75.0, "customer_3", "Refund test")
        transaction_id = payment_result["transaction_id"]

        refund_result = adapter.refund_payment(transaction_id)

        assert refund_result["success"]
        assert "refund_id" in refund_result

    def test_stripe_adapter_converts_currency(self) -> None:
        """Verify Stripe adapter converts dollars to cents."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        adapter.process_payment(10.0, "customer_4", "Currency test")

        # Check that Stripe received amount in cents
        transactions = stripe.transactions
        for tx_id, tx in transactions.items():
            assert tx["amount_cents"] == 1000  # 10 dollars = 1000 cents


class TestPayPalAdapter:
    """Tests for PayPal payment adapter."""

    def test_paypal_adapter_process_payment(self) -> None:
        """Verify PayPal adapter processes payments."""
        paypal = PayPalPaymentGateway("client_id", "client_secret")
        adapter = PayPalAdapter(paypal)

        result = adapter.process_payment(100.0, "customer_1", "Test payment")

        assert result["success"]
        assert result["amount"] == 100.0
        assert result["provider"] == "paypal"
        assert "transaction_id" in result

    def test_paypal_adapter_get_transaction_status(self) -> None:
        """Verify PayPal adapter gets transaction status."""
        paypal = PayPalPaymentGateway("client_id", "client_secret")
        adapter = PayPalAdapter(paypal)

        payment_result = adapter.process_payment(50.0, "customer_2", "Status test")
        transaction_id = payment_result["transaction_id"]

        status = adapter.get_transaction_status(transaction_id)

        assert status == "completed"

    def test_paypal_adapter_refund(self) -> None:
        """Verify PayPal adapter refunds payments."""
        paypal = PayPalPaymentGateway("client_id", "client_secret")
        adapter = PayPalAdapter(paypal)

        payment_result = adapter.process_payment(75.0, "customer_3", "Refund test")
        transaction_id = payment_result["transaction_id"]

        refund_result = adapter.refund_payment(transaction_id)

        assert refund_result["success"]
        assert "refund_id" in refund_result


class TestPaymentSystem:
    """Tests for payment system using adapters."""

    def test_payment_system_with_stripe(self) -> None:
        """Verify payment system works with Stripe adapter."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        system = PaymentSystem()
        system.set_payment_processor(adapter)

        success = system.process_order_payment("order_1", 100.0, "customer_1", "Test")

        assert success
        assert "order_1" in system.transactions

    def test_payment_system_with_paypal(self) -> None:
        """Verify payment system works with PayPal adapter."""
        paypal = PayPalPaymentGateway("client_id", "client_secret")
        adapter = PayPalAdapter(paypal)

        system = PaymentSystem()
        system.set_payment_processor(adapter)

        success = system.process_order_payment("order_2", 75.0, "customer_2", "Test")

        assert success
        assert "order_2" in system.transactions

    def test_payment_system_check_status(self) -> None:
        """Verify payment system can check payment status."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        system = PaymentSystem()
        system.set_payment_processor(adapter)

        system.process_order_payment("order_3", 50.0, "customer_3", "Test")

        status = system.check_payment_status("order_3")

        assert status == "completed"

    def test_payment_system_refund(self) -> None:
        """Verify payment system can refund orders."""
        stripe = StripePaymentGateway("test_key")
        adapter = StripeAdapter(stripe)

        system = PaymentSystem()
        system.set_payment_processor(adapter)

        system.process_order_payment("order_4", 100.0, "customer_4", "Test")
        success = system.refund_order("order_4")

        assert success
        assert system.transactions["order_4"]["status"] == "refunded"

    def test_payment_system_switch_providers(self) -> None:
        """Verify payment system can switch between providers."""
        stripe = StripePaymentGateway("test_key")
        paypal = PayPalPaymentGateway("client_id", "client_secret")

        system = PaymentSystem()

        # Process with Stripe
        system.set_payment_processor(StripeAdapter(stripe))
        system.process_order_payment("order_5", 100.0, "customer_5", "Stripe")

        # Switch to PayPal
        system.set_payment_processor(PayPalAdapter(paypal))
        system.process_order_payment("order_6", 100.0, "customer_6", "PayPal")

        assert system.transactions["order_5"]["provider"] == "stripe"
        assert system.transactions["order_6"]["provider"] == "paypal"

    def test_payment_system_without_processor_raises_error(self) -> None:
        """Verify system raises error without processor."""
        system = PaymentSystem()

        with pytest.raises(RuntimeError):
            system.process_order_payment("order_7", 100.0, "customer_7", "Test")

