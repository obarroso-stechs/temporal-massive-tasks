from __future__ import annotations

import dataclasses
from typing import Any

import httpx


class AsyncBaseService:
    """Shared async request/serialization helpers for NBI services."""

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: Any | None = None,
    ) -> dict[str, Any]:
        filtered_params = None
        if params is not None:
            filtered_params = {k: v for k, v in params.items() if v is not None}

        response = await self._http_client.request(
            method=method,
            url=path,
            params=filtered_params,
            json=self._serialize_body(body) if body is not None else None,
            headers={"Content-Type": "application/json"} if body is not None else None,
        )
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, dict):
            return payload
        return {"items": payload}

    @staticmethod
    def _serialize_body(body: Any) -> dict[str, Any]:
        if hasattr(body, "model_dump"):
            return body.model_dump(by_alias=True)
        if dataclasses.is_dataclass(body) and not isinstance(body, type):
            return dataclasses.asdict(body)
        return dict(body)
