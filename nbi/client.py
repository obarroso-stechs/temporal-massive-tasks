"""NbiClient — facade entry point for the NBI REST API.

Usage
-----
    from nbi import NbiClient
    from configurations.nbi import NbiConfig

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
from openapi_client import Configuration

from configurations.nbi import NbiConfig
from .services import DeviceService, FaultService, FileService, HealthService, TaskService


def _build_api_client(config: NbiConfig) -> ApiClient:
    openapi_cfg = Configuration(
        host=config.host,
        username=config.username,
        password=config.password,
    )
    openapi_cfg.verify_ssl = config.verify_ssl
    openapi_cfg.debug = config.debug
    return ApiClient(openapi_cfg)


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
        self._raw_client = _build_api_client(config)

        self.devices: DeviceService = DeviceService(self._raw_client)
        self.faults: FaultService = FaultService(self._raw_client)
        self.files: FileService = FileService(self._raw_client)
        self.tasks: TaskService = TaskService(self._raw_client)
        self.health: HealthService = HealthService(self._raw_client)

    def close(self) -> None:
        """Release the underlying HTTP connection pool (if supported)."""
        if hasattr(self._raw_client, "close"):
            self._raw_client.close()

    def __enter__(self) -> NbiClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()
