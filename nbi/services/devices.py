"""Device domain service."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from openapi_client import ApiClient

from .base import BaseService


class DeviceService(BaseService):
    """Wraps device endpoints — listing, parameter read/write, and lifecycle ops."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)

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
        projection: Optional[List[str]] = None,
        timeout: Optional[int] = None,
    ) -> List[Dict]:
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "serialNumber": serial_number,
            "tags": tags,
            "productClass": product_class,
            "projection": ",".join(projection) if projection else None,
            "timeout": timeout,
        }
        return self._request("GET", "/devices", params=params).get("items", [])

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------

    def get_parameter_sync(
        self,
        serial_number: str,
        params_list: List[str],
        *,
        connection_request: Optional[bool] = None,
        timeout: Optional[int] = None,
    ) -> Dict:
        params: Dict[str, Any] = {
            "paramsList": params_list,
            "connectionRequest": connection_request,
            "timeout": timeout,
        }
        return self._request(
            "GET", f"/devices/{serial_number}/getParameterValue", params=params
        )

    def set_parameter_sync(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "POST",
            f"/devices/{serial_number}/setParameterValue",
            body=body,
            params={"timeout": timeout},
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def reboot_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "POST", f"/devices/{serial_number}/reboot", params={"timeout": timeout}
        )

    def factory_reset_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "POST",
            f"/devices/{serial_number}/factoryReset",
            params={"timeout": timeout},
        )

    # ------------------------------------------------------------------
    # Object operations
    # ------------------------------------------------------------------

    def add_object_sync(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "POST",
            f"/devices/{serial_number}/addObject",
            body=body,
            params={"timeout": timeout},
        )

    def delete_object_sync(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        object_name = (
            body.object_name
            if hasattr(body, "object_name")
            else self._serialize_body(body)["objectName"]
        )
        return self._request(
            "DELETE",
            f"/devices/{serial_number}/deleteObject/{object_name}",
            params={"timeout": timeout},
        )

    def refresh_object_sync(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: Optional[int] = None,
    ) -> Dict:
        return self._request(
            "PUT",
            f"/devices/{serial_number}/refreshObject",
            body=body,
            params={"timeout": timeout},
        )
