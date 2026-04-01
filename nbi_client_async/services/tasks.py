from __future__ import annotations

from .base import AsyncBaseService


class AsyncTaskService(AsyncBaseService):
    async def get(self, serial_number: str, *, timeout: int | None = None) -> dict:
        return await self._request(
            "GET",
            f"/tasks/{serial_number}",
            params={"timeout": timeout},
        )

    async def delete(self, task_id: str, *, timeout: int | None = None) -> dict:
        return await self._request(
            "DELETE",
            f"/tasks/{task_id}",
            params={"timeout": timeout},
        )
