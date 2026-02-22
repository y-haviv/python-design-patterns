"""
Comprehensive tests for the Observer Pattern.

These tests verify:
1. Observer attachment and detachment.
2. Subject state changes and notifications.
3. Observer update mechanism.
4. Multiple observers and concurrent updates.
5. Real-world stock market scenario.
"""

from __future__ import annotations
import pytest
from .pattern import (
    Observer,
    Subject,
    ConcreteObserver,
    ConcreteSubject,
)
from .real_world_example import (
    Stock,
    Investor,
    StockMarket,
)


class TestConcreteSubjectObserver:
    """Tests for basic subject-observer functionality."""

    def test_attach_observer(self) -> None:
        """Verify attaching observers to a subject."""
        subject = ConcreteSubject("TestSubject", "initial")
        observer1 = ConcreteObserver("Observer1", subject)
        observer2 = ConcreteObserver("Observer2", subject)
        
        subject.attach(observer1)
        subject.attach(observer2)
        
        assert subject.get_observer_count() == 2
        assert observer1 in subject.get_observers()
        assert observer2 in subject.get_observers()

    def test_detach_observer(self) -> None:
        """Verify detaching observers from a subject."""
        subject = ConcreteSubject("TestSubject", "initial")
        observer1 = ConcreteObserver("Observer1", subject)
        observer2 = ConcreteObserver("Observer2", subject)
        
        subject.attach(observer1)
        subject.attach(observer2)
        subject.detach(observer1)
        
        assert subject.get_observer_count() == 1
        assert observer1 not in subject.get_observers()
        assert observer2 in subject.get_observers()

    def test_no_duplicate_observers(self) -> None:
        """Verify that the same observer cannot be attached twice."""
        subject = ConcreteSubject("TestSubject", "initial")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.attach(observer)
        
        assert subject.get_observer_count() == 1

    def test_set_state_notifies_observers(self) -> None:
        """Verify that setting state notifies all observers."""
        subject = ConcreteSubject("TestSubject", "initial")
        observer1 = ConcreteObserver("Observer1", subject)
        observer2 = ConcreteObserver("Observer2", subject)
        
        subject.attach(observer1)
        subject.attach(observer2)
        
        subject.set_state("updated")
        
        assert observer1.update_count == 1
        assert observer2.update_count == 1
        assert observer1.subject_state == "updated"
        assert observer2.subject_state == "updated"

    def test_no_notification_on_same_state(self) -> None:
        """Verify that setting the same state does not trigger notifications."""
        subject = ConcreteSubject("TestSubject", "state1")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.set_state("state1")
        
        assert observer.update_count == 0

    def test_multiple_state_changes(self) -> None:
        """Verify multiple state changes trigger multiple notifications."""
        subject = ConcreteSubject("TestSubject", "state1")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        
        subject.set_state("state2")
        subject.set_state("state3")
        subject.set_state("state4")
        
        assert observer.update_count == 3
        assert observer.subject_state == "state4"

    def test_observer_receives_extra_info(self) -> None:
        """Verify observers receive extra information with updates."""
        subject = ConcreteSubject("TestSubject", "initial")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.set_state("updated")
        
        last_update = observer.get_last_update()
        assert last_update is not None
        assert last_update["extra_info"]["old_state"] == "initial"
        assert last_update["extra_info"]["new_state"] == "updated"

    def test_state_change_log(self) -> None:
        """Verify subject maintains a log of state changes."""
        subject = ConcreteSubject("TestSubject", "state1")
        
        subject.set_state("state2")
        subject.set_state("state3")
        
        log = subject.get_state_change_log()
        assert len(log) == 2
        assert log[0]["state"] == "state2"
        assert log[1]["state"] == "state3"


class TestStockObserver:
    """Tests for stock market observer pattern."""

    def test_investor_watches_stock(self) -> None:
        """Verify investor can watch a stock."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        
        investor.watch_stock(stock)
        
        assert "AAPL" in investor.watched_stocks
        assert stock.get_observer_count() == 1

    def test_investor_stops_watching(self) -> None:
        """Verify investor can stop watching a stock."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        
        investor.watch_stock(stock)
        investor.stop_watching(stock)
        
        assert "AAPL" not in investor.watched_stocks
        assert stock.get_observer_count() == 0

    def test_multiple_investors_watch_same_stock(self) -> None:
        """Verify multiple investors can watch the same stock."""
        stock = Stock("AAPL", 150.0)
        investor1 = Investor("John")
        investor2 = Investor("Jane")
        
        investor1.watch_stock(stock)
        investor2.watch_stock(stock)
        
        assert stock.get_observer_count() == 2

    def test_stock_price_change_notifies_investors(self) -> None:
        """Verify stock price changes notify investors."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        
        investor.watch_stock(stock)
        stock.set_price(155.0)
        
        assert stock.get_price() == 155.0

    def test_investor_buys_stock(self) -> None:
        """Verify investor can buy shares."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        investor.buy(stock, 10, 150.0)
        
        assert "AAPL" in investor.portfolio
        assert investor.portfolio["AAPL"]["quantity"] == 10
        assert investor.portfolio["AAPL"]["total_invested"] == 1500.0

    def test_investor_sells_stock(self) -> None:
        """Verify investor can sell shares."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        investor.buy(stock, 10, 150.0)
        investor.sell(stock, 5, 160.0)
        
        assert investor.portfolio["AAPL"]["quantity"] == 5
        assert len(investor.transaction_log) == 2

    def test_investor_cannot_sell_unowned_shares(self) -> None:
        """Verify investor cannot sell shares they don't own."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        
        investor.sell(stock, 10, 150.0)
        
        assert "AAPL" not in investor.portfolio

    def test_investor_cannot_sell_more_than_owned(self) -> None:
        """Verify investor cannot sell more shares than they own."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        investor.buy(stock, 5, 150.0)
        investor.sell(stock, 10, 160.0)
        
        assert investor.portfolio["AAPL"]["quantity"] == 5

    def test_stock_price_history(self) -> None:
        """Verify stock maintains price change history."""
        stock = Stock("AAPL", 150.0)
        
        stock.set_price(155.0)
        stock.set_price(160.0)
        
        history = stock.price_history
        assert len(history) >= 3  # Initial + 2 updates
        assert history[-2]["price"] == 155.0
        assert history[-1]["price"] == 160.0

    def test_stock_market_functionality(self) -> None:
        """Verify stock market manages stocks and investors."""
        market = StockMarket("NYSE")
        
        aapl = market.add_stock("AAPL", 150.0)
        googl = market.add_stock("GOOGL", 140.0)
        
        assert market.get_stock("AAPL") is aapl
        assert market.get_stock("GOOGL") is googl

    def test_stock_market_update_price(self) -> None:
        """Verify stock market can update prices."""
        market = StockMarket("NYSE")
        market.add_stock("AAPL", 150.0)
        
        market.update_price("AAPL", 155.0)
        
        assert market.get_stock("AAPL").get_price() == 155.0

    def test_portfolio_value_calculation(self) -> None:
        """Verify portfolio value is calculated correctly."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        investor.buy(stock, 10, 150.0)
        assert investor.get_portfolio_value() == 1500.0
        
        stock.set_price(160.0)
        assert investor.get_portfolio_value() == 1600.0

    def test_average_cost_calculation(self) -> None:
        """Verify average cost basis is calculated correctly."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        investor.buy(stock, 10, 150.0)
        investor.buy(stock, 5, 160.0)
        
        portfolio_entry = investor.portfolio["AAPL"]
        expected_avg = (10 * 150.0 + 5 * 160.0) / 15
        assert abs(portfolio_entry["average_cost"] - expected_avg) < 0.01

    def test_investor_trading_strategy(self) -> None:
        """Verify investor's trading strategy triggers on price changes."""
        stock = Stock("AAPL", 150.0)
        investor = Investor("John")
        investor.watch_stock(stock)
        
        # Initial purchase on dip
        stock.set_price(145.0)
        
        # Should trigger buying after significant dip
        assert len(investor.transaction_log) > 0

    def test_observer_update_history(self) -> None:
        """Verify observer maintains update history."""
        subject = ConcreteSubject("TestSubject", "state1")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.set_state("state2")
        subject.set_state("state3")
        
        history = observer.update_history
        assert len(history) == 2
        assert history[0]["state"] == "state2"
        assert history[1]["state"] == "state3"

    def test_get_last_update(self) -> None:
        """Verify getting last update information."""
        subject = ConcreteSubject("TestSubject", "state1")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.set_state("state2")
        
        last_update = observer.get_last_update()
        assert last_update is not None
        assert last_update["update_count"] == 1
        assert last_update["state"] == "state2"

    def test_no_update_after_detach(self) -> None:
        """Verify detached observers don't receive updates."""
        subject = ConcreteSubject("TestSubject", "state1")
        observer = ConcreteObserver("Observer", subject)
        
        subject.attach(observer)
        subject.detach(observer)
        subject.set_state("state2")
        
        assert observer.update_count == 0
