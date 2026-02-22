"""
Real-World Example: Stock Price Updates.

Demonstrates how multiple investors can observe and react to changes
in stock prices without the stock needing to know about them directly.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any
from datetime import datetime
from .pattern import Subject, Observer


class Stock(Subject):
    """
    Represents a stock whose price is observed by investors.
    
    When the stock price changes, all investors are automatically
    notified about the price update.
    """

    def __init__(self, symbol: str, initial_price: float) -> None:
        """
        Initialize a stock.
        
        Args:
            symbol: Stock ticker symbol (e.g., "AAPL").
            initial_price: Initial price of the stock.
        """
        self.symbol = symbol
        self._price = initial_price
        self._observers: List[Observer] = []
        self.price_history: List[Dict[str, Any]] = []
        self._record_price_change(initial_price, "initialization")

    def _record_price_change(
        self, price: float, reason: str = "update"
    ) -> None:
        """Record the price change in history."""
        self.price_history.append({
            "price": price,
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "reason": reason,
            "observer_count": len(self._observers),
        })

    def attach(self, investor: Observer) -> None:
        """
        Attach an investor to observe this stock.
        
        Args:
            investor: The investor to notify on price changes.
        """
        if investor not in self._observers:
            self._observers.append(investor)
            print(f"[Stock({self.symbol})] Investor attached")

    def detach(self, investor: Observer) -> None:
        """
        Detach an investor from this stock.
        
        Args:
            investor: The investor to stop notifying.
        """
        if investor in self._observers:
            self._observers.remove(investor)
            print(f"[Stock({self.symbol})] Investor detached")

    def set_price(self, new_price: float) -> None:
        """
        Update the stock price and notify investors.
        
        Args:
            new_price: The new stock price.
        """
        if self._price != new_price:
            old_price = self._price
            change_amount = new_price - old_price
            change_percent = (change_amount / old_price * 100) if old_price else 0
            
            self._price = new_price
            self._record_price_change(new_price, "price_update")
            
            print(
                f"\n[Stock({self.symbol})] Price update: "
                f"${old_price:.2f} → ${new_price:.2f} "
                f"(${change_amount:+.2f}, {change_percent:+.2f}%)"
            )
            
            self.notify(
                old_price=old_price,
                new_price=new_price,
                change=change_amount,
                change_percent=change_percent,
            )

    def get_price(self) -> float:
        """Get the current stock price."""
        return self._price

    def get_state(self) -> float:
        """Get the current state (price) of the stock."""
        return self._price

    def notify(self, **kwargs) -> None:
        """Notify all investors about the price change."""
        print(f"Notifying {len(self._observers)} investor(s)...")
        for observer in self._observers:
            observer.update(self, **kwargs)


class Investor(Observer):
    """
    Represents an investor who observes stock prices.
    
    Investors are notified whenever a stock they're watching
    changes price, allowing them to react accordingly.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize an investor.
        
        Args:
            name: Name of the investor.
        """
        self.name = name
        self.watched_stocks: Dict[str, Stock] = {}
        self.portfolio: Dict[str, Dict[str, Any]] = {}
        self.transaction_log: List[Dict[str, Any]] = []

    def watch_stock(self, stock: Stock) -> None:
        """
        Start watching a stock for price changes.
        
        Args:
            stock: The stock to watch.
        """
        if stock.symbol not in self.watched_stocks:
            self.watched_stocks[stock.symbol] = stock
            stock.attach(self)
            print(f"[Investor({self.name})] Now watching {stock.symbol}")

    def stop_watching(self, stock: Stock) -> None:
        """
        Stop watching a stock.
        
        Args:
            stock: The stock to stop watching.
        """
        if stock.symbol in self.watched_stocks:
            del self.watched_stocks[stock.symbol]
            stock.detach(self)
            print(f"[Investor({self.name})] Stopped watching {stock.symbol}")

    def buy(
        self, stock: Stock, quantity: int, price: float
    ) -> None:
        """
        Buy shares of a stock.
        
        Args:
            stock: The stock to buy.
            quantity: Number of shares to buy.
            price: Price per share.
        """
        symbol = stock.symbol
        cost = quantity * price
        
        if symbol not in self.portfolio:
            self.portfolio[symbol] = {
                "quantity": 0,
                "total_invested": 0.0,
                "average_cost": 0.0,
            }
        
        portfolio_entry = self.portfolio[symbol]
        current_quantity = portfolio_entry["quantity"]
        current_invested = portfolio_entry["total_invested"]
        
        new_quantity = current_quantity + quantity
        new_invested = current_invested + cost
        new_average = new_invested / new_quantity
        
        portfolio_entry["quantity"] = new_quantity
        portfolio_entry["total_invested"] = new_invested
        portfolio_entry["average_cost"] = new_average
        
        self.transaction_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "action": "BUY",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total": cost,
        })
        
        print(
            f"  ↳ [Investor({self.name})] BOUGHT {quantity} × "
            f"{symbol} @ ${price:.2f}"
        )

    def sell(
        self, stock: Stock, quantity: int, price: float
    ) -> None:
        """
        Sell shares of a stock.
        
        Args:
            stock: The stock to sell.
            quantity: Number of shares to sell.
            price: Price per share.
        """
        symbol = stock.symbol
        
        if symbol not in self.portfolio:
            print(f"  ↳ [Investor({self.name})] Cannot sell - no shares of {symbol}")
            return
        
        portfolio_entry = self.portfolio[symbol]
        if portfolio_entry["quantity"] < quantity:
            print(
                f"  ↳ [Investor({self.name})] Cannot sell {quantity} shares "
                f"- only own {portfolio_entry['quantity']}"
            )
            return
        
        revenue = quantity * price
        cost_basis = quantity * portfolio_entry["average_cost"]
        profit = revenue - cost_basis
        
        portfolio_entry["quantity"] -= quantity
        portfolio_entry["total_invested"] -= cost_basis
        
        if portfolio_entry["quantity"] == 0:
            del self.portfolio[symbol]
        
        self.transaction_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "action": "SELL",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total": revenue,
            "profit": profit,
        })
        
        print(
            f"  ↳ [Investor({self.name})] SOLD {quantity} × {symbol} @ "
            f"${price:.2f} (Profit: ${profit:+.2f})"
        )

    def update(self, stock: Stock, **kwargs) -> None:
        """
        React to stock price changes.
        
        Args:
            stock: The stock that changed.
            **kwargs: Information about the price change.
        """
        new_price = kwargs.get("new_price")
        change_percent = kwargs.get("change_percent", 0)
        
        # Simple trading strategy: buy on dips, sell on rallies
        if "quantity" in self.portfolio.get(stock.symbol, {}):
            holding_quantity = self.portfolio[stock.symbol]["quantity"]
            
            if change_percent < -2:  # Price dropped more than 2%
                # Buying opportunity - buy 10 shares
                self.buy(stock, 10, new_price)
            elif change_percent > 5:  # Price increased more than 5%
                # Selling opportunity - sell 25% of holdings
                if holding_quantity > 0:
                    sell_quantity = int(holding_quantity * 0.25)
                    if sell_quantity > 0:
                        self.sell(stock, sell_quantity, new_price)
        else:
            # Don't hold shares yet
            if change_percent < -3:  # Significant dip
                # Initial purchase - buy 20 shares
                self.buy(stock, 20, new_price)

    def get_portfolio_value(self) -> float:
        """Calculate total portfolio value based on current prices."""
        total = 0.0
        for symbol, data in self.portfolio.items():
            if symbol in self.watched_stocks:
                price = self.watched_stocks[symbol].get_price()
                total += data["quantity"] * price
        return total

    def display_portfolio(self) -> None:
        """Display the investor's current portfolio."""
        print(f"\n=== Portfolio for {self.name} ===")
        if not self.portfolio:
            print("  (empty)")
            return
        
        total_value = 0.0
        for symbol, data in self.portfolio.items():
            quantity = data["quantity"]
            avg_cost = data["average_cost"]
            if symbol in self.watched_stocks:
                current_price = self.watched_stocks[symbol].get_price()
                position_value = quantity * current_price
                gain_loss = (current_price - avg_cost) * quantity
                gain_loss_pct = ((current_price - avg_cost) / avg_cost * 100)
                
                total_value += position_value
                print(
                    f"  {symbol}: {quantity} shares @ ${avg_cost:.2f} avg, "
                    f"current ${current_price:.2f}, value ${position_value:.2f} "
                    f"(Gain/Loss: ${gain_loss:+.2f} {gain_loss_pct:+.2f}%)"
                )
        
        print(f"  Total Portfolio Value: ${total_value:.2f}")


class StockMarket:
    """
    Central market that manages stocks and investors.
    
    Provides a convenient interface for market operations and
    demonstrates the observer pattern in action.
    """

    def __init__(self, name: str = "Stock Market") -> None:
        """
        Initialize the stock market.
        
        Args:
            name: Name of the market.
        """
        self.name = name
        self.stocks: Dict[str, Stock] = {}
        self.investors: List[Investor] = []

    def add_stock(self, symbol: str, initial_price: float) -> Stock:
        """
        Add a stock to the market.
        
        Args:
            symbol: Stock ticker symbol.
            initial_price: Initial price of the stock.
            
        Returns:
            The created Stock object.
        """
        stock = Stock(symbol, initial_price)
        self.stocks[symbol] = stock
        print(f"[Market] Added stock {symbol} @ ${initial_price:.2f}")
        return stock

    def get_stock(self, symbol: str) -> Optional[Stock]:
        """Get a stock by its symbol."""
        return self.stocks.get(symbol)

    def register_investor(self, investor: Investor) -> None:
        """Register an investor with the market."""
        if investor not in self.investors:
            self.investors.append(investor)
            print(f"[Market] Registered investor: {investor.name}")

    def update_price(self, symbol: str, new_price: float) -> None:
        """
        Update a stock's price.
        
        Args:
            symbol: Stock ticker symbol.
            new_price: New price for the stock.
        """
        if symbol in self.stocks:
            self.stocks[symbol].set_price(new_price)

    def display_market_summary(self) -> None:
        """Display summary of all stocks in the market."""
        print(f"\n=== {self.name} Summary ===")
        for symbol, stock in self.stocks.items():
            observer_count = len(stock._observers)
            print(f"  {symbol}: ${stock.get_price():.2f} "
                  f"({observer_count} investors watching)")
