"""File/firmware domain service."""

from __future__ import annotations

from typing import List, Optional

from openapi_client import ApiClient, FilesApi
from openapi_client.models import AsyncResponse, FirmwareFile

from .base import BaseService


class FileService(BaseService):
    """Wraps FilesApi — firmware file listing, detail, upload and download."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client)
        self._api = FilesApi(api_client)

    # ------------------------------------------------------------------
    # Listing / detail
    # ------------------------------------------------------------------

    def get_all_sync(self, *, timeout: Optional[int] = None) -> List[FirmwareFile]:
        return self._api.get_all_firmware_files(timeout=timeout)

    def get_all_async(self, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.get_all_firmware_files_async(
            files_all_async_post_request=callback_request,
            timeout=timeout,
        )

    def get_detail_sync(self, filename: str, *, timeout: Optional[int] = None) -> FirmwareFile:
        return self._api.get_firmware_file_detail(filename=filename, timeout=timeout)

    def get_detail_async(self, filename: str, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.get_firmware_file_detail_async(
            filename=filename,
            files_filename_async_post_request=callback_request,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Upload / download
    # ------------------------------------------------------------------

    def upload_sync(self, file, *, timeout: Optional[int] = None) -> FirmwareFile:
        return self._api.upload_firmware_file_sync(file=file, timeout=timeout)

    def upload_async(self, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.upload_firmware_file_async(
            files_upload_async_post_request=callback_request,
            timeout=timeout,
        )

    def download_sync(self, serial_number: str, body, *, timeout: Optional[int] = None):
        return self._api.download_file_sync(
            serial_number=serial_number,
            download_file_request=body,
            timeout=timeout,
        )

    def download_async(self, serial_number: str, callback_request, *, timeout: Optional[int] = None) -> AsyncResponse:
        return self._api.download_file_async(
            serial_number=serial_number,
            download_file_callback_request=callback_request,
            timeout=timeout,
        )
