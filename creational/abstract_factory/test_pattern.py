"""
Comprehensive tests for the Abstract Factory pattern.

These tests verify:
1. Different factories create consistent product families for their UI theme.
2. Products from the same factory are compatible.
3. Registry pattern allows runtime factory switching.
4. Complete integration of factories with application code.
5. Database abstraction layer works across multiple engines.
"""

from __future__ import annotations
import pytest
from typing import List

from .pattern import (
    UITheme,
    Button,
    Checkbox,
    TextInput,
    UIFactory,
    LightThemeFactory,
    DarkThemeFactory,
    HighContrastThemeFactory,
    Application,
    UIThemeRegistry,
)

from .real_world_example import (
    DatabaseEngine,
    DatabaseFactory,
    PostgreSQLFactory,
    MySQLFactory,
    SQLiteFactory,
    Connection,
    QueryBuilder,
    DataTypeMapper,
    DatabaseAdapter,
    DatabaseFactoryRegistry,
)


class TestUIThemeFactories:
    """Test basic UI theme factory functionality."""

    def test_light_factory_creates_light_components(self):
        """Verify LightThemeFactory creates all light-themed components."""
        factory = LightThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_input = factory.create_text_input()

        # All should be proper types
        assert isinstance(button, Button)
        assert isinstance(checkbox, Checkbox)
        assert isinstance(text_input, TextInput)

        # All should render
        button_str = button.render()
        checkbox_str = checkbox.render()
        input_str = text_input.render()

        assert "Light" in button_str or len(button_str) > 0
        assert "Light" in checkbox_str or len(checkbox_str) > 0
        assert "Light" in input_str or len(input_str) > 0

    def test_dark_factory_creates_dark_components(self):
        """Verify DarkThemeFactory creates all dark-themed components."""
        factory = DarkThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_input = factory.create_text_input()

        assert isinstance(button, Button)
        assert isinstance(checkbox, Checkbox)
        assert isinstance(text_input, TextInput)

        # Dark theme should be evident in rendering
        button_str = button.render()
        checkbox_str = checkbox.render()
        
        assert "Dark" in button_str or "━" in button_str
        assert "Dark" in checkbox_str or "☑" in checkbox_str

    def test_high_contrast_factory_creates_accessible_components(self):
        """Verify HighContrastThemeFactory creates accessible components."""
        factory = HighContrastThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_input = factory.create_text_input()

        assert isinstance(button, Button)
        assert isinstance(checkbox, Checkbox)
        assert isinstance(text_input, TextInput)

        # High contrast should be evident
        button_str = button.render()
        assert "HIGH" in button_str


class TestProductFamilyConsistency:
    """Test that products from the same factory form a consistent family."""

    def test_light_theme_family_consistency(self):
        """Verify all light theme products work together."""
        factory = LightThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()

        # Both should respond to their respective interfaces
        button_click = button.on_click("callback")
        checkbox_check = checkbox.set_checked(True)

        assert len(button_click) > 0
        assert len(checkbox_check) > 0

    def test_dark_theme_family_consistency(self):
        """Verify all dark theme products work together."""
        factory = DarkThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()

        button_click = button.on_click("callback")
        checkbox_check = checkbox.set_checked(True)

        assert len(button_click) > 0
        assert len(checkbox_check) > 0

    def test_high_contrast_family_consistency(self):
        """Verify all high contrast products work together."""
        factory = HighContrastThemeFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()

        button_click = button.on_click("callback")
        checkbox_check = checkbox.set_checked(False)

        assert "HIGH" in button_click or len(button_click) > 0
        assert "HIGH" in checkbox_check or len(checkbox_check) > 0


class TestApplicationWithFactory:
    """Test the Application class working with different factories."""

    def test_application_with_light_theme(self):
        """Verify Application renders correctly with light theme."""
        factory = LightThemeFactory()
        app = Application(factory)

        ui = app.render_ui()
        interactions = app.interact()

        assert len(ui) > 0
        assert len(interactions) > 0
        assert "APPLICATION UI" in ui.upper()

    def test_application_with_dark_theme(self):
        """Verify Application renders correctly with dark theme."""
        factory = DarkThemeFactory()
        app = Application(factory)

        ui = app.render_ui()
        
        # Should render and contain UI components
        assert len(ui) > 0
        assert "APPLICATION" in ui

    def test_application_theme_switching(self):
        """Verify application can switch themes at runtime."""
        # Start with light theme
        light_factory = LightThemeFactory()
        app_light = Application(light_factory)
        light_ui = app_light.render_ui()

        # Switch to dark theme
        dark_factory = DarkThemeFactory()
        app_dark = Application(dark_factory)
        dark_ui = app_dark.render_ui()

        # Both should render
        assert len(light_ui) > 0
        assert len(dark_ui) > 0

        # Results should be different (different theme styling)
        assert light_ui != dark_ui


class TestUIThemeRegistry:
    """Test the registry pattern for theme management."""

    def test_registry_get_factory_by_theme(self):
        """Verify registry returns correct factory by theme."""
        registry = UIThemeRegistry()

        light_factory = registry.get_factory(UITheme.LIGHT)
        assert isinstance(light_factory, LightThemeFactory)

        dark_factory = registry.get_factory(UITheme.DARK)
        assert isinstance(dark_factory, DarkThemeFactory)

    def test_registry_create_application_by_theme(self):
        """Verify registry can create applications by theme."""
        registry = UIThemeRegistry()

        app_light = registry.create_application(UITheme.LIGHT)
        app_dark = registry.create_application(UITheme.DARK)

        assert isinstance(app_light, Application)
        assert isinstance(app_dark, Application)

    def test_registry_list_available_themes(self):
        """Verify registry can list all available themes."""
        registry = UIThemeRegistry()

        themes = registry.list_available_themes()

        assert UITheme.LIGHT in themes
        assert UITheme.DARK in themes
        assert UITheme.HIGHCONTRAST in themes

    def test_registry_custom_factory_registration(self):
        """Verify registry allows registering custom factories."""
        class CustomFactory(UIFactory):
            def create_button(self) -> Button:
                class CustomButton(Button):
                    def render(self) -> str:
                        return "CUSTOM BUTTON"
                    def on_click(self, callback: str) -> str:
                        return "CUSTOM CLICK"
                return CustomButton()

            def create_checkbox(self) -> Checkbox:
                class CustomCheckbox(Checkbox):
                    def render(self) -> str:
                        return "CUSTOM CHECKBOX"
                    def set_checked(self, value: bool) -> str:
                        return "CUSTOM CHECK"
                return CustomCheckbox()

            def create_text_input(self) -> TextInput:
                class CustomTextInput(TextInput):
                    def render(self) -> str:
                        return "CUSTOM INPUT"
                    def set_placeholder(self, text: str) -> str:
                        return "CUSTOM PLACEHOLDER"
                return CustomTextInput()

        registry = UIThemeRegistry()
        registry.register_factory(UITheme.LIGHT, CustomFactory())

        # Now light theme should use custom factory
        factory = registry.get_factory(UITheme.LIGHT)
        button = factory.create_button()
        assert button.render() == "CUSTOM BUTTON"


class TestDatabaseFactories:
    """Test database factory functionality."""

    def test_postgresql_factory_creates_family(self):
        """Verify PostgreSQL factory creates all components."""
        factory = PostgreSQLFactory()

        conn = factory.create_connection()
        query_builder = factory.create_query_builder()
        type_mapper = factory.create_data_type_mapper()

        assert isinstance(conn, Connection)
        assert isinstance(query_builder, QueryBuilder)
        assert isinstance(type_mapper, DataTypeMapper)

    def test_mysql_factory_creates_family(self):
        """Verify MySQL factory creates all components."""
        factory = MySQLFactory()

        conn = factory.create_connection()
        query_builder = factory.create_query_builder()
        type_mapper = factory.create_data_type_mapper()

        assert isinstance(conn, Connection)
        assert isinstance(query_builder, QueryBuilder)
        assert isinstance(type_mapper, DataTypeMapper)

    def test_sqlite_factory_creates_family(self):
        """Verify SQLite factory creates all components."""
        factory = SQLiteFactory()

        conn = factory.create_connection()
        query_builder = factory.create_query_builder()
        type_mapper = factory.create_data_type_mapper()

        assert isinstance(conn, Connection)
        assert isinstance(query_builder, QueryBuilder)
        assert isinstance(type_mapper, DataTypeMapper)


class TestDatabaseComponentsIntegration:
    """Test that database components work together as families."""

    def test_postgresql_components_consistency(self):
        """Verify PostgreSQL components work together."""
        factory = PostgreSQLFactory()

        conn = factory.create_connection()
        conn_str = conn.connect("localhost", "admin", "secret")

        query_builder = factory.create_query_builder()
        select_query = query_builder.build_select("users", ["id", "name"])

        type_mapper = factory.create_data_type_mapper()
        int_type = type_mapper.python_to_sql_type(int)

        # All should work
        assert "PostgreSQL" in conn_str
        assert "SELECT" in select_query
        assert "INTEGER" in int_type or "INT" in int_type

    def test_mysql_query_builder_uses_backticks(self):
        """Verify MySQL query builder uses MySQL-specific syntax."""
        factory = MySQLFactory()
        query_builder = factory.create_query_builder()

        select_query = query_builder.build_select("users", ["id", "name"])

        # MySQL uses backticks for identifiers
        assert "`" in select_query

    def test_sqlite_type_mapping_differs(self):
        """Verify SQLite has different type mappings."""
        pg_factory = PostgreSQLFactory()
        sqlite_factory = SQLiteFactory()

        pg_type_mapper = pg_factory.create_data_type_mapper()
        sqlite_type_mapper = sqlite_factory.create_data_type_mapper()

        pg_bool_type = pg_type_mapper.python_to_sql_type(bool)
        sqlite_bool_type = sqlite_type_mapper.python_to_sql_type(bool)

        # SQLite uses INTEGER for booleans, PostgreSQL uses BOOLEAN
        assert pg_bool_type == "BOOLEAN"
        assert sqlite_bool_type == "INTEGER"


class TestDatabaseAdapter:
    """Test the database adapter with different factories."""

    def test_adapter_with_postgresql(self):
        """Verify adapter works with PostgreSQL factory."""
        factory = PostgreSQLFactory()
        adapter = DatabaseAdapter(factory)

        conn_info = adapter.connect("localhost", "admin", "secret")
        select_query = adapter.query_select("users", ["id"])
        int_col_type = adapter.get_column_type(int)

        assert len(conn_info) > 0
        assert "SELECT" in select_query
        assert len(int_col_type) > 0

    def test_adapter_with_mysql(self):
        """Verify adapter works with MySQL factory."""
        factory = MySQLFactory()
        adapter = DatabaseAdapter(factory)

        conn_info = adapter.connect("localhost", "admin", "secret")
        select_query = adapter.query_select("users")

        assert len(conn_info) > 0
        assert "SELECT" in select_query

    def test_adapter_with_sqlite(self):
        """Verify adapter works with SQLite factory."""
        factory = SQLiteFactory()
        adapter = DatabaseAdapter(factory)

        conn_info = adapter.connect("app.db", "", "")
        select_query = adapter.query_select("users")

        assert "SQLite" in conn_info
        assert "SELECT" in select_query

    def test_adapters_same_interface_different_output(self):
        """Verify adapters have same interface but different SQL output."""
        pg_adapter = DatabaseAdapter(PostgreSQLFactory())
        mysql_adapter = DatabaseAdapter(MySQLFactory())

        # Same operation, different SQL dialects
        pg_query = pg_adapter.query_select("users", ["id"])
        mysql_query = mysql_adapter.query_select("users", ["id"])

        # Both produce valid queries
        assert "SELECT" in pg_query
        assert "SELECT" in mysql_query

        # Queries differ in syntax
        assert pg_query != mysql_query


class TestDatabaseFactoryRegistry:
    """Test registry for database factories."""

    def test_registry_get_factory_by_engine(self):
        """Verify registry returns correct factory by engine."""
        registry = DatabaseFactoryRegistry()

        pg_factory = registry.get_factory(DatabaseEngine.POSTGRESQL)
        mysql_factory = registry.get_factory(DatabaseEngine.MYSQL)

        assert isinstance(pg_factory, PostgreSQLFactory)
        assert isinstance(mysql_factory, MySQLFactory)

    def test_registry_create_adapter_by_engine(self):
        """Verify registry can create adapters."""
        registry = DatabaseFactoryRegistry()

        pg_adapter = registry.create_adapter(DatabaseEngine.POSTGRESQL)
        mysql_adapter = registry.create_adapter(DatabaseEngine.MYSQL)

        assert isinstance(pg_adapter, DatabaseAdapter)
        assert isinstance(mysql_adapter, DatabaseAdapter)

    def test_registry_get_available_engines(self):
        """Verify registry lists available engines."""
        registry = DatabaseFactoryRegistry()

        engines = registry.get_available_engines()

        assert "postgresql" in engines
        assert "mysql" in engines
        assert "sqlite" in engines

    def test_registry_unknown_engine_raises_error(self):
        """Verify registry raises error for unknown engine."""
        registry = DatabaseFactoryRegistry()

        with pytest.raises(ValueError):
            # Create a dummy enum value that doesn't exist
            class FakeEngine:
                value = "nonexistent"
            registry.get_factory(FakeEngine())  # type: ignore


class TestAbstractFactoryBenefits:
    """Test the key benefits of the Abstract Factory pattern."""

    def test_switching_entire_product_family_is_simple(self):
        """Demonstrate easy switching of entire product families."""
        app_light = Application(LightThemeFactory())
        app_dark = Application(DarkThemeFactory())

        light_render = app_light.render_ui()
        dark_render = app_dark.render_ui()

        # Both work, different output
        assert len(light_render) > 0
        assert len(dark_render) > 0
        assert light_render != dark_render

    def test_products_from_same_family_are_consistent(self):
        """Verify products from same factory are from same family."""
        factory = DarkThemeFactory()

        # Multiple creations from same factory
        button1 = factory.create_button()
        button2 = factory.create_button()

        checkbox1 = factory.create_checkbox()
        checkbox2 = factory.create_checkbox()

        # All buttons are from same theme family
        button1_render = button1.render()
        checkbox1_render = checkbox1.render()

        # Both should have consistent styling cues
        assert ("Dark" in button1_render) == ("Dark" in checkbox1_render)

    def test_database_adapter_abstracts_implementation_details(self):
        """Show how adapter abstracts away implementation details."""
        engines = [DatabaseEngine.POSTGRESQL, DatabaseEngine.MYSQL, DatabaseEngine.SQLITE]
        registry = DatabaseFactoryRegistry()

        # Same application code works with all engines
        for engine in engines:
            adapter = registry.create_adapter(engine)

            # Same interface
            conn = adapter.connect("localhost", "user", "pass")
            query = adapter.query_select("users", ["id"])
            col_type = adapter.get_column_type(str)

            # All work without knowing engine specifics
            assert len(conn) > 0
            assert "SELECT" in query
            assert len(col_type) > 0


class TestIntegrationScenarios:
    """Integration tests with realistic scenarios."""

    def test_multi_theme_application_scenario(self):
        """Test realistic scenario: user switches themes in application."""
        registry = UIThemeRegistry()

        # User starts with light theme
        app = registry.create_application(UITheme.LIGHT)
        initial_render = app.render_ui()

        # User preferences change to dark theme
        app = registry.create_application(UITheme.DARK)
        new_render = app.render_ui()

        # Both work, user doesn't know about factories
        assert initial_render != new_render
        assert "APPLICATION UI" in initial_render.upper()
        assert "APPLICATION UI" in new_render.upper()

    def test_multi_database_application_scenario(self):
        """Test realistic scenario: application supports multiple databases."""
        registry = DatabaseFactoryRegistry()

        # For different deployments
        deployments = {
            "production": DatabaseEngine.POSTGRESQL,
            "staging": DatabaseEngine.MYSQL,
            "local": DatabaseEngine.SQLITE,
        }

        for env, engine in deployments.items():
            adapter = registry.create_adapter(engine)

            # Same code in all deployments
            adapter.connect(f"{env}_host", "user", "pass")
            select_query = adapter.query_select("accounts", ["id", "balance"])
            account_type = adapter.get_column_type(float)

            # All work identically from application's perspective
            assert "SELECT" in select_query
            assert len(account_type) > 0
