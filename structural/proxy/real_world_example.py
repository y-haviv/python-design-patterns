"""Proxy Real-World Example: Remote Service Proxy."""

from typing import Any, List
from datetime import datetime


class RemoteService:
    """Remote service interface."""

    def fetch_data(self, resource_id: str) -> dict:
        pass


class ExpensiveRemoteService(RemoteService):
    """Simulates expensive remote service."""

    def fetch_data(self, resource_id: str) -> dict:
        # Simulate network call
        return {
            "id": resource_id,
            "data": f"Data for {resource_id}",
            "timestamp": datetime.now().isoformat()
        }


class RemoteServiceProxy(RemoteService):
    """Proxy with caching and error handling."""

    def __init__(self, max_cache_size: int = 100):
        self._service = ExpensiveRemoteService()
        self._cache: dict = {}
        self._max_cache = max_cache_size
        self._request_count = 0

    def fetch_data(self, resource_id: str) -> dict:
        self._request_count += 1

        # Check cache
        if resource_id in self._cache:
            return {"source": "cache", **self._cache[resource_id]}

        # Fetch from service
        try:
            data = self._service.fetch_data(resource_id)
            self._cache[resource_id] = data
            return {"source": "remote", **data}
        except Exception as e:
            return {"error": str(e)}

    def get_stats(self) -> dict:
        return {
            "requests": self._request_count,
            "cached_items": len(self._cache)
        }


