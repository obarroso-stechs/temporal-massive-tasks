"""NbiClient — facade entry point for the NBI REST API.

Usage
-----
    from nbi import NbiClient, NbiConfig

    config = NbiConfig(host="https://...", username="admin", password="secret")

    # Option A: explicit lifecycle
    client = NbiClient(config)
    devices = client.devices.list_sync()
    client.close()

    # Option B: context manager (recommended)
    with NbiClient(config) as client:
        devices = client.devices.list_sync()

    # Option C: config from environment variables
    with NbiClient(NbiConfig()) as client:
        devices = client.devices.list_sync()
"""

from __future__ import annotations

from openapi_client import ApiClient

from .configuration.nbi_configuration import NbiConfig
from .services import DeviceService, FaultService, FileService, HealthService, TaskService


class NbiClient:
    """Facade that wires configuration, transport and domain services together.

    Each domain is exposed as a typed attribute so call sites are explicit
    and IDE auto-complete works out of the box:

        client.devices   → DeviceService
        client.faults    → FaultService
        client.files     → FileService
        client.tasks     → TaskService
        client.health    → HealthService
    """

    def __init__(self, config: NbiConfig) -> None:
        self._raw_client = ApiClient(config.to_openapi_configuration())

        self.devices: DeviceService = DeviceService(self._raw_client)
        self.faults: FaultService = FaultService(self._raw_client)
        self.files: FileService = FileService(self._raw_client)
        self.tasks: TaskService = TaskService(self._raw_client)
        self.health: HealthService = HealthService(self._raw_client)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release the underlying HTTP connection pool (if supported)."""
        if hasattr(self._raw_client, "close"):
            self._raw_client.close()

    def __enter__(self) -> NbiClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()
