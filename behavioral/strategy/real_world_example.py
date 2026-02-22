"""
Real-World Example: Payment Processing with Multiple Strategies.

Demonstrates how different payment methods can be processed using
different strategies, allowing clients to choose at runtime.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta


class PaymentStrategy(ABC):
    """
    Abstract payment strategy that defines interface for payment methods.
    
    Different payment methods implement this interface, allowing
    payment processing to use different strategies.
    """

    @abstractmethod
    def validate_payment_details(self) -> bool:
        """Validate payment details."""
        pass

    @abstractmethod
    def process_payment(self, amount: float) -> Dict[str, Any]:
        """Process a payment."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Refund a previous payment."""
        pass

    @abstractmethod
    def get_payment_method_name(self) -> str:
        """Get the name of this payment method."""
        pass


class CreditCardStrategy(PaymentStrategy):
    """
    Concrete strategy for credit card payments.
    
    Implements credit card specific payment processing logic.
    """

    def __init__(
        self, card_number: str, expiry: str, cvv: str, cardholder: str
    ) -> None:
        """
        Initialize credit card details.
        
        Args:
            card_number: 16-digit card number.
            expiry: Expiry date (MM/YY format).
            cvv: 3-digit CVV.
            cardholder: Cardholder name.
        """
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv
        self.cardholder = cardholder
        self.transaction_history: List[Dict[str, Any]] = []

    def validate_payment_details(self) -> bool:
        """Validate credit card details."""
        # Simple validation
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            print("  ✗ Invalid card number")
            return False
        
        if len(self.cvv) != 3 or not self.cvv.isdigit():
            print("  ✗ Invalid CVV")
            return False
        
        # Check expiry
        month, year = map(int, self.expiry.split('/'))
        today = datetime.now()
        expiry_date = datetime(2000 + year, month, 1)
        
        if expiry_date < today:
            print("  ✗ Card expired")
            return False
        
        print("  ✓ Card details valid")
        return True

    def process_payment(self, amount: float) -> Dict[str, Any]:
        """Process credit card payment."""
        if not self.validate_payment_details():
            return {
                "success": False,
                "message": "Payment validation failed",
                "transaction_id": None,
            }
        
        transaction_id = f"CC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fee = amount * 0.025  # 2.5% processing fee
        total = amount + fee
        
        transaction = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "transaction_id": transaction_id,
            "type": "payment",
            "amount": amount,
            "fee": fee,
            "total": total,
            "status": "completed",
        }
        self.transaction_history.append(transaction)
        
        print(f"  ✓ Credit card payment processed")
        print(f"    Amount: ${amount:.2f}")
        print(f"    Fee: ${fee:.2f}")
        print(f"    Total: ${total:.2f}")
        print(f"    Transaction ID: {transaction_id}")
        
        return {
            "success": True,
            "message": "Payment processed successfully",
            "transaction_id": transaction_id,
            "total_charged": total,
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Refund a credit card charge."""
        refund_id = f"REF-{transaction_id}"
        
        refund = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "original_transaction": transaction_id,
            "refund_id": refund_id,
            "type": "refund",
            "amount": amount,
            "status": "completed",
        }
        self.transaction_history.append(refund)
        
        print(f"  ✓ Credit card refund processed")
        print(f"    Original Transaction: {transaction_id}")
        print(f"    Refund Amount: ${amount:.2f}")
        print(f"    Refund ID: {refund_id}")
        
        return {
            "success": True,
            "message": "Refund processed successfully",
            "refund_id": refund_id,
            "refunded_amount": amount,
        }

    def get_payment_method_name(self) -> str:
        """Get payment method name."""
        return "Credit Card"


class PayPalStrategy(PaymentStrategy):
    """
    Concrete strategy for PayPal payments.
    
    Implements PayPal specific payment processing logic.
    """

    def __init__(self, email: str, password: str) -> None:
        """
        Initialize PayPal credentials.
        
        Args:
            email: PayPal account email.
            password: PayPal password.
        """
        self.email = email
        self.password = password
        self.authenticated = False
        self.transaction_history: List[Dict[str, Any]] = []

    def validate_payment_details(self) -> bool:
        """Validate PayPal credentials."""
        if not self.email or "@" not in self.email:
            print("  ✗ Invalid PayPal email")
            return False
        
        if not self.password or len(self.password) < 6:
            print("  ✗ Invalid PayPal password")
            return False
        
        # Simulate authentication
        self.authenticated = True
        print("  ✓ PayPal credentials authenticated")
        return True

    def process_payment(self, amount: float) -> Dict[str, Any]:
        """Process PayPal payment."""
        if not self.validate_payment_details():
            return {
                "success": False,
                "message": "PayPal authentication failed",
                "transaction_id": None,
            }
        
        transaction_id = f"PP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fee = amount * 0.015  # 1.5% processing fee
        total = amount + fee
        
        transaction = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "transaction_id": transaction_id,
            "type": "payment",
            "amount": amount,
            "fee": fee,
            "total": total,
            "status": "completed",
        }
        self.transaction_history.append(transaction)
        
        print(f"  ✓ PayPal payment processed")
        print(f"    Amount: ${amount:.2f}")
        print(f"    Fee: ${fee:.2f}")
        print(f"    Total: ${total:.2f}")
        print(f"    Transaction ID: {transaction_id}")
        
        return {
            "success": True,
            "message": "Payment processed via PayPal",
            "transaction_id": transaction_id,
            "total_charged": total,
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Refund a PayPal payment."""
        refund_id = f"REF-{transaction_id}"
        
        refund = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "original_transaction": transaction_id,
            "refund_id": refund_id,
            "type": "refund",
            "amount": amount,
            "status": "completed",
        }
        self.transaction_history.append(refund)
        
        print(f"  ✓ PayPal refund processed")
        print(f"    Original Transaction: {transaction_id}")
        print(f"    Refund Amount: ${amount:.2f}")
        print(f"    Refund ID: {refund_id}")
        
        return {
            "success": True,
            "message": "Refund processed via PayPal",
            "refund_id": refund_id,
            "refunded_amount": amount,
        }

    def get_payment_method_name(self) -> str:
        """Get payment method name."""
        return "PayPal"


class CryptocurrencyStrategy(PaymentStrategy):
    """
    Concrete strategy for cryptocurrency payments.
    
    Implements cryptocurrency specific payment processing logic.
    """

    def __init__(self, wallet_address: str, currency: str = "BTC") -> None:
        """
        Initialize cryptocurrency wallet.
        
        Args:
            wallet_address: Wallet address.
            currency: Cryptocurrency type (BTC, ETH, etc.).
        """
        self.wallet_address = wallet_address
        self.currency = currency
        self.transaction_history: List[Dict[str, Any]] = []

    def validate_payment_details(self) -> bool:
        """Validate cryptocurrency wallet."""
        if not self.wallet_address or len(self.wallet_address) < 26:
            print(f"  ✗ Invalid {self.currency} wallet address")
            return False
        
        if self.currency not in ["BTC", "ETH", "XRP", "LTC"]:
            print(f"  ✗ Unsupported cryptocurrency: {self.currency}")
            return False
        
        print(f"  ✓ {self.currency} wallet validated")
        return True

    def process_payment(self, amount: float) -> Dict[str, Any]:
        """Process cryptocurrency payment."""
        if not self.validate_payment_details():
            return {
                "success": False,
                "message": "Cryptocurrency validation failed",
                "transaction_id": None,
            }
        
        transaction_id = f"CRYPTO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine crypto amount and fees based on current rates (simplified)
        rate = {"BTC": 0.000025, "ETH": 0.0005, "XRP": 0.02, "LTC": 0.001}
        crypto_amount = amount * rate.get(self.currency, 0.0001)
        fee = crypto_amount * 0.001  # 0.1% network fee
        
        transaction = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "transaction_id": transaction_id,
            "type": "payment",
            "usd_amount": amount,
            "crypto_amount": crypto_amount,
            "currency": self.currency,
            "fee": fee,
            "status": "pending_confirmation",
        }
        self.transaction_history.append(transaction)
        
        print(f"  ✓ Cryptocurrency payment initiated")
        print(f"    USD Amount: ${amount:.2f}")
        print(f"    Crypto Amount: {crypto_amount:.8f} {self.currency}")
        print(f"    Network Fee: {fee:.8f} {self.currency}")
        print(f"    Transaction ID: {transaction_id}")
        print(f"    Status: Awaiting blockchain confirmation")
        
        return {
            "success": True,
            "message": f"Payment initiated via {self.currency}",
            "transaction_id": transaction_id,
            "crypto_amount": crypto_amount,
            "status": "pending_confirmation",
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Refund a cryptocurrency payment."""
        refund_id = f"REF-{transaction_id}"
        
        refund = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "original_transaction": transaction_id,
            "refund_id": refund_id,
            "type": "refund",
            "usd_amount": amount,
            "status": "pending_confirmation",
        }
        self.transaction_history.append(refund)
        
        print(f"  ✓ Cryptocurrency refund initiated")
        print(f"    Original Transaction: {transaction_id}")
        print(f"    Refund Amount: ${amount:.2f}")
        print(f"    Refund ID: {refund_id}")
        
        return {
            "success": True,
            "message": "Refund initiated on blockchain",
            "refund_id": refund_id,
            "refunded_amount": amount,
            "status": "pending_confirmation",
        }

    def get_payment_method_name(self) -> str:
        """Get payment method name."""
        return f"Cryptocurrency ({self.currency})"


class PaymentProcessor:
    """
    Payment processor that uses payment strategies.
    
    Allows clients to choose different payment methods at runtime.
    """

    def __init__(self, strategy: PaymentStrategy) -> None:
        """
        Initialize processor with payment strategy.
        
        Args:
            strategy: The payment strategy to use.
        """
        self._strategy = strategy
        self.transaction_log: List[Dict[str, Any]] = []

    def set_payment_method(self, strategy: PaymentStrategy) -> None:
        """
        Change payment method.
        
        Args:
            strategy: The new payment strategy.
        """
        print(f"\n[Processor] Switching to {strategy.get_payment_method_name()}")
        self._strategy = strategy

    def pay(self, amount: float) -> bool:
        """
        Process payment using current strategy.
        
        Args:
            amount: Amount to charge.
            
        Returns:
            True if payment was successful.
        """
        print(f"\n[Processor] Processing payment: ${amount:.2f}")
        print(f"           Method: {self._strategy.get_payment_method_name()}")
        
        result = self._strategy.process_payment(amount)
        
        if result["success"]:
            self.transaction_log.append({
                "timestamp": datetime.now(),
                "method": self._strategy.get_payment_method_name(),
                "amount": amount,
                "status": "success",
                "transaction_id": result.get("transaction_id"),
            })
        
        return result["success"]

    def refund(self, transaction_id: str, amount: float) -> bool:
        """
        Process refund using current strategy.
        
        Args:
            transaction_id: ID of transaction to refund.
            amount: Refund amount.
            
        Returns:
            True if refund was successful.
        """
        print(f"\n[Processor] Processing refund: ${amount:.2f}")
        print(f"           Method: {self._strategy.get_payment_method_name()}")
        
        result = self._strategy.refund(transaction_id, amount)
        
        if result["success"]:
            self.transaction_log.append({
                "timestamp": datetime.now(),
                "method": self._strategy.get_payment_method_name(),
                "amount": -amount,
                "status": "refund",
                "refund_id": result.get("refund_id"),
            })
        
        return result["success"]

    def get_transaction_count(self) -> int:
        """Get number of transactions processed."""
        return len(self.transaction_log)


class ShoppingCart:
    """
    Shopping cart that uses payment strategy for checkout.
    
    Demonstrates practical use of strategy pattern in e-commerce.
    """

    def __init__(self) -> None:
        """Initialize shopping cart."""
        self.items: List[Dict[str, Any]] = []
        self.payment_processor: Optional[PaymentProcessor] = None

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """
        Add item to cart.
        
        Args:
            name: Item name.
            price: Price per unit.
            quantity: Quantity to add.
        """
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "subtotal": price * quantity,
        })
        print(f"  Added: {quantity}x {name} @ ${price:.2f}")

    def get_total(self) -> float:
        """Calculate cart total."""
        return sum(item["subtotal"] for item in self.items)

    def set_payment_method(self, strategy: PaymentStrategy) -> None:
        """
        Set payment method.
        
        Args:
            strategy: Payment strategy to use.
        """
        self.payment_processor = PaymentProcessor(strategy)
        print(f"  Payment method set to: {strategy.get_payment_method_name()}")

    def checkout(self) -> bool:
        """
        Checkout using selected payment method.
        
        Returns:
            True if checkout was successful.
        """
        if not self.payment_processor:
            print("  ✗ No payment method set")
            return False
        
        total = self.get_total()
        print(f"\n=== Checkout ===")
        print(f"  Items in cart: {len(self.items)}")
        print(f"  Total: ${total:.2f}")
        
        return self.payment_processor.pay(total)

    def display_cart(self) -> None:
        """Display cart contents."""
        print("\n=== Shopping Cart ===")
        if not self.items:
            print("  (empty)")
            return
        
        for item in self.items:
            print(
                f"  {item['quantity']}x {item['name']} "
                f"@ ${item['price']:.2f} = ${item['subtotal']:.2f}"
            )
        
        print(f"  Total: ${self.get_total():.2f}")
