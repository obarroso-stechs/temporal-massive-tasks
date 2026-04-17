"""Base service class shared by all domain services."""

from __future__ import annotations

import base64
import dataclasses
import json
from typing import Any, Dict, Optional

from openapi_client import ApiClient


class BaseService:
    """Holds the shared ApiClient instance.

    All domain services extend this class and receive the ApiClient
    via constructor injection, keeping them decoupled from configuration.
    """

    def __init__(self, api_client: ApiClient) -> None:
        self._api_client = api_client

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
    ) -> Dict:
        """Make a raw HTTP request bypassing OpenAPI SDK deserialization.

        The NBI API always returns {"result": ..., "items": [...]} which is
        incompatible with the OpenAPI-generated deserializer. This helper
        returns the raw parsed JSON dict.

        Args:
            method: HTTP verb (GET, POST, PUT, DELETE).
            path: URL path starting with /, e.g. "/devices/{sn}/reboot".
            params: Query parameters (None values are excluded).
            body: Request body. Accepts pydantic models, dataclasses, or dicts.
        """
        cfg = self._api_client.configuration
        url = cfg.host.rstrip("/") + path

        raw_password = (
            cfg.password.get_secret_value()
            if hasattr(cfg.password, "get_secret_value")
            else (cfg.password or "")
        )
        credentials = base64.b64encode(
            f"{cfg.username}:{raw_password}".encode()
        ).decode()
        headers: Dict[str, str] = {
            "Authorization": f"Basic {credentials}",
            "Accept": "application/json",
        }

        kwargs: Dict[str, Any] = {"headers": headers}

        if params:
            kwargs["fields"] = {k: v for k, v in params.items() if v is not None}

        if body is not None:
            headers["Content-Type"] = "application/json"
            kwargs["body"] = json.dumps(self._serialize_body(body)).encode()

        resp = self._api_client.rest_client.pool_manager.request(method, url, **kwargs)
        return json.loads(resp.data.decode("utf-8"))

    @staticmethod
    def _serialize_body(body: Any) -> Dict:
        if hasattr(body, "model_dump"):
            return body.model_dump(by_alias=True)
        if dataclasses.is_dataclass(body) and not isinstance(body, type):
            return dataclasses.asdict(body)
        return dict(body)
