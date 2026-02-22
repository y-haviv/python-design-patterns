"""
Builder Pattern - Structural Implementation.

This module demonstrates the Builder pattern, which provides a way to construct 
complex objects step-by-step. It separates the construction logic from the 
representation, allowing the same construction process to create different 
representations.

The Builder pattern is particularly useful when:
- An object has many optional parameters
- You want a readable, fluent interface for object creation
- You want to ensure objects are created in a valid state
- The construction process has multiple steps that should be reusable
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Type
from enum import Enum


class HTTPMethod(Enum):
    """HTTP request methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class HTTPRequest:
    """
    Complex Product: HTTP Request.
    
    Represents a complete HTTP request with all its components.
    This would be difficult to construct directly due to many parameters.
    """

    method: HTTPMethod
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True
    proxy: Optional[str] = None
    auth_token: Optional[str] = None
    user_agent: str = "Python-HTTPClient/1.0"

    def validate(self) -> bool:
        """
        Validate that the request is properly configured.
        
        Returns:
            True if valid, raises ValueError if invalid.
        """
        if not self.url:
            raise ValueError("URL is required")
        if self.method is None:
            raise ValueError("HTTP method is required")
        if self.method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]:
            if self.body is None or self.body == "":
                # These methods typically require a body, though not strictly
                pass
        return True

    def construct(self) -> str:
        """
        Construct a string representation of the request.
        
        Returns:
            A formatted string showing the complete request.
        """
        lines = []
        lines.append(f"{self.method.value} {self.url}")

        if self.query_params:
            query_str = "&".join(f"{k}={v}" for k, v in self.query_params.items())
            lines[0] += f"?{query_str}"

        lines.append("--- HEADERS ---")
        for key, value in self.headers.items():
            lines.append(f"{key}: {value}")
        lines.append(f"User-Agent: {self.user_agent}")

        if self.auth_token:
            lines.append(f"Authorization: Bearer {self.auth_token}")

        lines.append("--- CONFIGURATION ---")
        lines.append(f"Timeout: {self.timeout}s")
        lines.append(f"Max Retries: {self.max_retries}")
        lines.append(f"Verify SSL: {self.verify_ssl}")
        if self.proxy:
            lines.append(f"Proxy: {self.proxy}")

        if self.body:
            lines.append("--- BODY ---")
            lines.append(self.body)

        return "\n".join(lines)


class HTTPRequestBuilder:
    """
    Concrete Builder: HTTP Request Builder.
    
    Provides a fluent interface for constructing HTTPRequest objects.
    Each method returns self to enable method chaining (fluent interface).
    
    Benefits:
    - Readable: building a complex object reads like English
    - Flexible: can set only the fields you need
    - Maintainable: adding new optional fields only requires a new method
    - Reusable: the same builder can be reused or reset
    """

    def __init__(self) -> None:
        """Initialize the builder with default values."""
        self._method: HTTPMethod = HTTPMethod.GET
        self._url: str = ""
        self._headers: Dict[str, str] = {}
        self._query_params: Dict[str, str] = {}
        self._body: Optional[str] = None
        self._timeout: int = 30
        self._max_retries: int = 3
        self._verify_ssl: bool = True
        self._proxy: Optional[str] = None
        self._auth_token: Optional[str] = None
        self._user_agent: str = "Python-HTTPClient/1.0"

    def with_url(self, url: str) -> HTTPRequestBuilder:
        """
        Set the request URL.
        
        Args:
            url: The target URL (required).
            
        Returns:
            Self for method chaining.
        """
        self._url = url
        return self

    def with_method(self, method: HTTPMethod | str) -> HTTPRequestBuilder:
        """
        Set the HTTP method.
        
        Args:
            method: HTTPMethod enum or string ("GET", "POST", etc.)
            
        Returns:
            Self for method chaining.
        """
        if isinstance(method, str):
            self._method = HTTPMethod[method.upper()]
        else:
            self._method = method
        return self

    def with_header(self, key: str, value: str) -> HTTPRequestBuilder:
        """
        Add a header to the request.
        
        Args:
            key: Header name.
            value: Header value.
            
        Returns:
            Self for method chaining.
        """
        self._headers[key] = value
        return self

    def with_headers(self, headers: Dict[str, str]) -> HTTPRequestBuilder:
        """
        Add multiple headers at once.
        
        Args:
            headers: Dictionary of header key-value pairs.
            
        Returns:
            Self for method chaining.
        """
        self._headers.update(headers)
        return self

    def with_query_param(self, key: str, value: str) -> HTTPRequestBuilder:
        """
        Add a query parameter.
        
        Args:
            key: Parameter name.
            value: Parameter value.
            
        Returns:
            Self for method chaining.
        """
        self._query_params[key] = value
        return self

    def with_query_params(self, params: Dict[str, str]) -> HTTPRequestBuilder:
        """
        Add multiple query parameters at once.
        
        Args:
            params: Dictionary of query parameters.
            
        Returns:
            Self for method chaining.
        """
        self._query_params.update(params)
        return self

    def with_body(self, body: str) -> HTTPRequestBuilder:
        """
        Set the request body (for POST, PUT, PATCH).
        
        Args:
            body: The request body content.
            
        Returns:
            Self for method chaining.
        """
        self._body = body
        return self

    def with_json_body(self, data: Dict[str, Any]) -> HTTPRequestBuilder:
        """
        Set the request body as JSON.
        
        Args:
            data: A dictionary to serialize as JSON.
            
        Returns:
            Self for method chaining.
        """
        import json
        self._body = json.dumps(data)
        self._headers["Content-Type"] = "application/json"
        return self

    def with_timeout(self, seconds: int) -> HTTPRequestBuilder:
        """
        Set the request timeout.
        
        Args:
            seconds: Timeout in seconds.
            
        Returns:
            Self for method chaining.
        """
        self._timeout = seconds
        return self

    def with_max_retries(self, retries: int) -> HTTPRequestBuilder:
        """
        Set the maximum number of retries.
        
        Args:
            retries: Number of retry attempts.
            
        Returns:
            Self for method chaining.
        """
        self._max_retries = retries
        return self

    def with_ssl_verification(self, verify: bool) -> HTTPRequestBuilder:
        """
        Set whether to verify SSL certificates.
        
        Args:
            verify: True to verify, False to skip verification.
            
        Returns:
            Self for method chaining.
        """
        self._verify_ssl = verify
        return self

    def with_proxy(self, proxy_url: str) -> HTTPRequestBuilder:
        """
        Set a proxy for the request.
        
        Args:
            proxy_url: The proxy URL (e.g., "http://proxy.example.com:8080").
            
        Returns:
            Self for method chaining.
        """
        self._proxy = proxy_url
        return self

    def with_auth_bearer_token(self, token: str) -> HTTPRequestBuilder:
        """
        Set bearer token authentication.
        
        Args:
            token: The bearer token.
            
        Returns:
            Self for method chaining.
        """
        self._auth_token = token
        return self

    def with_user_agent(self, user_agent: str) -> HTTPRequestBuilder:
        """
        Set the User-Agent header.
        
        Args:
            user_agent: The User-Agent string.
            
        Returns:
            Self for method chaining.
        """
        self._user_agent = user_agent
        return self

    def reset(self) -> HTTPRequestBuilder:
        """
        Reset the builder to its initial state.
        
        Useful for reusing a builder to create multiple requests.
        
        Returns:
            Self for method chaining.
        """
        self.__init__()
        return self

    def build(self) -> HTTPRequest:
        """
        Build and return the HTTPRequest object.
        
        Validates the request before returning.
        
        Returns:
            A valid HTTPRequest instance.
            
        Raises:
            ValueError: If the request is invalid.
        """
        request = HTTPRequest(
            method=self._method,
            url=self._url,
            headers=self._headers.copy(),
            query_params=self._query_params.copy(),
            body=self._body,
            timeout=self._timeout,
            max_retries=self._max_retries,
            verify_ssl=self._verify_ssl,
            proxy=self._proxy,
            auth_token=self._auth_token,
            user_agent=self._user_agent
        )
        request.validate()
        return request


# ============================================================================
# Complex Product Example 2: Computer Configuration
# ============================================================================


@dataclass
class Computer:
    """
    Complex Product: Computer Configuration.
    
    Represents a computer with various components and specifications.
    This demonstrates how the Builder pattern works with domain objects.
    """

    # Processor
    cpu_cores: int = 4
    cpu_ghz: float = 2.5
    
    # Memory
    ram_gb: int = 8
    
    # Storage
    ssd_gb: int = 256
    has_hdd: bool = False
    hdd_gb: int = 0
    
    # GPU
    has_gpu: bool = False
    gpu_vram_gb: int = 0
    gpu_model: str = ""
    
    # Cooling & Power
    cooling_type: str = "air"  # "air", "liquid", "passive"
    psu_wattage: int = 450
    
    # Features
    has_wifi: bool = True
    has_bluetooth: bool = True
    color: str = "black"

    def validate(self) -> bool:
        """Validate computer configuration."""
        if self.cpu_cores < 1:
            raise ValueError("CPU cores must be at least 1")
        if self.ram_gb < 1:
            raise ValueError("RAM must be at least 1GB")
        if self.ssd_gb < 0:
            raise ValueError("SSD cannot be negative")
        return True

    def estimate_price(self) -> float:
        """Estimate the computer's price."""
        price = 400.0  # Base price
        
        # CPU
        price += self.cpu_cores * 50
        price += self.cpu_ghz * 100
        
        # RAM
        price += self.ram_gb * 80
        
        # Storage
        price += self.ssd_gb * 0.10
        if self.has_hdd:
            price += self.hdd_gb * 0.05
        
        # GPU
        if self.has_gpu:
            price += 300 + (self.gpu_vram_gb * 50)
        
        # Cooling
        if self.cooling_type == "liquid":
            price += 150
        
        # PSU
        price += self.psu_wattage * 0.5
        
        return price

    def specifications_summary(self) -> str:
        """Generate a summary of computer specifications."""
        lines = []
        lines.append("=== COMPUTER SPECIFICATIONS ===")
        lines.append(f"CPU: {self.cpu_cores} cores @ {self.cpu_ghz}GHz")
        lines.append(f"RAM: {self.ram_gb}GB")
        lines.append(f"Storage: {self.ssd_gb}GB SSD" + 
                    (f" + {self.hdd_gb}GB HDD" if self.has_hdd else ""))
        
        if self.has_gpu:
            lines.append(f"GPU: {self.gpu_model} ({self.gpu_vram_gb}GB VRAM)")
        
        lines.append(f"Cooling: {self.cooling_type}")
        lines.append(f"PSU: {self.psu_wattage}W")
        lines.append(f"Connectivity: {"WiFi + " if self.has_wifi else ""}{"Bluetooth" if self.has_bluetooth else "Wired only"}")
        lines.append(f"Color: {self.color}")
        lines.append(f"Estimated Price: ${self.estimate_price():.2f}")
        
        return "\n".join(lines)


class ComputerBuilder:
    """
    Concrete Builder: Computer Configuration Builder.
    
    Provides a fluent interface for building computer configurations.
    This demonstrates the Builder pattern for more complex domain objects.
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._cpu_cores: int = 4
        self._cpu_ghz: float = 2.5
        self._ram_gb: int = 8
        self._ssd_gb: int = 256
        self._has_hdd: bool = False
        self._hdd_gb: int = 0
        self._has_gpu: bool = False
        self._gpu_vram_gb: int = 0
        self._gpu_model: str = ""
        self._cooling_type: str = "air"
        self._psu_wattage: int = 450
        self._has_wifi: bool = True
        self._has_bluetooth: bool = True
        self._color: str = "black"

    def with_cpu(self, cores: int, ghz: float) -> ComputerBuilder:
        """Set CPU specifications."""
        self._cpu_cores = cores
        self._cpu_ghz = ghz
        return self

    def with_ram(self, gb: int) -> ComputerBuilder:
        """Set RAM amount."""
        self._ram_gb = gb
        return self

    def with_ssd(self, gb: int) -> ComputerBuilder:
        """Set SSD storage."""
        self._ssd_gb = gb
        return self

    def with_hdd(self, gb: int) -> ComputerBuilder:
        """Add HDD storage."""
        self._has_hdd = True
        self._hdd_gb = gb
        return self

    def with_gpu(self, model: str, vram_gb: int) -> ComputerBuilder:
        """Add GPU."""
        self._has_gpu = True
        self._gpu_model = model
        self._gpu_vram_gb = vram_gb
        return self

    def with_liquid_cooling(self) -> ComputerBuilder:
        """Use liquid cooling."""
        self._cooling_type = "liquid"
        return self

    def with_psu(self, wattage: int) -> ComputerBuilder:
        """Set power supply wattage."""
        self._psu_wattage = wattage
        return self

    def with_color(self, color: str) -> ComputerBuilder:
        """Set computer color."""
        self._color = color
        return self

    def without_wifi(self) -> ComputerBuilder:
        """Remove WiFi."""
        self._has_wifi = False
        return self

    def without_bluetooth(self) -> ComputerBuilder:
        """Remove Bluetooth."""
        self._has_bluetooth = False
        return self

    def build(self) -> Computer:
        """Build the computer."""
        computer = Computer(
            cpu_cores=self._cpu_cores,
            cpu_ghz=self._cpu_ghz,
            ram_gb=self._ram_gb,
            ssd_gb=self._ssd_gb,
            has_hdd=self._has_hdd,
            hdd_gb=self._hdd_gb,
            has_gpu=self._has_gpu,
            gpu_vram_gb=self._gpu_vram_gb,
            gpu_model=self._gpu_model,
            cooling_type=self._cooling_type,
            psu_wattage=self._psu_wattage,
            has_wifi=self._has_wifi,
            has_bluetooth=self._has_bluetooth,
            color=self._color
        )
        computer.validate()
        return computer


# ============================================================================
# Pre-built Configuration Sets (Director Pattern)
# ============================================================================


class RequestTemplates:
    """
    Director Pattern (Optional Enhancement).
    
    Provides pre-built request templates for common scenarios.
    This eliminates the need to build from scratch for typical use cases.
    """

    @staticmethod
    def get_api_call() -> HTTPRequest:
        """Build a typical RESTful API request."""
        return (HTTPRequestBuilder()
                .with_url("https://api.example.com/v1/users")
                .with_method(HTTPMethod.GET)
                .with_header("Accept", "application/json")
                .with_auth_bearer_token("your-api-key")
                .with_timeout(15)
                .build())

    @staticmethod
    def post_json_data() -> HTTPRequest:
        """Build a POST request with JSON data."""
        return (HTTPRequestBuilder()
                .with_url("https://api.example.com/v1/users")
                .with_method(HTTPMethod.POST)
                .with_json_body({"name": "John", "email": "john@example.com"})
                .with_auth_bearer_token("api-key")
                .build())

    @staticmethod
    def webhook_request() -> HTTPRequest:
        """Build a webhook request with retries."""
        return (HTTPRequestBuilder()
                .with_url("https://webhook.example.com/events")
                .with_method(HTTPMethod.POST)
                .with_header("X-Webhook-Secret", "secret-key")
                .with_max_retries(5)
                .with_timeout(10)
                .build())


class ComputerTemplates:
    """Director Pattern for computers."""

    @staticmethod
    def budget_build() -> Computer:
        """Build a budget computer."""
        return (ComputerBuilder()
                .with_cpu(4, 2.5)
                .with_ram(8)
                .with_ssd(256)
                .build())

    @staticmethod
    def gaming_build() -> Computer:
        """Build a gaming computer."""
        return (ComputerBuilder()
                .with_cpu(16, 4.0)
                .with_ram(32)
                .with_ssd(1024)
                .with_hdd(2048)
                .with_gpu("NVIDIA RTX 4080", 12)
                .with_liquid_cooling()
                .with_psu(1200)
                .with_color("RGB")
                .build())

    @staticmethod
    def workstation_build() -> Computer:
        """Build a professional workstation."""
        return (ComputerBuilder()
                .with_cpu(32, 3.8)
                .with_ram(128)
                .with_ssd(2048)
                .with_gpu("NVIDIA A6000", 48)
                .with_liquid_cooling()
                .with_psu(2000)
                .build())
