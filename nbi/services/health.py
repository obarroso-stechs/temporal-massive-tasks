"""Health/diagnostics service."""

from __future__ import annotations

from typing import Dict

from openapi_client import ApiClient, APITestApi
from openapi_client.models import GetErrorCodes200ResponseValue, TestWs200Response

from .base import BaseService


class HealthService(BaseService):
    """Wraps APITestApi — health check and error code listing."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)
        self._api = APITestApi(api_client)

    def ping(self) -> TestWs200Response:
        """Check API connectivity."""
        return self._api.test_ws()

    def get_error_codes(self) -> Dict[str, GetErrorCodes200ResponseValue]:
        """Return the full error code catalogue from the server."""
        return self._api.get_error_codes()
