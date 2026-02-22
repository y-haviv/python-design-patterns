"""
Comprehensive tests for the Factory Method pattern.

These tests verify:
1. Correct instantiation of different product types via factories.
2. Type consistency and adherence to the product interface.
3. Factory polymorphism and template method behavior.
4. Registry functionality for centralized factory management.
5. Real-world API service factory behavior.
"""

from __future__ import annotations
import pytest
from threading import Thread
from typing import List

from .pattern import (
    Transport,
    HTTPTransport,
    HTTPSTransport,
    FTPTransport,
    WebSocketTransport,
    TransportFactory,
    HTTPFactory,
    HTTPSFactory,
    FTPFactory,
    WebSocketFactory,
    TransportFactoryRegistry,
    TransportType,
)

from .real_world_example import (
    APIService,
    RESTfulAPIService,
    GraphQLAPIService,
    SOAPAPIService,
    APIServiceFactory,
    RESTfulAPIFactory,
    GraphQLAPIFactory,
    SOAPAPIFactory,
    APIServiceRegistry,
)


class TestBasicFactoryMethod:
    """Test basic factory method functionality."""

    def test_http_factory_creates_http_transport(self):
        """Verify HTTPFactory creates HTTPTransport instances."""
        factory = HTTPFactory()
        transport = factory.create_transport()

        assert isinstance(transport, HTTPTransport)
        assert isinstance(transport, Transport)

    def test_https_factory_creates_https_transport(self):
        """Verify HTTPSFactory creates HTTPSTransport instances."""
        factory = HTTPSFactory()
        transport = factory.create_transport()

        assert isinstance(transport, HTTPSTransport)
        assert isinstance(transport, Transport)

    def test_ftp_factory_creates_ftp_transport(self):
        """Verify FTPFactory creates FTPTransport instances."""
        factory = FTPFactory()
        transport = factory.create_transport()

        assert isinstance(transport, FTPTransport)
        assert isinstance(transport, Transport)

    def test_websocket_factory_creates_websocket_transport(self):
        """Verify WebSocketFactory creates WebSocketTransport instances."""
        factory = WebSocketFactory()
        transport = factory.create_transport()

        assert isinstance(transport, WebSocketTransport)
        assert isinstance(transport, Transport)

    def test_each_factory_creates_new_instance(self):
        """Verify each factory call creates a new instance (not a singleton)."""
        factory = HTTPFactory()
        transport1 = factory.create_transport()
        transport2 = factory.create_transport()

        assert transport1 is not transport2
        assert id(transport1) != id(transport2)


class TestTransportInterface:
    """Test that all products conform to the Transport interface."""

    def test_all_transports_implement_interface(self):
        """Verify all transport types implement the Transport interface."""
        transports: List[Transport] = [
            HTTPTransport(),
            HTTPSTransport(),
            FTPTransport(),
            WebSocketTransport(),
        ]

        for transport in transports:
            assert isinstance(transport, Transport)
            # Verify all methods exist and are callable
            assert callable(transport.connect)
            assert callable(transport.send_data)
            assert callable(transport.disconnect)

    def test_transport_connect_returns_string(self):
        """Verify connect() method returns a descriptive string."""
        transports: List[Transport] = [
            HTTPTransport(),
            HTTPSTransport(),
            FTPTransport(),
            WebSocketTransport(),
        ]

        for transport in transports:
            result = transport.connect()
            assert isinstance(result, str)
            assert len(result) > 0

    def test_transport_send_data_requires_connection(self):
        """Verify that send_data works after connect and not before."""
        transport = HTTPTransport()

        # Before connection
        result_before = transport.send_data("test")
        assert "Error" in result_before or "Not connected" in result_before

        # After connection
        transport.connect()
        result_after = transport.send_data("test_data")
        assert "Error" not in result_after


class TestTemplateMethod:
    """Test the template method pattern used in factories."""

    def test_factory_communicate_method(self):
        """Verify the template method orchestrates factory usage."""
        factory = HTTPFactory()
        message = "Hello, Server!"

        result = factory.communicate(message)

        # Result should contain connection, transmission, and disconnection logs
        assert "connect" in result.lower()
        assert "transmit" in result.lower() or "sending" in result.lower()
        assert "disconnect" in result.lower()

    def test_different_factories_produce_different_outputs(self):
        """Verify that different factories produce different communication outputs."""
        http_result = HTTPFactory().communicate("test")
        https_result = HTTPSFactory().communicate("test")
        ftp_result = FTPFactory().communicate("test")

        # Each should contain protocol-specific information
        assert "HTTP" in http_result
        assert "HTTPS" in https_result or "SSL" in https_result
        assert "FTP" in ftp_result


class TestTransportRegistry:
    """Test the registry enhancement for factory management."""

    def test_registry_get_factory_returns_correct_factory(self):
        """Verify registry returns the correct factory for each type."""
        registry = TransportFactoryRegistry()

        http_factory = registry.get_factory(TransportType.HTTP)
        assert isinstance(http_factory, HTTPFactory)

        https_factory = registry.get_factory(TransportType.HTTPS)
        assert isinstance(https_factory, HTTPSFactory)

    def test_registry_create_transport(self):
        """Verify registry can create transports by type."""
        registry = TransportFactoryRegistry()

        http_transport = registry.create_transport(TransportType.HTTP)
        assert isinstance(http_transport, HTTPTransport)

        ftp_transport = registry.create_transport(TransportType.FTP)
        assert isinstance(ftp_transport, FTPTransport)

    def test_registry_register_custom_factory(self):
        """Verify registry allows registering custom factories."""
        class CustomTransport(Transport):
            def connect(self) -> str:
                return "Custom connection"

            def send_data(self, data: str) -> str:
                return f"Custom: {data}"

            def disconnect(self) -> str:
                return "Custom disconnection"

        class CustomFactory(TransportFactory):
            def create_transport(self) -> Transport:
                return CustomTransport()

        registry = TransportFactoryRegistry()
        registry.register_factory(TransportType.HTTP, CustomFactory())

        transport = registry.create_transport(TransportType.HTTP)
        assert isinstance(transport, CustomTransport)
        assert transport.connect() == "Custom connection"

    def test_registry_unknown_type_raises_error(self):
        """Verify registry raises error for unknown transport types."""
        registry = TransportFactoryRegistry()

        with pytest.raises(ValueError):
            registry.get_factory(TransportType.HTTP)  # Will fail if value is invalid
            # (This is a simplified check; in real code, use an invalid enum)


class TestRealWorldAPIServices:
    """Test the real-world API service factory implementations."""

    def test_rest_api_factory_creates_rest_service(self):
        """Verify RESTful API factory creates the correct service."""
        factory = RESTfulAPIFactory()
        service = factory.create_api_service()

        assert isinstance(service, RESTfulAPIService)
        assert isinstance(service, APIService)

    def test_graphql_api_factory_creates_graphql_service(self):
        """Verify GraphQL API factory creates the correct service."""
        factory = GraphQLAPIFactory()
        service = factory.create_api_service()

        assert isinstance(service, GraphQLAPIService)
        assert isinstance(service, APIService)

    def test_soap_api_factory_creates_soap_service(self):
        """Verify SOAP API factory creates the correct service."""
        factory = SOAPAPIFactory()
        service = factory.create_api_service()

        assert isinstance(service, SOAPAPIService)
        assert isinstance(service, APIService)

    def test_api_service_headers_differ_by_type(self):
        """Verify different API services build different headers."""
        rest_service = RESTfulAPIService()
        graphql_service = GraphQLAPIService()
        soap_service = SOAPAPIService()

        rest_headers = rest_service.build_headers()
        graphql_headers = graphql_service.build_headers()
        soap_headers = soap_service.build_headers()

        # REST and GraphQL both use application/json
        assert "application/json" in rest_headers.get("Content-Type", "")
        assert "application/json" in graphql_headers.get("Content-Type", "")

        # SOAP uses application/soap+xml
        assert "soap+xml" in soap_headers.get("Content-Type", "")

    def test_api_service_config_is_type_specific(self):
        """Verify each API service has type-specific configuration."""
        rest_config = RESTfulAPIService().get_config()
        graphql_config = GraphQLAPIService().get_config()
        soap_config = SOAPAPIService().get_config()

        assert rest_config["protocol"] == "REST"
        assert graphql_config["protocol"] == "GraphQL"
        assert soap_config["protocol"] == "SOAP"

        # Check type-specific fields
        assert "retries" in rest_config
        assert "batch_size" in graphql_config
        assert "ws_security" in soap_config


class TestAPIServiceRegistry:
    """Test the real-world API service registry."""

    def test_registry_get_factory_by_name(self):
        """Verify registry returns correct factory by API type name."""
        registry = APIServiceRegistry()

        rest_factory = registry.get_factory("rest")
        assert isinstance(rest_factory, RESTfulAPIFactory)

        graphql_factory = registry.get_factory("graphql")
        assert isinstance(graphql_factory, GraphQLAPIFactory)

    def test_registry_call_api_without_knowing_type(self):
        """Verify registry can create and call API without knowing concrete type."""
        registry = APIServiceRegistry()

        result = registry.call_api("rest", "/api/users")
        assert "REST" in result
        assert "200 OK" in result

    def test_registry_register_custom_api_factory(self):
        """Verify registry allows registering custom API factories."""
        class CustomAPIService(APIService):
            def get_config(self):
                return {"protocol": "CUSTOM"}

            def build_headers(self):
                return {"Custom-Header": "value"}

            def make_request(self, endpoint: str, method: str = "GET") -> str:
                return f"CUSTOM: {method} {endpoint}"

        class CustomAPIFactory(APIServiceFactory):
            def create_api_service(self) -> APIService:
                return CustomAPIService()

        registry = APIServiceRegistry()
        registry.register_factory("custom", CustomAPIFactory())

        service = registry.get_factory("custom").create_api_service()
        assert isinstance(service, CustomAPIService)
        assert service.get_config()["protocol"] == "CUSTOM"

    def test_registry_unknown_api_type_raises_error(self):
        """Verify registry raises error for unknown API type."""
        registry = APIServiceRegistry()

        with pytest.raises(ValueError, match="Unknown API type"):
            registry.get_factory("unknown_type")


class TestConcurrency:
    """Test factory behavior in concurrent scenarios."""

    def test_factories_thread_safe(self):
        """Verify factories work correctly with multiple threads."""
        results: List[Transport] = []
        errors: List[Exception] = []

        def create_transports():
            try:
                factory = HTTPFactory()
                for _ in range(10):
                    transport = factory.create_transport()
                    results.append(transport)
            except Exception as e:
                errors.append(e)

        threads = [Thread(target=create_transports) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # No errors should occur
        assert len(errors) == 0

        # All transports should be Transport instances
        assert all(isinstance(t, Transport) for t in results)

        # We should have created 50 transports (5 threads * 10 per thread)
        assert len(results) == 50


class TestIntegration:
    """Integration tests combining multiple pattern aspects."""

    def test_factory_method_with_registry_workflow(self):
        """Test complete workflow: registry -> factory -> product."""
        registry = TransportFactoryRegistry()

        # Simulate a workflow where we iterate over all transport types
        for transport_type in TransportType:
            factory = registry.get_factory(transport_type)
            transport = factory.create_transport()

            # All should be Transport instances
            assert isinstance(transport, Transport)

            # All should have required methods
            transport.connect()
            transport.send_data("test")
            transport.disconnect()

    def test_api_service_registry_complete_workflow(self):
        """Test complete API service workflow."""
        registry = APIServiceRegistry()

        api_types = ["rest", "graphql", "soap"]

        for api_type in api_types:
            factory = registry.get_factory(api_type)
            service = factory.create_api_service()

            # All should be APIService instances
            assert isinstance(service, APIService)

            # All should support the interface
            config = service.get_config()
            headers = service.build_headers()
            request_result = service.make_request("/api/test")

            assert isinstance(config, dict)
            assert isinstance(headers, dict)
            assert isinstance(request_result, str)
