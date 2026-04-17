from __future__ import annotations

from typing import Any

from .base import AsyncBaseService


class AsyncFileService(AsyncBaseService):
    async def get_all(self, *, timeout: int | None = None) -> dict[str, Any]:
        return await self._request(
            "GET",
            "/files/all",
            params={"timeout": timeout},
        )

    async def get_detail(self, filename: str, *, timeout: int | None = None) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/files/{filename}",
            params={"timeout": timeout},
        )

    async def upload(self, file: Any, *, timeout: int | None = None) -> dict[str, Any]:
        return await self._request(
            "POST",
            "/files/upload",
            params={"timeout": timeout},
            body=file,
        )

    async def download(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/files/{serial_number}/downloadFile",
            params={"timeout": timeout},
            body=body,
        )
