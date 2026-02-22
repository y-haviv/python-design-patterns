"""
Real-world Abstract Factory: Database Access Layer.

This example demonstrates a realistic scenario where different databases 
(PostgreSQL, MySQL, SQLite) require different connection strategies, 
query builders, and result formatters. The Abstract Factory pattern 
ensures a consistent, database-agnostic interface across the application.

This is a common pattern in ORMs like SQLAlchemy and database abstraction layers.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class DatabaseEngine(Enum):
    """Supported database engines (product families)."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


@dataclass
class QueryResult:
    """Encapsulates query execution results."""
    rows: List[Dict[str, Any]]
    affected_rows: int = 0
    last_insert_id: Optional[int] = None
    execution_time_ms: float = 0.0


# ============================================================================
# Abstract Products: Database Implementation Components
# ============================================================================


class Connection(ABC):
    """Abstract Product: Database Connection."""

    @abstractmethod
    def connect(self, host: str, user: str, password: str) -> str:
        """Establish a database connection with specific credentials."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> QueryResult:
        """Execute a query and return results."""
        pass

    @abstractmethod
    def close(self) -> str:
        """Close the database connection."""
        pass


class QueryBuilder(ABC):
    """Abstract Product: SQL Query Builder."""

    @abstractmethod
    def build_select(self, table: str, columns: List[str]) -> str:
        """Build a SELECT query (dialect-specific)."""
        pass

    @abstractmethod
    def build_insert(self, table: str, values: Dict[str, Any]) -> str:
        """Build an INSERT query (dialect-specific)."""
        pass

    @abstractmethod
    def build_update(self, table: str, values: Dict[str, Any], where: str) -> str:
        """Build an UPDATE query (dialect-specific)."""
        pass


class DataTypeMapper(ABC):
    """Abstract Product: Maps Python types to database-specific types."""

    @abstractmethod
    def python_to_sql_type(self, python_type: type) -> str:
        """Convert Python type to database-specific column type."""
        pass

    @abstractmethod
    def sql_to_python_type(self, sql_type: str) -> type:
        """Convert database-specific type to Python type."""
        pass


# ============================================================================
# Concrete Products: PostgreSQL Family
# ============================================================================


class PostgreSQLConnection(Connection):
    """Concrete Product: PostgreSQL Connection."""

    def __init__(self):
        self.host = None
        self.connected = False
        self.port = 5432  # Default PostgreSQL port

    def connect(self, host: str, user: str, password: str) -> str:
        """Connect to PostgreSQL server."""
        self.host = host
        self.connected = True
        return (
            f"PostgreSQL Connection established\n"
            f"Host: {host}:{self.port}\n"
            f"User: {user}\n"
            f"Connection pool size: 10 (default)"
        )

    def execute_query(self, query: str) -> QueryResult:
        """Execute PostgreSQL query with RETURNING clause support."""
        if not self.connected:
            return QueryResult(rows=[], affected_rows=0)
        return QueryResult(
            rows=[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
            affected_rows=2,
            execution_time_ms=0.45
        )

    def close(self) -> str:
        """Close PostgreSQL connection."""
        self.connected = False
        return "PostgreSQL connection closed (pool cleaned up)"


class PostgreSQLQueryBuilder(QueryBuilder):
    """Concrete Product: PostgreSQL-specific Query Builder."""

    def build_select(self, table: str, columns: List[str]) -> str:
        """Build PostgreSQL SELECT with OFFSET pagination."""
        cols = ", ".join(columns) if columns else "*"
        return f'SELECT {cols} FROM {table} OFFSET 0 LIMIT 10;'

    def build_insert(self, table: str, values: Dict[str, Any]) -> str:
        """Build PostgreSQL INSERT with RETURNING clause."""
        cols = ", ".join(values.keys())
        vals = ", ".join(f"'{v}'" for v in values.values())
        return f"INSERT INTO {table} ({cols}) VALUES ({vals}) RETURNING *;"

    def build_update(self, table: str, values: Dict[str, Any], where: str) -> str:
        """Build PostgreSQL UPDATE with RETURNING clause."""
        set_clause = ", ".join(f"{k} = '{v}'" for k, v in values.items())
        return f"UPDATE {table} SET {set_clause} WHERE {where} RETURNING *;"


class PostgreSQLDataTypeMapper(DataTypeMapper):
    """Concrete Product: PostgreSQL Data Type Mapper."""

    def python_to_sql_type(self, python_type: type) -> str:
        """PostgreSQL column types."""
        mapping = {
            str: "VARCHAR(255)",
            int: "INTEGER",
            float: "NUMERIC(10,2)",
            bool: "BOOLEAN",
            bytes: "BYTEA"
        }
        return mapping.get(python_type, "TEXT")

    def sql_to_python_type(self, sql_type: str) -> type:
        """Convert PostgreSQL types to Python."""
        mapping = {
            "INTEGER": int,
            "VARCHAR": str,
            "NUMERIC": float,
            "BOOLEAN": bool,
            "BYTEA": bytes
        }
        return mapping.get(sql_type, str)


# ============================================================================
# Concrete Products: MySQL Family
# ============================================================================


class MySQLConnection(Connection):
    """Concrete Product: MySQL Connection."""

    def __init__(self):
        self.host = None
        self.connected = False
        self.port = 3306  # Default MySQL port

    def connect(self, host: str, user: str, password: str) -> str:
        """Connect to MySQL server."""
        self.host = host
        self.connected = True
        return (
            f"MySQL Connection established\n"
            f"Host: {host}:{self.port}\n"
            f"User: {user}\n"
            f"Connection pool size: 5 (default)"
        )

    def execute_query(self, query: str) -> QueryResult:
        """Execute MySQL query."""
        if not self.connected:
            return QueryResult(rows=[], affected_rows=0)
        return QueryResult(
            rows=[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
            affected_rows=2,
            last_insert_id=3,
            execution_time_ms=0.62
        )

    def close(self) -> str:
        """Close MySQL connection."""
        self.connected = False
        return "MySQL connection closed (all connections released)"


class MySQLQueryBuilder(QueryBuilder):
    """Concrete Product: MySQL-specific Query Builder."""

    def build_select(self, table: str, columns: List[str]) -> str:
        """Build MySQL SELECT with backtick quoting."""
        cols_str = ", ".join(f"`{c}`" for c in columns) if columns else "*"
        return f"SELECT {cols_str} FROM `{table}` LIMIT 10;"

    def build_insert(self, table: str, values: Dict[str, Any]) -> str:
        """Build MySQL INSERT."""
        cols = ", ".join(f"`{k}`" for k in values.keys())
        vals = ", ".join(f"'{v}'" for v in values.values())
        return f"INSERT INTO `{table}` ({cols}) VALUES ({vals});"

    def build_update(self, table: str, values: Dict[str, Any], where: str) -> str:
        """Build MySQL UPDATE."""
        set_clause = ", ".join(f"`{k}` = '{v}'" for k, v in values.items())
        return f"UPDATE `{table}` SET {set_clause} WHERE {where};"


class MySQLDataTypeMapper(DataTypeMapper):
    """Concrete Product: MySQL Data Type Mapper."""

    def python_to_sql_type(self, python_type: type) -> str:
        """MySQL column types."""
        mapping = {
            str: "VARCHAR(255)",
            int: "INT",
            float: "DECIMAL(10,2)",
            bool: "TINYINT(1)",
            bytes: "BLOB"
        }
        return mapping.get(python_type, "TEXT")

    def sql_to_python_type(self, sql_type: str) -> type:
        """Convert MySQL types to Python."""
        mapping = {
            "INT": int,
            "VARCHAR": str,
            "DECIMAL": float,
            "TINYINT": bool,
            "BLOB": bytes
        }
        return mapping.get(sql_type, str)


# ============================================================================
# Concrete Products: SQLite Family
# ============================================================================


class SQLiteConnection(Connection):
    """Concrete Product: SQLite Connection."""

    def __init__(self):
        self.db_file = None
        self.connected = False

    def connect(self, db_file: str, user: str = None, password: str = None) -> str:
        """Connect to SQLite database file."""
        self.db_file = db_file
        self.connected = True
        return (
            f"SQLite Connection established\n"
            f"Database file: {db_file}\n"
            f"Mode: local file-based\n"
            f"No authentication required"
        )

    def execute_query(self, query: str) -> QueryResult:
        """Execute SQLite query."""
        if not self.connected:
            return QueryResult(rows=[], affected_rows=0)
        return QueryResult(
            rows=[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
            affected_rows=2,
            execution_time_ms=0.08
        )

    def close(self) -> str:
        """Close SQLite connection."""
        self.connected = False
        return "SQLite connection closed (file-based database synchronized)"


class SQLiteQueryBuilder(QueryBuilder):
    """Concrete Product: SQLite-specific Query Builder."""

    def build_select(self, table: str, columns: List[str]) -> str:
        """Build SQLite SELECT."""
        cols = ", ".join(columns) if columns else "*"
        return f'SELECT {cols} FROM {table} LIMIT 10;'

    def build_insert(self, table: str, values: Dict[str, Any]) -> str:
        """Build SQLite INSERT (no RETURNING clause)."""
        cols = ", ".join(values.keys())
        vals = ", ".join(f"'{v}'" for v in values.values())
        return f"INSERT INTO {table} ({cols}) VALUES ({vals});"

    def build_update(self, table: str, values: Dict[str, Any], where: str) -> str:
        """Build SQLite UPDATE."""
        set_clause = ", ".join(f"{k} = '{v}'" for k, v in values.items())
        return f"UPDATE {table} SET {set_clause} WHERE {where};"


class SQLiteDataTypeMapper(DataTypeMapper):
    """Concrete Product: SQLite Data Type Mapper."""

    def python_to_sql_type(self, python_type: type) -> str:
        """SQLite column types (limited set)."""
        mapping = {
            str: "TEXT",
            int: "INTEGER",
            float: "REAL",
            bool: "INTEGER",  # SQLite uses INTEGER for booleans
            bytes: "BLOB"
        }
        return mapping.get(python_type, "TEXT")

    def sql_to_python_type(self, sql_type: str) -> type:
        """Convert SQLite types to Python."""
        mapping = {
            "INTEGER": int,
            "TEXT": str,
            "REAL": float,
            "BLOB": bytes
        }
        return mapping.get(sql_type, str)


# ============================================================================
# Abstract Factory
# ============================================================================


class DatabaseFactory(ABC):
    """
    Abstract Factory: Creates database implementation components.
    
    Each concrete factory provides a complete family of database-specific 
    components that work together seamlessly.
    """

    @abstractmethod
    def create_connection(self) -> Connection:
        """Create a connection for this database engine."""
        pass

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder:
        """Create a query builder for this database engine."""
        pass

    @abstractmethod
    def create_data_type_mapper(self) -> DataTypeMapper:
        """Create a data type mapper for this database engine."""
        pass


# ============================================================================
# Concrete Factories
# ============================================================================


class PostgreSQLFactory(DatabaseFactory):
    """Concrete Factory: PostgreSQL database family."""

    def create_connection(self) -> Connection:
        """Create a PostgreSQL connection."""
        return PostgreSQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        """Create a PostgreSQL query builder."""
        return PostgreSQLQueryBuilder()

    def create_data_type_mapper(self) -> DataTypeMapper:
        """Create a PostgreSQL data type mapper."""
        return PostgreSQLDataTypeMapper()


class MySQLFactory(DatabaseFactory):
    """Concrete Factory: MySQL database family."""

    def create_connection(self) -> Connection:
        """Create a MySQL connection."""
        return MySQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        """Create a MySQL query builder."""
        return MySQLQueryBuilder()

    def create_data_type_mapper(self) -> DataTypeMapper:
        """Create a MySQL data type mapper."""
        return MySQLDataTypeMapper()


class SQLiteFactory(DatabaseFactory):
    """Concrete Factory: SQLite database family."""

    def create_connection(self) -> Connection:
        """Create a SQLite connection."""
        return SQLiteConnection()

    def create_query_builder(self) -> QueryBuilder:
        """Create a SQLite query builder."""
        return SQLiteQueryBuilder()

    def create_data_type_mapper(self) -> DataTypeMapper:
        """Create a SQLite data type mapper."""
        return SQLiteDataTypeMapper()


# ============================================================================
# Database Application Layer
# ============================================================================


class DatabaseAdapter:
    """
    Adapter: Uses a database factory to provide a database-agnostic interface.
    
    Client code depends only on this adapter and abstract interfaces, 
    never on concrete database implementations.
    """

    def __init__(self, factory: DatabaseFactory):
        """
        Initialize adapter with a database factory.
        
        Args:
            factory: The DatabaseFactory providing the implementation family.
        """
        self._factory = factory
        self._conn = factory.create_connection()
        self._query_builder = factory.create_query_builder()
        self._type_mapper = factory.create_data_type_mapper()

    def connect(self, host: str, user: str, password: str) -> str:
        """Connect to the database."""
        return self._conn.connect(host, user, password)

    def query_select(self, table: str, columns: List[str] = None) -> str:
        """Build and show a SELECT query (database-agnostic)."""
        return self._query_builder.build_select(table, columns or [])

    def query_insert(self, table: str, values: Dict[str, Any]) -> str:
        """Build and show an INSERT query (database-agnostic)."""
        return self._query_builder.build_insert(table, values)

    def get_column_type(self, python_type: type) -> str:
        """Get database-specific column type for Python type."""
        return self._type_mapper.python_to_sql_type(python_type)

    def close(self) -> str:
        """Close the database connection."""
        return self._conn.close()


class DatabaseFactoryRegistry:
    """Registry: Manages database factory instances."""

    def __init__(self):
        self._factories = {
            DatabaseEngine.POSTGRESQL: PostgreSQLFactory(),
            DatabaseEngine.MYSQL: MySQLFactory(),
            DatabaseEngine.SQLITE: SQLiteFactory(),
        }

    def get_factory(self, engine: DatabaseEngine) -> DatabaseFactory:
        """Get factory for specified database engine."""
        if engine not in self._factories:
            raise ValueError(f"Unsupported database engine: {engine}")
        return self._factories[engine]

    def create_adapter(self, engine: DatabaseEngine) -> DatabaseAdapter:
        """Create a database adapter for the specified engine."""
        factory = self.get_factory(engine)
        return DatabaseAdapter(factory)

    def get_available_engines(self) -> List[str]:
        """List all available database engines."""
        return [engine.value for engine in self._factories.keys()]


def demonstrate_database_agnosticism():
    """
    Demonstrate how the same application code works with different databases.
    
    This shows the power of Abstract Factory: client code never changes,
    but the entire database backend can be switched by changing one factory.
    """
    registry = DatabaseFactoryRegistry()
    
    results = []
    
    for engine in [DatabaseEngine.POSTGRESQL, DatabaseEngine.MYSQL, DatabaseEngine.SQLITE]:
        adapter = registry.create_adapter(engine)
        
        # Same code for all databases
        connection_info = adapter.connect(
            host="localhost" if engine != DatabaseEngine.SQLITE else "app.db",
            user="admin",
            password="secret"
        )
        
        select_query = adapter.query_select("users", ["id", "name"])
        insert_query = adapter.query_insert("users", {"name": "Alice", "email": "alice@example.com"})
        int_type = adapter.get_column_type(int)
        str_type = adapter.get_column_type(str)
        close_info = adapter.close()
        
        engine_name = engine.value.upper()
        results.append(
            f"=== {engine_name} ===\n"
            f"Connection: {connection_info}\n\n"
            f"SELECT Query: {select_query}\n"
            f"INSERT Query: {insert_query}\n"
            f"INT Type: {int_type}\n"
            f"STR Type: {str_type}\n"
            f"Close: {close_info}\n"
        )
    
    return "\n".join(results)
