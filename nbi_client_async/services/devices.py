from __future__ import annotations

from typing import Any

from .base import AsyncBaseService


class AsyncDeviceService(AsyncBaseService):
    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        serial_number: str | None = None,
        tags: str | None = None,
        product_class: str | None = None,
        projection: list[str] | None = None,
        timeout: int | None = None,
    ) -> list[dict[str, Any]]:
        params = {
            "limit": limit,
            "offset": offset,
            "serialNumber": serial_number,
            "tags": tags,
            "productClass": product_class,
            "projection": ",".join(projection) if projection else None,
            "timeout": timeout,
        }
        return (await self._request("GET", "/devices", params=params)).get("items", [])

    async def get_parameter(
        self,
        serial_number: str,
        params_list: list[str] | str,
        *,
        connection_request: bool | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        normalized_params = params_list if isinstance(params_list, list) else [params_list]
        params = {
            "paramsList": normalized_params,
            "connectionRequest": connection_request,
            "timeout": timeout,
        }
        return await self._request(
            "GET", f"/devices/{serial_number}/getParameterValue", params=params
        )

    async def set_parameter(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/devices/{serial_number}/setParameterValue",
            params={"timeout": timeout},
            body=body,
        )

    async def reboot(
        self,
        serial_number: str,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/devices/{serial_number}/reboot",
            params={"timeout": timeout},
        )

    async def factory_reset(
        self,
        serial_number: str,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/devices/{serial_number}/factoryReset",
            params={"timeout": timeout},
        )

    async def add_object(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/devices/{serial_number}/addObject",
            params={"timeout": timeout},
            body=body,
        )

    async def delete_object(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        object_name = (
            body.object_name
            if hasattr(body, "object_name")
            else self._serialize_body(body)["objectName"]
        )
        return await self._request(
            "DELETE",
            f"/devices/{serial_number}/deleteObject/{object_name}",
            params={"timeout": timeout},
        )

    async def refresh_object(
        self,
        serial_number: str,
        body: Any,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "PUT",
            f"/devices/{serial_number}/refreshObject",
            params={"timeout": timeout},
            body=body,
        )
