from __future__ import annotations

from .base import AsyncBaseService


class AsyncHealthService(AsyncBaseService):
    async def ping(self) -> dict:
        return await self._request("GET", "/testws")

    async def get_error_codes(self) -> dict:
        return await self._request("GET", "/errorCodes")
