"""Facade Pattern Implementation (Structural)."""

from typing import List, Dict, Optional


class Subsystem1:
    def operation_a(self) -> str:
        return "Subsystem1: Ready!"

    def operation_b(self) -> str:
        return "Subsystem1: Go!"


class Subsystem2:
    def operation_a(self) -> str:
        return "Subsystem2: Get ready."

    def operation_b(self) -> str:
        return "Subsystem2: Fire!"


class Facade:
    """Simplified interface to complex subsystems."""

    def __init__(self, subsystem1: Subsystem1, subsystem2: Subsystem2):
        self._subsystem1 = subsystem1
        self._subsystem2 = subsystem2

    def operation(self) -> str:
        results = []
        results.append("Facade initializes subsystems:")
        results.append(self._subsystem1.operation_a())
        results.append(self._subsystem2.operation_a())
        results.append("Facade orders subsystems to work:")
        results.append(self._subsystem1.operation_b())
        results.append(self._subsystem2.operation_b())
        return "\n".join(results)


class DatabaseConnection:
    def connect(self) -> str:
        return "✓ Connected to database"

    def disconnect(self) -> str:
        return "✓ Disconnected from database"

    def query(self, sql: str) -> str:
        return f"✓ Executed: {sql}"


class CacheManager:
    def __init__(self):
        self.cache: Dict = {}

    def put(self, key: str, value: str) -> str:
        self.cache[key] = value
        return f"✓ Cached: {key}"

    def get(self, key: str) -> Optional[str]:
        return self.cache.get(key)

    def clear(self) -> str:
        self.cache.clear()
        return "✓ Cache cleared"


class LogManager:
    def __init__(self):
        self.logs: List[str] = []

    def log(self, message: str) -> None:
        self.logs.append(message)

    def get_logs(self) -> List[str]:
        return self.logs.copy()


class RepositoryFacade:
    """Facade for database, cache, and logging."""

    def __init__(self):
        self._db = DatabaseConnection()
        self._cache = CacheManager()
        self._logger = LogManager()

    def get_user(self, user_id: int) -> Dict:
        cache_key = f"user_{user_id}"
        self._logger.log(f"Getting user {user_id}")

        if cache_key in self._cache.cache:
            self._logger.log("Retrieved from cache")
            return self._cache.get(cache_key)

        self._logger.log("Querying database")
        result = {"id": user_id, "name": "User"}
        self._cache.put(cache_key, str(result))
        return result

    def create_user(self, name: str) -> Dict:
        self._logger.log(f"Creating user: {name}")
        user = {"id": 1, "name": name}
        self._cache.clear()
        return user


class PaymentGateway:
    def authorize(self, amount: float) -> str:
        return f"✓ Authorized: ${amount}"

    def capture(self, transaction_id: str) -> str:
        return f"✓ Captured transaction: {transaction_id}"

    def refund(self, transaction_id: str) -> str:
        return f"✓ Refunded transaction: {transaction_id}"


class NotificationService:
    def send_email(self, to: str, subject: str) -> str:
        return f"✓ Email sent to {to}: {subject}"

    def send_sms(self, phone: str, message: str) -> str:
        return f"✓ SMS sent to {phone}: {message}"


class InventoryService:
    def __init__(self):
        self.items: Dict[str, int] = {}

    def reserve(self, item_id: str, quantity: int) -> bool:
        if item_id not in self.items:
            self.items[item_id] = 100
        self.items[item_id] -= quantity
        return True

    def release(self, item_id: str, quantity: int) -> bool:
        self.items[item_id] += quantity
        return True


class OrderFacade:
    """Facade for order processing."""

    def __init__(self):
        self._payment = PaymentGateway()
        self._notification = NotificationService()
        self._inventory = InventoryService()

    def place_order(self, customer_email: str, item_id: str, amount: float) -> Dict:
        """Place an order - handles all subsystems."""
        self._notification.send_email(customer_email, "Order received")
        self._payment.authorize(amount)
        self._inventory.reserve(item_id, 1)

        return {
            "status": "confirmed",
            "email": customer_email,
            "amount": amount
        }

    def cancel_order(self, order_id: str, item_id: str, amount: float, customer_email: str) -> Dict:
        """Cancel an order - handles all subsystems."""
        self._inventory.release(item_id, 1)
        self._payment.refund(order_id)
        self._notification.send_email(customer_email, f"Order {order_id} cancelled. Refunded: ${amount}")

        return {
            "status": "cancelled",
            "refunded_amount": amount
        }


