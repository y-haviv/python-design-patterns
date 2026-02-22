"""
Real-World Example: Payment Processing System Integration.

This example demonstrates the Adapter pattern in a practical scenario:
integrating multiple payment processors with different APIs into a 
unified payment system.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class PaymentProcessor(ABC):
    """
    Target interface - the standard payment processor interface 
    our application expects.
    """

    @abstractmethod
    def process_payment(
        self, amount: float, customer_id: str, description: str
    ) -> Dict[str, Any]:
        """Process a payment and return transaction result."""
        pass

    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        """Get the status of a transaction."""
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        """Refund a payment."""
        pass


class StripePaymentGateway:
    """
    Adaptee - third-party Stripe payment API with different interface.
    
    This represents a real-world payment gateway with its own API 
    that doesn't match our PaymentProcessor interface.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize Stripe gateway with API key."""
        self.api_key = api_key
        self.transactions: Dict[str, Dict[str, Any]] = {}

    def charge_card(
        self, amount_cents: int, card_token: str, description: str
    ) -> Dict[str, Any]:
        """
        Charge a card using Stripe API.
        
        Note: Stripe uses cents, not dollars, and different parameter names.
        """
        transaction_id = f"stripe_{datetime.now().timestamp()}"
        self.transactions[transaction_id] = {
            "amount_cents": amount_cents,
            "card": card_token,
            "description": description,
            "status": "succeeded",
            "timestamp": datetime.now().isoformat(),
        }
        return {
            "id": transaction_id,
            "object": "charge",
            "amount": amount_cents,
            "status": "succeeded",
        }

    def get_charge_status(self, charge_id: str) -> str:
        """Get Stripe charge status."""
        if charge_id in self.transactions:
            return self.transactions[charge_id]["status"]
        return "unknown"

    def refund_charge(self, charge_id: str) -> Dict[str, Any]:
        """Refund a Stripe charge."""
        if charge_id in self.transactions:
            self.transactions[charge_id]["status"] = "refunded"
            return {"id": charge_id, "object": "refund", "status": "succeeded"}
        return {"error": "Charge not found"}


class PayPalPaymentGateway:
    """
    Another Adaptee - PayPal API with its own different interface.
    
    Represents another real payment gateway that needs adaptation.
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Initialize PayPal gateway with credentials."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.payments: Dict[str, Dict[str, Any]] = {}

    def create_payment(
        self, total: str, currency: str, description: str
    ) -> Dict[str, Any]:
        """
        Create a PayPal payment.
        
        Note: PayPal uses different parameter names and structure.
        """
        payment_id = f"paypal_{datetime.now().timestamp()}"
        self.payments[payment_id] = {
            "total": float(total),
            "currency": currency,
            "description": description,
            "state": "approved",
            "create_time": datetime.now().isoformat(),
        }
        return {
            "id": payment_id,
            "state": "approved",
            "transactions": [{"amount": {"total": total, "currency": currency}}],
        }

    def get_payment_state(self, payment_id: str) -> str:
        """Get PayPal payment state."""
        if payment_id in self.payments:
            return self.payments[payment_id]["state"]
        return "unknown"

    def execute_refund(
        self, payment_id: str, refund_amount: str
    ) -> Dict[str, Any]:
        """Execute PayPal refund."""
        if payment_id in self.payments:
            self.payments[payment_id]["state"] = "refunded"
            return {
                "id": f"refund_{datetime.now().timestamp()}",
                "state": "completed",
            }
        return {"error": "Payment not found"}


class StripeAdapter(PaymentProcessor):
    """
    Adapter - makes Stripe API conform to PaymentProcessor interface.
    
    Translates PaymentProcessor method calls to Stripe API calls.
    """

    def __init__(self, stripe_gateway: StripePaymentGateway) -> None:
        """Initialize adapter with Stripe gateway."""
        self.stripe = stripe_gateway

    def process_payment(
        self, amount: float, customer_id: str, description: str
    ) -> Dict[str, Any]:
        """
        Process payment using Stripe.
        
        Adapts from standard interface (dollars) to Stripe interface (cents).
        """
        amount_cents = int(amount * 100)
        card_token = f"customer_{customer_id}"

        result = self.stripe.charge_card(amount_cents, card_token, description)

        return {
            "success": result["status"] == "succeeded",
            "transaction_id": result["id"],
            "amount": amount,
            "provider": "stripe",
            "timestamp": datetime.now().isoformat(),
        }

    def get_transaction_status(self, transaction_id: str) -> str:
        """Get transaction status from Stripe."""
        stripe_status = self.stripe.get_charge_status(transaction_id)

        # Normalize Stripe status to our standard
        status_map = {"succeeded": "completed", "failed": "failed", "unknown": "pending"}
        return status_map.get(stripe_status, "unknown")

    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        """Refund via Stripe."""
        result = self.stripe.refund_charge(transaction_id)

        return {
            "success": result.get("status") == "succeeded",
            "refund_id": result.get("id"),
            "timestamp": datetime.now().isoformat(),
        }


class PayPalAdapter(PaymentProcessor):
    """
    Adapter - makes PayPal API conform to PaymentProcessor interface.
    
    Translates PaymentProcessor method calls to PayPal API calls.
    """

    def __init__(self, paypal_gateway: PayPalPaymentGateway) -> None:
        """Initialize adapter with PayPal gateway."""
        self.paypal = paypal_gateway

    def process_payment(
        self, amount: float, customer_id: str, description: str
    ) -> Dict[str, Any]:
        """
        Process payment using PayPal.
        
        Adapts from standard interface to PayPal interface.
        """
        # PayPal expects string amounts and currency
        result = self.paypal.create_payment(str(amount), "USD", description)

        return {
            "success": result["state"] == "approved",
            "transaction_id": result["id"],
            "amount": amount,
            "provider": "paypal",
            "timestamp": datetime.now().isoformat(),
        }

    def get_transaction_status(self, transaction_id: str) -> str:
        """Get transaction status from PayPal."""
        paypal_state = self.paypal.get_payment_state(transaction_id)

        # Normalize PayPal state to our standard
        status_map = {"approved": "completed", "failed": "failed", "created": "pending"}
        return status_map.get(paypal_state, "unknown")

    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        """Refund via PayPal."""
        result = self.paypal.execute_refund(transaction_id, "0")

        return {
            "success": result.get("state") == "completed",
            "refund_id": result.get("id"),
            "timestamp": datetime.now().isoformat(),
        }


class PaymentSystem:
    """
    Client that uses adapters to work with multiple payment providers.
    
    This system doesn't need to know about different payment APIs—
    it just uses the unified PaymentProcessor interface.
    """

    def __init__(self) -> None:
        """Initialize the payment system."""
        self.processor: Optional[PaymentProcessor] = None
        self.transactions: Dict[str, Dict[str, Any]] = {}

    def set_payment_processor(self, processor: PaymentProcessor) -> None:
        """Set the payment processor to use."""
        self.processor = processor

    def process_order_payment(
        self, order_id: str, amount: float, customer_id: str, description: str
    ) -> bool:
        """Process payment for an order."""
        if not self.processor:
            raise RuntimeError("No payment processor configured")

        result = self.processor.process_payment(amount, customer_id, description)

        self.transactions[order_id] = {
            "amount": amount,
            "customer_id": customer_id,
            "transaction_id": result["transaction_id"],
            "status": "completed" if result["success"] else "failed",
            "provider": result["provider"],
        }

        return result["success"]

    def check_payment_status(self, order_id: str) -> str:
        """Check the status of a payment."""
        if order_id not in self.transactions:
            return "unknown"

        transaction = self.transactions[order_id]
        if not self.processor:
            return "unknown"

        return self.processor.get_transaction_status(transaction["transaction_id"])

    def refund_order(self, order_id: str) -> bool:
        """Refund payment for an order."""
        if order_id not in self.transactions or not self.processor:
            return False

        transaction = self.transactions[order_id]
        result = self.processor.refund_payment(transaction["transaction_id"])

        if result["success"]:
            transaction["status"] = "refunded"

        return result["success"]

    def get_transaction_details(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get transaction details."""
        return self.transactions.get(order_id)


