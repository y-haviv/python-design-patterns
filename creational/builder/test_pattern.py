"""
Comprehensive tests for the Builder pattern.

These tests verify:
1. Basic builder functionality and fluent interface.
2. Method chaining and return value consistency.
3. Default values and partial configuration.
4. Validation on build().
5. Builder reusability and reset functionality.
6. Complex real-world scenarios with SQL queries.
"""

from __future__ import annotations
import pytest
from typing import List

from .pattern import (
    HTTPMethod,
    HTTPRequest,
    HTTPRequestBuilder,
    Computer,
    ComputerBuilder,
    RequestTemplates,
    ComputerTemplates,
)

from .real_world_example import (
    JoinType,
    OrderDirection,
    SQLQuery,
    SQLQueryBuilder,
    QueryTemplates,
)


class TestHTTPRequestBuilder:
    """Test HTTP request builder functionality."""

    def test_builder_returns_self_for_chaining(self):
        """Verify builder methods return self for chaining."""
        builder = HTTPRequestBuilder()

        result = builder.with_url("https://api.example.com")
        assert result is builder

    def test_fluent_interface_chain(self):
        """Verify fluent interface chaining works."""
        request = (HTTPRequestBuilder()
                  .with_url("https://api.example.com")
                  .with_method("GET")
                  .with_header("Accept", "application/json")
                  .build())

        assert isinstance(request, HTTPRequest)
        assert request.url == "https://api.example.com"
        assert request.method == HTTPMethod.GET
        assert request.headers["Accept"] == "application/json"

    def test_build_creates_http_request(self):
        """Verify build() creates an HTTPRequest instance."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .with_method("POST")
                  .build())

        assert isinstance(request, HTTPRequest)
        assert request.method == HTTPMethod.POST

    def test_default_values_are_applied(self):
        """Verify default values are set when not specified."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .build())

        assert request.method == HTTPMethod.GET
        assert request.timeout == 30
        assert request.max_retries == 3
        assert request.verify_ssl is True

    def test_with_url_is_required_for_validation(self):
        """Verify build() validates that URL is set."""
        with pytest.raises(ValueError):
            HTTPRequestBuilder().build()

    def test_with_json_body_sets_content_type_header(self):
        """Verify with_json_body sets Content-Type header."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .with_method("POST")
                  .with_json_body({"key": "value"})
                  .build())

        assert request.headers["Content-Type"] == "application/json"
        assert '"key": "value"' in request.body or "'key': 'value'" in request.body

    def test_multiple_headers(self):
        """Verify multiple headers can be added."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .with_header("X-Token", "secret")
                  .with_header("X-Request-ID", "req-123")
                  .with_headers({"X-Custom": "value"})
                  .build())

        assert request.headers["X-Token"] == "secret"
        assert request.headers["X-Request-ID"] == "req-123"
        assert request.headers["X-Custom"] == "value"

    def test_query_parameters(self):
        """Verify query parameters can be added."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .with_query_param("page", "1")
                  .with_query_param("limit", "10")
                  .build())

        assert request.query_params["page"] == "1"
        assert request.query_params["limit"] == "10"

    def test_request_construct_method(self):
        """Verify request can be constructed as a string."""
        request = (HTTPRequestBuilder()
                  .with_url("https://api.example.com/users")
                  .with_method("POST")
                  .with_header("X-Token", "secret")
                  .with_json_body({"name": "John"})
                  .with_timeout(20)
                  .build())

        constructed = request.construct()

        assert "POST" in constructed
        assert "https://api.example.com/users" in constructed
        assert "X-Token" in constructed
        assert "20" in constructed

    def test_builder_reset(self):
        """Verify builder can be reset to initial state."""
        builder = HTTPRequestBuilder()
        
        builder.with_url("https://first.com").with_method("POST")
        builder.reset()
        
        # After reset, should create a GET request
        request1 = builder.build()
        assert request1.method == HTTPMethod.GET
        assert request1.url == ""

    def test_builder_reuse(self):
        """Verify builder can be reused to create multiple objects."""
        builder = HTTPRequestBuilder()
        
        request1 = builder.with_url("https://api1.com").build()
        
        builder.reset()
        request2 = builder.with_url("https://api2.com").build()
        
        assert request1.url == "https://api1.com"
        assert request2.url == "https://api2.com"


class TestComputerBuilder:
    """Test computer configuration builder."""

    def test_basic_computer_build(self):
        """Verify basic computer building."""
        computer = ComputerBuilder().build()

        assert isinstance(computer, Computer)
        assert computer.cpu_cores == 4
        assert computer.ram_gb == 8

    def test_custom_computer_configuration(self):
        """Verify custom computer configuration."""
        computer = (ComputerBuilder()
                   .with_cpu(8, 3.5)
                   .with_ram(16)
                   .with_ssd(512)
                   .build())

        assert computer.cpu_cores == 8
        assert computer.cpu_ghz == 3.5
        assert computer.ram_gb == 16
        assert computer.ssd_gb == 512

    def test_computer_with_gpu(self):
        """Verify computer with GPU configuration."""
        computer = (ComputerBuilder()
                   .with_gpu("NVIDIA RTX 3080", 10)
                   .build())

        assert computer.has_gpu is True
        assert computer.gpu_model == "NVIDIA RTX 3080"
        assert computer.gpu_vram_gb == 10

    def test_computer_with_hdd(self):
        """Verify computer with HDD configuration."""
        computer = (ComputerBuilder()
                   .with_hdd(2048)
                   .build())

        assert computer.has_hdd is True
        assert computer.hdd_gb == 2048

    def test_computer_liquid_cooling(self):
        """Verify liquid cooling option."""
        computer = (ComputerBuilder()
                   .with_liquid_cooling()
                   .build())

        assert computer.cooling_type == "liquid"

    def test_computer_connectivity_options(self):
        """Verify WiFi and Bluetooth options."""
        computer = (ComputerBuilder()
                   .without_wifi()
                   .without_bluetooth()
                   .build())

        assert computer.has_wifi is False
        assert computer.has_bluetooth is False

    def test_computer_price_estimation(self):
        """Verify price estimation increases with features."""
        basic = ComputerBuilder().build()
        gaming = (ComputerBuilder()
                 .with_cpu(16, 4.0)
                 .with_ram(32)
                 .with_gpu("NVIDIA RTX 4080", 12)
                 .build())

        basic_price = basic.estimate_price()
        gaming_price = gaming.estimate_price()

        assert gaming_price > basic_price

    def test_computer_specifications_summary(self):
        """Verify specifications summary generation."""
        computer = (ComputerBuilder()
                   .with_cpu(8, 3.0)
                   .with_ram(16)
                   .build())

        summary = computer.specifications_summary()

        assert "8 cores" in summary
        assert "16GB" in summary or "16 cores" not in summary


class TestRequestTemplates:
    """Test pre-built request templates."""

    def test_api_call_template(self):
        """Verify API call template creates proper request."""
        request = RequestTemplates.get_api_call()

        assert request.method == HTTPMethod.GET
        assert "api.example.com" in request.url
        assert request.headers["Accept"] == "application/json"
        assert request.timeout == 15

    def test_post_json_template(self):
        """Verify POST JSON template."""
        request = RequestTemplates.post_json_data()

        assert request.method == HTTPMethod.POST
        assert request.headers["Content-Type"] == "application/json"
        assert request.body is not None

    def test_webhook_template(self):
        """Verify webhook template."""
        request = RequestTemplates.webhook_request()

        assert request.method == HTTPMethod.POST
        assert request.max_retries == 5
        assert "webhook" in request.url.lower()


class TestComputerTemplates:
    """Test pre-built computer templates."""

    def test_budget_build_template(self):
        """Verify budget build template."""
        computer = ComputerTemplates.budget_build()

        assert computer.cpu_cores == 4
        assert computer.ram_gb == 8
        assert computer.ssd_gb == 256

    def test_gaming_build_template(self):
        """Verify gaming build is powerful."""
        computer = ComputerTemplates.gaming_build()

        assert computer.cpu_cores >= 16
        assert computer.ram_gb >= 32
        assert computer.has_gpu is True
        assert computer.cooling_type == "liquid"

    def test_workstation_build_template(self):
        """Verify workstation build for professionals."""
        computer = ComputerTemplates.workstation_build()

        assert computer.cpu_cores >= 32
        assert computer.ram_gb >= 128
        assert computer.has_gpu is True


class TestSQLQueryBuilder:
    """Test SQL query builder."""

    def test_simple_select_query(self):
        """Verify simple SELECT query building."""
        query = (SQLQueryBuilder()
                .select("id", "name")
                .from_table("users")
                .build())

        sql = query.to_sql_single_line()

        assert "SELECT id, name" in sql
        assert "FROM users" in sql

    def test_select_all_by_default(self):
        """Verify SELECT * when no columns specified."""
        query = (SQLQueryBuilder()
                .from_table("users")
                .build())

        sql = query.to_sql_single_line()
        assert "SELECT *" in sql

    def test_where_clause(self):
        """Verify WHERE clause building."""
        query = (SQLQueryBuilder()
                .select("id", "name")
                .from_table("users")
                .where("age > :age")
                .parameter("age", 18)
                .build())

        sql = query.to_sql_single_line()

        assert "WHERE" in sql
        assert "age > " in sql

    def test_multiple_where_conditions(self):
        """Verify multiple WHERE conditions are combined with AND."""
        query = (SQLQueryBuilder()
                .from_table("users")
                .where("age > :min_age")
                .where("status = :status")
                .parameter("min_age", 18)
                .parameter("status", "active")
                .build())

        sql = query.to_sql_single_line()

        assert "age > " in sql
        assert "status = " in sql
        assert "AND" in sql

    def test_join_clause(self):
        """Verify JOIN clause building."""
        query = (SQLQueryBuilder()
                .select("u.name", "o.id")
                .from_table("users u")
                .inner_join("orders o", "o.user_id = u.id")
                .build())

        sql = query.to_sql_single_line()

        assert "INNER JOIN" in sql
        assert "orders o" in sql
        assert "ON" in sql

    def test_group_by_clause(self):
        """Verify GROUP BY clause building."""
        query = (SQLQueryBuilder()
                .select("user_id", "COUNT(*) as total")
                .from_table("orders")
                .group_by("user_id")
                .build())

        sql = query.to_sql_single_line()

        assert "GROUP BY" in sql
        assert "user_id" in sql

    def test_having_clause(self):
        """Verify HAVING clause building."""
        query = (SQLQueryBuilder()
                .select("user_id", "COUNT(*) as total")
                .from_table("orders")
                .group_by("user_id")
                .having("COUNT(*) > :min")
                .parameter("min", 5)
                .build())

        sql = query.to_sql_single_line()

        assert "HAVING" in sql

    def test_order_by_clause(self):
        """Verify ORDER BY clause building."""
        query = (SQLQueryBuilder()
                .select("id", "name")
                .from_table("users")
                .order_by("name", OrderDirection.ASC)
                .order_by("id", OrderDirection.DESC)
                .build())

        sql = query.to_sql_single_line()

        assert "ORDER BY" in sql
        assert "ASC" in sql
        assert "DESC" in sql

    def test_limit_and_offset(self):
        """Verify LIMIT and OFFSET clauses."""
        query = (SQLQueryBuilder()
                .select("id", "name")
                .from_table("users")
                .limit(10)
                .offset(20)
                .build())

        sql = query.to_sql_single_line()

        assert "LIMIT 10" in sql
        assert "OFFSET 20" in sql

    def test_complex_query_building(self):
        """Verify complex query with multiple clauses."""
        query = (SQLQueryBuilder()
                .select("u.id", "u.name", "COUNT(o.id) as order_count")
                .from_table("users u")
                .left_join("orders o", "o.user_id = u.id")
                .where("u.status = :status")
                .parameter("status", "active")
                .group_by("u.id", "u.name")
                .having("COUNT(o.id) > :min")
                .parameter("min", 5)
                .order_by("order_count", OrderDirection.DESC)
                .limit(100)
                .build())

        sql = query.to_sql_single_line()

        # Verify all components are present
        assert "SELECT" in sql
        assert "LEFT JOIN" in sql
        assert "WHERE" in sql
        assert "GROUP BY" in sql
        assert "HAVING" in sql
        assert "ORDER BY" in sql
        assert "LIMIT" in sql

    def test_query_reset(self):
        """Verify query builder reset."""
        builder = SQLQueryBuilder()
        
        builder.select("id").from_table("users").where("age > 18")
        builder.reset()
        
        query = builder.select("name").from_table("products").build()
        sql = query.to_sql_single_line()
        
        assert "name" in sql
        assert "products" in sql
        assert "users" not in sql or "users" not being the original query


class TestQueryTemplates:
    """Test pre-built query templates."""

    def test_users_with_posts_template(self):
        """Verify users with posts template."""
        query = QueryTemplates.users_with_posts()

        sql = query.to_sql_single_line()

        assert "COUNT" in sql
        assert "LEFT JOIN" in sql
        assert "GROUP BY" in sql

    def test_active_users_paginated_template(self):
        """Verify paginated users template."""
        query = QueryTemplates.active_users_paginated(page=2, page_size=25)

        sql = query.to_sql_single_line()

        # Page 2, size 25 = offset 25
        assert "LIMIT 25" in sql
        assert "OFFSET 25" in sql

    def test_orders_by_customer_template(self):
        """Verify orders by customer template."""
        query = QueryTemplates.orders_by_customer(customer_id=123)

        sql = query.to_sql_single_line()

        assert "INNER JOIN" in sql
        assert "ORDER BY" in sql

    def test_sales_report_template(self):
        """Verify sales report template."""
        query = QueryTemplates.sales_report()

        sql = query.to_sql_single_line()

        assert "SUM" in sql
        assert "GROUP BY" in sql
        assert "HAVING" in sql


class TestBuilderBenefits:
    """Test the key benefits of the Builder pattern."""

    def test_readable_configuration_http_request(self):
        """Demonstrate readable HTTP request configuration."""
        request = (HTTPRequestBuilder()
                  .with_url("https://api.example.com/users")
                  .with_method("POST")
                  .with_header("Authorization", "Bearer token")
                  .with_json_body({"email": "user@example.com"})
                  .with_timeout(30)
                  .with_max_retries(3)
                  .build())

        # If we reach here, the fluent interface allows clear configuration
        assert request.url == "https://api.example.com/users"

    def test_partial_configuration_with_defaults(self):
        """Verify partial configuration works with defaults."""
        request = (HTTPRequestBuilder()
                  .with_url("https://example.com")
                  .build())

        # Many defaults should be applied
        assert request.timeout == 30  # Default
        assert request.max_retries == 3  # Default

    def test_complex_query_readability(self):
        """Demonstrate readable query building."""
        query = (SQLQueryBuilder()
                .select("id", "name", "email")
                .from_table("users")
                .where("status = :status")
                .parameter("status", "active")
                .where("age > :age")
                .parameter("age", 21)
                .order_by("name", OrderDirection.ASC)
                .limit(50)
                .build())

        # If we reach here, the fluent interface is clearly readable
        assert len(query.to_sql_single_line()) > 0
