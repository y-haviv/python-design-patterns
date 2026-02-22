"""Tests for Proxy Pattern."""
import pytest
from .pattern import (
    RealSubject, Proxy,
    RealImage, ImageProxy,
    DatabaseProxy,
    RealService, ProtectionProxy, ValidationProxy, LoggingProxy
)


class TestBasicProxy:
    def test_proxy_controls_access(self):
        real = RealSubject()
        proxy = Proxy(real)
        
        assert "Proxy" in proxy.request()


class TestImageProxy:
    def test_lazy_loading(self):
        proxy = ImageProxy("image.png")
        assert proxy.display() == "Displaying image.png"


class TestDatabaseProxy:
    def test_caching(self):
        proxy = DatabaseProxy()
        
        result1 = proxy.query("SELECT * FROM users")
        result2 = proxy.query("SELECT * FROM users")
        
        assert "Cached" in result2


class TestProtectionProxy:
    def test_access_control(self):
        service = RealService()
        proxy = ProtectionProxy(service, "guest")
        
        result = proxy.operation("data")
        assert "Access denied" in result

    def test_authorized_access(self):
        service = RealService()
        proxy = ProtectionProxy(service, "admin")
        
        result = proxy.operation("data")
        assert "processed" in result


class TestValidationProxy:
    def test_validation(self):
        service = RealService()
        proxy = ValidationProxy(service)
        
        result = proxy.operation("")
        assert "Invalid" in result


class TestLoggingProxy:
    def test_logging(self):
        service = RealService()
        proxy = LoggingProxy(service)
        
        proxy.operation("data1")
        proxy.operation("data2")
        
        log = proxy.get_log()
        assert len(log) == 2

