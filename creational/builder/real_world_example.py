"""
Real-world Builder: SQL Query Builder with Fluent API.

This example demonstrates a realistic use case where the Builder pattern 
is used to construct complex SQL queries in a readable, maintainable way.
SQL queries often have many optional clauses (WHERE, ORDER BY, GROUP BY, LIMIT, etc.),
making the Builder pattern ideal for this use case.

This pattern is used in popular ORMs like SQLAlchemy and Django ORM.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class JoinType(Enum):
    """SQL JOIN types."""
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"


class OrderDirection(Enum):
    """Sort order direction."""
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class SQLQuery:
    """
    Complex Product: SQL Query.
    
    Represents a structured SQL SELECT query with all its components.
    This would be cumbersome to construct directly.
    """

    select_columns: List[str] = field(default_factory=list)
    from_table: Optional[str] = None
    joins: List[Tuple[JoinType, str, str]] = field(default_factory=list)  # (type, table, condition)
    where_conditions: List[str] = field(default_factory=list)
    group_by_columns: List[str] = field(default_factory=list)
    having_conditions: List[str] = field(default_factory=list)
    order_by: List[Tuple[str, OrderDirection]] = field(default_factory=list)
    limit_value: Optional[int] = None
    offset_value: Optional[int] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate the query is properly formed."""
        if not self.from_table:
            raise ValueError("Query must have a FROM clause")
        if not self.select_columns:
            raise ValueError("Query must have SELECT columns")
        if any(";" in s for s in self.select_columns + [self.from_table]):
            raise ValueError("SQL injection detected: semicolon in query")
        return True

    def to_sql(self) -> str:
        """
        Construct the SQL string from the query components.
        
        Returns:
            The SQL query string (without parameters substituted).
        """
        parts = []

        # SELECT clause
        parts.append(f"SELECT {', '.join(self.select_columns)}")

        # FROM clause
        parts.append(f"FROM {self.from_table}")

        # JOIN clauses
        for join_type, table, condition in self.joins:
            parts.append(f"{join_type.value} {table} ON {condition}")

        # WHERE clause
        if self.where_conditions:
            where_clause = " AND ".join(f"({cond})" for cond in self.where_conditions)
            parts.append(f"WHERE {where_clause}")

        # GROUP BY clause
        if self.group_by_columns:
            parts.append(f"GROUP BY {', '.join(self.group_by_columns)}")

        # HAVING clause
        if self.having_conditions:
            having_clause = " AND ".join(f"({cond})" for cond in self.having_conditions)
            parts.append(f"HAVING {having_clause}")

        # ORDER BY clause
        if self.order_by:
            order_clause = ", ".join(f"{col} {direction.value}" for col, direction in self.order_by)
            parts.append(f"ORDER BY {order_clause}")

        # LIMIT clause
        if self.limit_value is not None:
            parts.append(f"LIMIT {self.limit_value}")

        # OFFSET clause
        if self.offset_value is not None:
            parts.append(f"OFFSET {self.offset_value}")

        return "\n".join(parts)

    def to_sql_single_line(self) -> str:
        """Get query as a single line."""
        return " ".join(line.strip() for line in self.to_sql().split("\n"))


class SQLQueryBuilder:
    """
    Concrete Builder: SQL Query Builder.
    
    Provides a fluent interface for constructing complex SQL SELECT queries.
    This demonstrates the Builder pattern for real-world SQL query construction.
    """

    def __init__(self):
        """Initialize builder."""
        self._select_columns: List[str] = ["*"]
        self._from_table: Optional[str] = None
        self._joins: List[Tuple[JoinType, str, str]] = []
        self._where_conditions: List[str] = []
        self._group_by_columns: List[str] = []
        self._having_conditions: List[str] = []
        self._order_by: List[Tuple[str, OrderDirection]] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._parameters: Dict[str, Any] = {}

    def select(self, *columns: str) -> SQLQueryBuilder:
        """
        Set the SELECT columns.
        
        Args:
            *columns: Column names to select. If empty, uses '*' (all columns).
            
        Returns:
            Self for method chaining.
        """
        if columns:
            self._select_columns = list(columns)
        else:
            self._select_columns = ["*"]
        return self

    def from_table(self, table_name: str) -> SQLQueryBuilder:
        """
        Set the FROM table.
        
        Args:
            table_name: Name of the table to query from.
            
        Returns:
            Self for method chaining.
        """
        self._from_table = table_name
        return self

    def inner_join(self, table: str, condition: str) -> SQLQueryBuilder:
        """Add an INNER JOIN clause."""
        self._joins.append((JoinType.INNER, table, condition))
        return self

    def left_join(self, table: str, condition: str) -> SQLQueryBuilder:
        """Add a LEFT JOIN clause."""
        self._joins.append((JoinType.LEFT, table, condition))
        return self

    def right_join(self, table: str, condition: str) -> SQLQueryBuilder:
        """Add a RIGHT JOIN clause."""
        self._joins.append((JoinType.RIGHT, table, condition))
        return self

    def join(self, join_type: JoinType, table: str, condition: str) -> SQLQueryBuilder:
        """Add a JOIN clause with specified type."""
        self._joins.append((join_type, table, condition))
        return self

    def where(self, condition: str) -> SQLQueryBuilder:
        """
        Add a WHERE condition.
        
        Multiple calls are combined with AND.
        
        Args:
            condition: The WHERE condition (e.g., "age > 18", "status = :status").
            
        Returns:
            Self for method chaining.
        """
        self._where_conditions.append(condition)
        return self

    def where_in(self, column: str, values: List[Any]) -> SQLQueryBuilder:
        """Add a WHERE ... IN condition."""
        placeholders = ", ".join(f":{i}" for i in range(len(values)))
        condition = f"{column} IN ({placeholders})"
        self._where_conditions.append(condition)
        for i, value in enumerate(values):
            self._parameters[str(i)] = value
        return self

    def where_between(self, column: str, start: Any, end: Any) -> SQLQueryBuilder:
        """Add a WHERE ... BETWEEN condition."""
        condition = f"{column} BETWEEN :start AND :end"
        self._where_conditions.append(condition)
        self._parameters["start"] = start
        self._parameters["end"] = end
        return self

    def parameter(self, name: str, value: Any) -> SQLQueryBuilder:
        """
        Add a query parameter (for parameterized queries).
        
        Args:
            name: Parameter name (used in conditions with :name).
            value: Parameter value.
            
        Returns:
            Self for method chaining.
        """
        self._parameters[name] = value
        return self

    def group_by(self, *columns: str) -> SQLQueryBuilder:
        """
        Add GROUP BY columns.
        
        Args:
            *columns: Columns to group by.
            
        Returns:
            Self for method chaining.
        """
        self._group_by_columns.extend(columns)
        return self

    def having(self, condition: str) -> SQLQueryBuilder:
        """
        Add a HAVING condition.
        
        Args:
            condition: The HAVING condition (e.g., "COUNT(*) > 5").
            
        Returns:
            Self for method chaining.
        """
        self._having_conditions.append(condition)
        return self

    def order_by(self, column: str, direction: OrderDirection = OrderDirection.ASC) -> SQLQueryBuilder:
        """
        Add an ORDER BY clause.
        
        Args:
            column: Column to order by.
            direction: Sort direction (ASC or DESC).
            
        Returns:
            Self for method chaining.
        """
        self._order_by.append((column, direction))
        return self

    def limit(self, count: int) -> SQLQueryBuilder:
        """
        Set the LIMIT clause.
        
        Args:
            count: Maximum number of rows to return.
            
        Returns:
            Self for method chaining.
        """
        self._limit_value = count
        return self

    def offset(self, count: int) -> SQLQueryBuilder:
        """
        Set the OFFSET clause (for pagination).
        
        Args:
            count: Number of rows to skip.
            
        Returns:
            Self for method chaining.
        """
        self._offset_value = count
        return self

    def reset(self) -> SQLQueryBuilder:
        """Reset the builder to initial state."""
        self.__init__()
        return self

    def build(self) -> SQLQuery:
        """
        Build and return the SQLQuery object.
        
        Returns:
            A validated SQLQuery instance.
            
        Raises:
            ValueError: If the query is invalid.
        """
        query = SQLQuery(
            select_columns=self._select_columns.copy(),
            from_table=self._from_table,
            joins=self._joins.copy(),
            where_conditions=self._where_conditions.copy(),
            group_by_columns=self._group_by_columns.copy(),
            having_conditions=self._having_conditions.copy(),
            order_by=self._order_by.copy(),
            limit_value=self._limit_value,
            offset_value=self._offset_value,
            parameters=self._parameters.copy()
        )
        query.validate()
        return query


# ============================================================================
# Query Templates (Director Pattern)
# ============================================================================


class QueryTemplates:
    """
    Director Pattern: Provides pre-built query templates for common queries.
    """

    @staticmethod
    def users_with_posts() -> SQLQuery:
        """Query users with their post count."""
        return (SQLQueryBuilder()
                .select("u.id", "u.name", "u.email", "COUNT(p.id) as post_count")
                .from_table("users u")
                .left_join("posts p", "p.user_id = u.id")
                .group_by("u.id", "u.name", "u.email")
                .having("COUNT(p.id) > 0")
                .order_by("post_count", OrderDirection.DESC)
                .build())

    @staticmethod
    def active_users_paginated(page: int = 1, page_size: int = 20) -> SQLQuery:
        """Query active users with pagination."""
        offset = (page - 1) * page_size
        return (SQLQueryBuilder()
                .select("id", "name", "email", "created_at")
                .from_table("users")
                .where("status = :status")
                .parameter("status", "active")
                .order_by("created_at", OrderDirection.DESC)
                .limit(page_size)
                .offset(offset)
                .build())

    @staticmethod
    def orders_by_customer(customer_id: int) -> SQLQuery:
        """Query orders for a specific customer with product details."""
        return (SQLQueryBuilder()
                .select("o.id", "o.order_date", "p.name", "p.price", "oi.quantity")
                .from_table("orders o")
                .inner_join("order_items oi", "oi.order_id = o.id")
                .inner_join("products p", "p.id = oi.product_id")
                .where("o.customer_id = :customer_id")
                .parameter("customer_id", customer_id)
                .order_by("o.order_date", OrderDirection.DESC)
                .build())

    @staticmethod
    def sales_report() -> SQLQuery:
        """Query sales summary by product."""
        return (SQLQueryBuilder()
                .select("p.id", "p.name", "SUM(oi.quantity) as total_sold", "SUM(oi.quantity * p.price) as revenue")
                .from_table("products p")
                .left_join("order_items oi", "oi.product_id = p.id")
                .where("p.active = :active")
                .parameter("active", True)
                .group_by("p.id", "p.name")
                .having("SUM(oi.quantity) > :min_sales")
                .parameter("min_sales", 10)
                .order_by("revenue", OrderDirection.DESC)
                .limit(100)
                .build())


def demonstrate_query_building():
    """Demonstrate various SQL query building scenarios."""
    
    scenarios = []
    
    # Scenario 1: Simple SELECT
    query1 = (SQLQueryBuilder()
              .select("id", "name", "email")
              .from_table("users")
              .where("age > :min_age")
              .parameter("min_age", 18)
              .order_by("name")
              .limit(10)
              .build())
    
    scenarios.append(("Simple User Query", query1.to_sql_single_line()))
    
    # Scenario 2: Complex query with joins and aggregation
    query2 = (SQLQueryBuilder()
              .select("u.id", "u.name", "COUNT(o.id) as order_count", "SUM(o.total) as total_spent")
              .from_table("users u")
              .left_join("orders o", "o.user_id = u.id")
              .where("u.status = :status")
              .parameter("status", "active")
              .where("u.created_at >= :start_date")
              .parameter("start_date", "2024-01-01")
              .group_by("u.id", "u.name")
              .having("COUNT(o.id) >= :min_orders")
              .parameter("min_orders", 5)
              .order_by("total_spent", OrderDirection.DESC)
              .limit(50)
              .build())
    
    scenarios.append(("Complex Analytics Query", query2.to_sql_single_line()))
    
    # Scenario 3: Using templates
    query3 = QueryTemplates.active_users_paginated(page=2, page_size=25)
    scenarios.append(("Paginated Users Query", query3.to_sql_single_line()))
    
    return scenarios
