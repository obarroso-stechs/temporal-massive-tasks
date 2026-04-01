from __future__ import annotations

from .base import AsyncBaseService


class AsyncFaultService(AsyncBaseService):
    async def get(self, serial_number: str, *, timeout: int | None = None) -> dict:
        return await self._request(
            "GET",
            f"/faults/{serial_number}",
            params={"timeout": timeout},
        )

    async def delete(self, fault_id: str, *, timeout: int | None = None) -> dict:
        return await self._request(
            "DELETE",
            f"/faults/{fault_id}",
            params={"timeout": timeout},
        )
