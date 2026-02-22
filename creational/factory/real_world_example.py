"""
Real-world Factory Method: HTTP Client Factory for Multiple API Services.

This example demonstrates a realistic use case where different API services 
require different HTTP configurations, retry policies, and headers. The Factory 
Method pattern abstracts away these differences from the client code.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import json


class APIService(ABC):
    """
    Abstract Product: API Service Client.
    
    Defines the common interface that all concrete API clients must implement.
    """

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Return the configuration for this API service."""
        pass

    @abstractmethod
    def build_headers(self) -> Dict[str, str]:
        """Build request headers specific to this API."""
        pass

    @abstractmethod
    def make_request(self, endpoint: str, method: str = "GET") -> str:
        """
        Simulate making an HTTP request to the API.
        
        Args:
            endpoint: The API endpoint path.
            method: The HTTP method (GET, POST, etc.)
            
        Returns:
            A simulated response from the API.
        """
        pass


class RESTfulAPIService(APIService):
    """
    Concrete Product: RESTful API Service.
    
    Implements a standard REST API client with JSON payloads and 
    standard HTTP methods.
    """

    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.timeout = 30
        self.retries = 3

    def get_config(self) -> Dict[str, Any]:
        """Return REST-specific configuration."""
        return {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "retries": self.retries,
            "protocol": "REST",
            "content_type": "application/json"
        }

    def build_headers(self) -> Dict[str, str]:
        """Build REST API headers."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "PythonClientV1.0"
        }

    def make_request(self, endpoint: str, method: str = "GET") -> str:
        """Simulate REST API request."""
        url = f"{self.base_url}{endpoint}"
        headers = self.build_headers()
        return (
            f"REST Request: {method} {url}\n"
            f"Headers: {json.dumps(headers, indent=2)}\n"
            f"Response: 200 OK (JSON payload received)"
        )


class GraphQLAPIService(APIService):
    """
    Concrete Product: GraphQL API Service.
    
    Implements a GraphQL client that always uses POST requests 
    and sends queries as JSON payloads.
    """

    def __init__(self, base_url: str = "https://graphql.example.com/query"):
        self.base_url = base_url
        self.timeout = 45
        self.batch_size = 10

    def get_config(self) -> Dict[str, Any]:
        """Return GraphQL-specific configuration."""
        return {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "batch_size": self.batch_size,
            "protocol": "GraphQL",
            "introspection_enabled": True
        }

    def build_headers(self) -> Dict[str, str]:
        """Build GraphQL API headers."""
        return {
            "Content-Type": "application/json",
            "X-GraphQL-Client": "PythonClientV1.0",
            "Accept": "application/json"
        }

    def make_request(self, endpoint: str, method: str = "POST") -> str:
        """Simulate GraphQL query request (always POST)."""
        headers = self.build_headers()
        query = '{ user { id name email } }'
        return (
            f"GraphQL Request: POST {self.base_url}\n"
            f"Headers: {json.dumps(headers, indent=2)}\n"
            f"Query: {query}\n"
            f"Response: 200 OK (GraphQL JSON response received)"
        )


class SOAPAPIService(APIService):
    """
    Concrete Product: SOAP API Service.
    
    Implements a SOAP client with XML payloads, WSDL support, and 
    enhanced authentication headers.
    """

    def __init__(self, wsdl_url: str = "https://soap.example.com/service?wsdl"):
        self.wsdl_url = wsdl_url
        self.timeout = 60
        self.soap_version = "1.2"

    def get_config(self) -> Dict[str, Any]:
        """Return SOAP-specific configuration."""
        return {
            "wsdl_url": self.wsdl_url,
            "timeout": self.timeout,
            "soap_version": self.soap_version,
            "protocol": "SOAP",
            "ws_security": True
        }

    def build_headers(self) -> Dict[str, str]:
        """Build SOAP API headers with WS-Security."""
        return {
            "Content-Type": f"application/soap+xml; charset=UTF-8 (version {self.soap_version})",
            "SOAPAction": "http://example.com/GetUser",
            "Authorization": "Bearer ws-security-token-xyz"
        }

    def make_request(self, endpoint: str, method: str = "POST") -> str:
        """Simulate SOAP request with XML envelope."""
        headers = self.build_headers()
        soap_envelope = (
            '<?xml version="1.0"?>\n'
            '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
            '  <soap:Body>...</soap:Body>\n'
            '</soap:Envelope>'
        )
        return (
            f"SOAP Request: POST {endpoint}\n"
            f"Headers: {json.dumps(headers, indent=2)}\n"
            f"Envelope:\n{soap_envelope}\n"
            f"Response: 200 OK (SOAP XML response received)"
        )


class APIServiceFactory(ABC):
    """
    Abstract Creator (Factory).
    
    Declares the factory method for creating API service clients 
    and provides template methods that use these services.
    """

    @abstractmethod
    def create_api_service(self) -> APIService:
        """
        Factory method: Create an API service client.
        
        Returns:
            An APIService instance of the appropriate type.
        """
        pass

    def call_api(self, endpoint: str) -> str:
        """
        Template method: Uses the factory method to call an API.
        
        This demonstrates how the base class provides a common workflow 
        while delegating the specific API client instantiation to subclasses.
        
        Args:
            endpoint: The API endpoint to call.
            
        Returns:
            The result of the API call.
        """
        service = self.create_api_service()
        config = service.get_config()
        response = service.make_request(endpoint, method="GET")
        
        return (
            f"API Configuration: {config}\n"
            f"\n{response}"
        )


class RESTfulAPIFactory(APIServiceFactory):
    """
    Concrete Creator: Creates RESTful API Service clients.
    """

    def create_api_service(self) -> APIService:
        """
        Create a RESTful API service.
        
        Returns:
            A RESTfulAPIService configured for the application.
        """
        return RESTfulAPIService(base_url="https://api.rest.example.com")


class GraphQLAPIFactory(APIServiceFactory):
    """
    Concrete Creator: Creates GraphQL API Service clients.
    """

    def create_api_service(self) -> APIService:
        """
        Create a GraphQL API service.
        
        Returns:
            A GraphQLAPIService configured for the application.
        """
        return GraphQLAPIService(base_url="https://graphql.example.com/query")


class SOAPAPIFactory(APIServiceFactory):
    """
    Concrete Creator: Creates SOAP API Service clients.
    """

    def create_api_service(self) -> APIService:
        """
        Create a SOAP API service.
        
        Returns:
            A SOAPAPIService configured for the application.
        """
        return SOAPAPIService(wsdl_url="https://soap.example.com/service?wsdl")


class APIServiceRegistry:
    """
    Registry Enhancement: Centralized management of API service factories.
    
    Allows runtime selection of API factories without knowing concrete types.
    This is useful when the API type is determined by configuration or user input.
    """

    def __init__(self):
        self._factories: Dict[str, APIServiceFactory] = {
            "rest": RESTfulAPIFactory(),
            "graphql": GraphQLAPIFactory(),
            "soap": SOAPAPIFactory(),
        }

    def get_factory(self, api_type: str) -> APIServiceFactory:
        """
        Retrieve a factory for the specified API type.
        
        Args:
            api_type: The API type (e.g., "rest", "graphql", "soap").
            
        Returns:
            The corresponding APIServiceFactory.
            
        Raises:
            ValueError: If the API type is not registered.
        """
        if api_type not in self._factories:
            raise ValueError(
                f"Unknown API type: {api_type}\n"
                f"Available types: {list(self._factories.keys())}"
            )
        return self._factories[api_type]

    def call_api(self, api_type: str, endpoint: str) -> str:
        """
        Convenient method to call an API by type without knowing the factory.
        
        Args:
            api_type: The API type to use.
            endpoint: The API endpoint to call.
            
        Returns:
            The result of the API call.
        """
        factory = self.get_factory(api_type)
        return factory.call_api(endpoint)

    def register_factory(self, api_type: str, factory: APIServiceFactory) -> None:
        """
        Register a custom factory for a specific API type.
        
        This allows adding support for new API types at runtime.
        
        Args:
            api_type: The name of the API type.
            factory: The APIServiceFactory instance to register.
        """
        self._factories[api_type] = factory


def simulate_microservice_architecture():
    """
    Simulate a microservice architecture where different services 
    use different API types to communicate.
    """
    from typing import List

    services_config: List[tuple[str, str]] = [
        ("rest", "/api/users/123"),
        ("graphql", "/query?query={user{id,name}}"),
        ("soap", "/soap-service"),
    ]

    registry = APIServiceRegistry()

    results = []
    for api_type, endpoint in services_config:
        try:
            result = registry.call_api(api_type, endpoint)
            results.append(f"Service [{api_type.upper()}]:\n{result}\n")
        except ValueError as e:
            results.append(f"Error: {e}\n")

    return "\n---\n".join(results)
