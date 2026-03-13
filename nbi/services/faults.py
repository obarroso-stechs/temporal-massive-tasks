"""Fault domain service."""

from __future__ import annotations

from typing import List, Optional

from openapi_client import ApiClient, FaultsApi
from openapi_client.models import AsyncResponse, DeleteDeviceTask200Response, DeviceFault

from .base import BaseService


class FaultService(BaseService):
    """Wraps FaultsApi — fault listing and deletion."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)
        self._api = FaultsApi(api_client)

    def get_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> List[DeviceFault]:
        return self._api.get_device_faults(
            serial_number=serial_number,
            timeout=timeout,
        )

    def get_async(
        self,
        serial_number: str,
        callback_request,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.get_device_faults_async(
            serial_number=serial_number,
            faults_get_serial_number_async_post_request=callback_request,
            timeout=timeout,
        )

    def delete_sync(
        self,
        serial_number: str,
        fault_code: str,
        *,
        timeout: Optional[int] = None,
    ) -> DeleteDeviceTask200Response:
        return self._api.delete_device_fault(
            serial_number=serial_number,
            fault_code=fault_code,
            timeout=timeout,
        )

    def delete_async(
        self,
        serial_number: str,
        fault_code: str,
        callback_request,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.delete_device_fault_async(
            serial_number=serial_number,
            fault_code=fault_code,
            faults_get_serial_number_async_post_request=callback_request,
            timeout=timeout,
        )
