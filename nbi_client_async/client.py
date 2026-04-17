from __future__ import annotations

import httpx

from configurations.nbi import NbiConfig
from .services import (
    AsyncDeviceService,
    AsyncFaultService,
    AsyncFileService,
    AsyncHealthService,
    AsyncTaskService,
)


class AsyncNbiClient:
    """Async facade for the NBI REST API."""

    def __init__(self, config: NbiConfig, *, timeout: float = 30.0) -> None:
        self._http_client = httpx.AsyncClient(
            base_url=config.host.rstrip("/"),
            auth=(config.username, config.password),
            verify=config.verify_ssl,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

        self.devices: AsyncDeviceService = AsyncDeviceService(self._http_client)
        self.faults: AsyncFaultService = AsyncFaultService(self._http_client)
        self.files: AsyncFileService = AsyncFileService(self._http_client)
        self.tasks: AsyncTaskService = AsyncTaskService(self._http_client)
        self.health: AsyncHealthService = AsyncHealthService(self._http_client)

    async def aclose(self) -> None:
        await self._http_client.aclose()

    async def __aenter__(self) -> "AsyncNbiClient":
        return self

    async def __aexit__(self, *_exc_info) -> None:
        await self.aclose()
