"""Device domain service."""

from __future__ import annotations

import base64
import json
from datetime import datetime
from typing import Dict, List, Optional

from openapi_client import ApiClient, DevicesApi
from openapi_client.models import (
    AsyncResponse,
    FactoryResetSync200Response,
    GetDeviceListCallbackRequest,
    ObjectOperationRequest,
    ParameterValue,
    RebootSync200Response,
    SetParameterValueRequest,
    DevicesSerialNumberGetParameterValueAsyncPostRequest,
    DevicesSerialNumberSetParameterValueAsyncPostRequest,
    DevicesSerialNumberRebootAsyncPostRequest,
    DevicesSerialNumberFactoryResetAsyncPostRequest,
)

from .base import BaseService


class DeviceService(BaseService):
    """Wraps DevicesApi — device listing, parameter read/write, and lifecycle ops."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)
        self._api = DevicesApi(api_client)

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_sync(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        serial_number: Optional[str] = None,
        tags: Optional[str] = None,
        product_class: Optional[str] = None,
        last_inform: Optional[datetime] = None,
        last_inform_operator: Optional[str] = None,
        projection: Optional[List[str]] = None,
        timeout: Optional[int] = None,
    ) -> List[Dict]:
        """Fetch device list and return raw items dicts from the API envelope.

        The NBI API returns {"result": "success", "items": [...]} which is
        incompatible with the OpenAPI-generated deserializer. We bypass
        deserialization entirely and return the raw dicts from ``items``.
        """
        cfg = self._api_client.configuration
        url = cfg.host.rstrip("/") + "/devices"

        # Build query params — only include non-None values
        fields: Dict[str, str] = {}
        if limit is not None:
            fields["limit"] = str(limit)
        if offset is not None:
            fields["offset"] = str(offset)
        if serial_number is not None:
            fields["serialNumber"] = serial_number
        if tags is not None:
            fields["tags"] = tags
        if product_class is not None:
            fields["productClass"] = product_class
        if projection is not None:
            fields["projection"] = ",".join(projection)

        # HTTP Basic Auth header
        raw_password = (
            cfg.password.get_secret_value()
            if hasattr(cfg.password, "get_secret_value")
            else (cfg.password or "")
        )
        credentials = base64.b64encode(
            f"{cfg.username}:{raw_password}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Accept": "application/json",
        }

        kwargs = {"headers": headers}
        if fields:
            kwargs["fields"] = fields
        if timeout is not None:
            kwargs["timeout"] = timeout

        resp = self._api_client.rest_client.pool_manager.request(
            "GET", url, **kwargs
        )
        data = json.loads(resp.data.decode("utf-8"))
        return data.get("items", [])


    def list_async(
        self,
        callback_request: GetDeviceListCallbackRequest,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.list_devices_async(
            get_device_list_callback_request=callback_request,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------

    def get_parameter_sync(
        self,
        serial_number: str,
        parameter_name: str,
        *,
        timeout: Optional[int] = None,
    ) -> List[ParameterValue]:
        return self._api.get_parameter_value_sync(
            serial_number=serial_number,
            parameter_name=parameter_name,
            timeout=timeout,
        )

    def get_parameter_async(
        self,
        serial_number: str,
        callback_request: DevicesSerialNumberGetParameterValueAsyncPostRequest,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.get_parameter_value_async(
            serial_number=serial_number,
            devices_serial_number_get_parameter_value_async_post_request=callback_request,
            timeout=timeout,
        )

    def set_parameter_sync(
        self,
        serial_number: str,
        body: SetParameterValueRequest,
        *,
        timeout: Optional[int] = None,
    ) -> List[ParameterValue]:
        return self._api.set_parameter_value_sync(
            serial_number=serial_number,
            set_parameter_value_request=body,
            timeout=timeout,
        )

    def set_parameter_async(
        self,
        serial_number: str,
        callback_request: DevicesSerialNumberSetParameterValueAsyncPostRequest,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.set_parameter_value_async(
            serial_number=serial_number,
            devices_serial_number_set_parameter_value_async_post_request=callback_request,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def reboot_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> RebootSync200Response:
        return self._api.reboot_sync(serial_number=serial_number, timeout=timeout)

    def reboot_async(
        self,
        serial_number: str,
        callback_request: DevicesSerialNumberRebootAsyncPostRequest,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.reboot_async(
            serial_number=serial_number,
            devices_serial_number_reboot_async_post_request=callback_request,
            timeout=timeout,
        )

    def factory_reset_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> FactoryResetSync200Response:
        return self._api.factory_reset_sync(
            serial_number=serial_number, timeout=timeout
        )

    def factory_reset_async(
        self,
        serial_number: str,
        callback_request: DevicesSerialNumberFactoryResetAsyncPostRequest,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.factory_reset_async(
            serial_number=serial_number,
            devices_serial_number_factory_reset_async_post_request=callback_request,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Object operations
    # ------------------------------------------------------------------

    def add_object_sync(
        self,
        serial_number: str,
        body: ObjectOperationRequest,
        *,
        timeout: Optional[int] = None,
    ):
        return self._api.add_object_sync(
            serial_number=serial_number,
            object_operation_request=body,
            timeout=timeout,
        )

    def add_object_async(self, serial_number: str, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.add_object_async(
            serial_number=serial_number,
            add_object_callback_request=callback_request,
            timeout=timeout,
        )

    def delete_object_sync(
        self,
        serial_number: str,
        body: ObjectOperationRequest,
        *,
        timeout: Optional[int] = None,
    ):
        return self._api.delete_object_sync(
            serial_number=serial_number,
            object_operation_request=body,
            timeout=timeout,
        )

    def delete_object_async(self, serial_number: str, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.delete_object_async(
            serial_number=serial_number,
            delete_object_callback_request=callback_request,
            timeout=timeout,
        )

    def refresh_object_sync(
        self,
        serial_number: str,
        body: ObjectOperationRequest,
        *,
        timeout: Optional[int] = None,
    ):
        return self._api.refresh_object_sync(
            serial_number=serial_number,
            object_operation_request=body,
            timeout=timeout,
        )

    def refresh_object_async(self, serial_number: str, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.refresh_object_async(
            serial_number=serial_number,
            refresh_object_callback_request=callback_request,
            timeout=timeout,
        )
