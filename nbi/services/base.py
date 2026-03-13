"""Base service class shared by all domain services."""

from __future__ import annotations

from openapi_client import ApiClient


class BaseService:
    """Holds the shared ApiClient instance.

    All domain services extend this class and receive the ApiClient
    via constructor injection, keeping them decoupled from configuration.
    """

    def __init__(self, api_client: ApiClient) -> None:
        self._api_client = api_client
