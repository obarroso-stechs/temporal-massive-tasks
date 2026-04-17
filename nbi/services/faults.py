"""Fault domain service."""

from __future__ import annotations

from typing import Dict, Optional

from openapi_client import ApiClient

from .base import BaseService


class FaultService(BaseService):
    """Wraps fault endpoints — fault listing and deletion."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)

    def get_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "GET", f"/faults/{serial_number}", params={"timeout": timeout}
        )

    def delete_sync(
        self,
        fault_id: str,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "DELETE", f"/faults/{fault_id}", params={"timeout": timeout}
        )
