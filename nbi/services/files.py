"""File/firmware domain service."""

from __future__ import annotations

from typing import Any, Dict, Optional

from openapi_client import ApiClient

from .base import BaseService


class FileService(BaseService):
    """Wraps file endpoints — firmware file listing, detail, upload and download."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)

    # ------------------------------------------------------------------
    # Listing / detail
    # ------------------------------------------------------------------

    def get_all_sync(self, *, timeout: Optional[int] = None) -> Dict:
        return self._request("GET", "/files/all", params={"timeout": timeout})

    def get_detail_sync(self, filename: str, *, timeout: Optional[int] = None) -> Dict:
        return self._request(
            "GET", f"/files/{filename}", params={"timeout": timeout}
        )

    # ------------------------------------------------------------------
    # Upload / download
    # ------------------------------------------------------------------

    def upload_sync(self, file: Any, *, timeout: Optional[int] = None) -> Dict:
        return self._request(
            "POST", "/files/upload", body=file, params={"timeout": timeout}
        )

    def download_sync(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "POST",
            f"/files/{serial_number}/downloadFile",
            body=body,
            params={"timeout": timeout},
        )
