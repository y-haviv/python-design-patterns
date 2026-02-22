"""
Strategy Pattern Implementation (Behavioral).

Define a family of algorithms, encapsulate each one, and make them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.

Key Components:
- Strategy: Declares interface common to all algorithms.
- ConcreteStrategy: Implements algorithm using the Strategy interface.
- Context: Uses a Strategy to execute an algorithm.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict
from datetime import datetime


class Strategy(ABC):
    """
    Abstract strategy that defines interface for algorithms.
    
    Different algorithms implement this interface, allowing them
    to be used interchangeably by the context.
    """

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """
        Execute the algorithm.
        
        Args:
            data: Input data for the algorithm.
            
        Returns:
            Result of the algorithm.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this strategy."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Get a description of this strategy."""
        pass


class Context:
    """
    Context that uses a Strategy to perform an algorithm.
    
    The context accepts a strategy at construction time and
    uses it to execute the algorithm without knowing the
    algorithm details.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Initialize context with a strategy.
        
        Args:
            strategy: The strategy to use for algorithm execution.
        """
        self._strategy = strategy
        self.execution_log: List[Dict[str, Any]] = []

    def set_strategy(self, strategy: Strategy) -> None:
        """
        Replace the current strategy.
        
        Args:
            strategy: The new strategy to use.
        """
        old_strategy_name = self._strategy.get_name()
        new_strategy_name = strategy.get_name()
        
        print(
            f"\n[Context] Strategy change: {old_strategy_name} → {new_strategy_name}"
        )
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """
        Execute the current strategy.
        
        Args:
            data: Input data for the strategy.
            
        Returns:
            Result from the strategy.
        """
        print(f"[Context] Using strategy: {self._strategy.get_name()}")
        print(f"          {self._strategy.describe()}")
        
        result = self._strategy.execute(data)
        
        # Log execution
        self.execution_log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "strategy": self._strategy.get_name(),
            "input": data,
            "output": result,
        })
        
        return result

    def get_strategy(self) -> Strategy:
        """Get the current strategy."""
        return self._strategy

    def get_strategy_name(self) -> str:
        """Get the name of the current strategy."""
        return self._strategy.get_name()

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get the log of all strategy executions."""
        return self.execution_log.copy()


class ConcreteStrategyA(Strategy):
    """Concrete strategy A implementing a specific algorithm."""

    def execute(self, data: Any) -> Any:
        """
        Execute algorithm A.
        
        Args:
            data: Input data (typically a list or number).
            
        Returns:
            Result of algorithm A.
        """
        print("  [Strategy A] Executing algorithm...")
        if isinstance(data, (list, str)):
            result = data[::-1]  # Reverse
            print(f"  [Strategy A] Result: {result}")
            return result
        elif isinstance(data, (int, float)):
            result = data * 2  # Double
            print(f"  [Strategy A] Result: {result}")
            return result
        else:
            print("  [Strategy A] Unsupported data type")
            return None

    def get_name(self) -> str:
        """Get strategy name."""
        return "Strategy A (Reverse/Double)"

    def describe(self) -> str:
        """Get strategy description."""
        return "Reverses sequences or doubles numbers"


class ConcreteStrategyB(Strategy):
    """Concrete strategy B implementing a specific algorithm."""

    def execute(self, data: Any) -> Any:
        """
        Execute algorithm B.
        
        Args:
            data: Input data (typically a list or number).
            
        Returns:
            Result of algorithm B.
        """
        print("  [Strategy B] Executing algorithm...")
        if isinstance(data, (list, tuple)):
            result = sorted(data)  # Sort
            print(f"  [Strategy B] Result: {result}")
            return result
        elif isinstance(data, str):
            result = ''.join(sorted(data))  # Sort characters
            print(f"  [Strategy B] Result: {result}")
            return result
        elif isinstance(data, (int, float)):
            result = data ** 2  # Square
            print(f"  [Strategy B] Result: {result}")
            return result
        else:
            print("  [Strategy B] Unsupported data type")
            return None

    def get_name(self) -> str:
        """Get strategy name."""
        return "Strategy B (Sort/Square)"

    def describe(self) -> str:
        """Get strategy description."""
        return "Sorts sequences or squares numbers"


class ConcreteStrategyC(Strategy):
    """Concrete strategy C implementing a specific algorithm."""

    def execute(self, data: Any) -> Any:
        """
        Execute algorithm C.
        
        Args:
            data: Input data (typically a list or number).
            
        Returns:
            Result of algorithm C.
        """
        print("  [Strategy C] Executing algorithm...")
        if isinstance(data, (list, tuple)):
            result = list(set(data))  # Remove duplicates
            print(f"  [Strategy C] Result: {result}")
            return result
        elif isinstance(data, str):
            result = ''.join(dict.fromkeys(data))  # Remove duplicate chars
            print(f"  [Strategy C] Result: {result}")
            return result
        elif isinstance(data, (int, float)):
            result = abs(data)  # Absolute value
            print(f"  [Strategy C] Result: {result}")
            return result
        else:
            print("  [Strategy C] Unsupported data type")
            return None

    def get_name(self) -> str:
        """Get strategy name."""
        return "Strategy C (Unique/Abs)"

    def describe(self) -> str:
        """Get strategy description."""
        return "Removes duplicates or takes absolute value"
