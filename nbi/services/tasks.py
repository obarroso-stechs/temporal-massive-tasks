"""Task domain service."""

from __future__ import annotations

from typing import List, Optional

from openapi_client import ApiClient, TasksApi
from openapi_client.models import AsyncResponse, DeleteDeviceTask200Response, DeviceTask

from .base import BaseService


class TaskService(BaseService):
    """Wraps TasksApi — task listing and deletion."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)
        self._api = TasksApi(api_client)

    def get_sync(
        self,
        serial_number: str,
        *,
        timeout: Optional[int] = None,
    ) -> List[DeviceTask]:
        return self._api.get_device_tasks(
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
        return self._api.get_device_tasks_async(
            serial_number=serial_number,
            tasks_get_serial_number_async_post_request=callback_request,
            timeout=timeout,
        )

    def delete_sync(
        self,
        serial_number: str,
        task_id: str,
        *,
        timeout: Optional[int] = None,
    ) -> DeleteDeviceTask200Response:
        return self._api.delete_device_task(
            serial_number=serial_number,
            task_id=task_id,
            timeout=timeout,
        )

    def delete_async(
        self,
        serial_number: str,
        task_id: str,
        callback_request,
        *,
        timeout: Optional[int] = None,
    ) -> AsyncResponse:
        return self._api.delete_device_task_async(
            serial_number=serial_number,
            task_id=task_id,
            tasks_del_task_id_async_post_request=callback_request,
            timeout=timeout,
        )
