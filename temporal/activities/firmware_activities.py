"""Firmware update activities.

Todas las activities son funciones sync (def, no async def) porque
el NbiClient usa urllib3 bloqueante. El worker debe configurar un
ThreadPoolExecutor como activity_executor para que corran en threads
separados sin bloquear el event loop de Temporal.
"""

from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi import NbiClient, NbiConfig
from openapi_client.models import DownloadFileRequest

from temporal.models import (
    FirmwareDownloadInput,
    FirmwareUpdateResult,
)


@activity.defn
def trigger_firmware_download(input: FirmwareDownloadInput) -> FirmwareUpdateResult:
    """Dispara la descarga de firmware hacia el dispositivo via TR-069.

    Llama a files/{serial_number}/download con el body:
      { "filename": "...", "file_type": "1 Firmware Upgrade Image" }
    """
    body = DownloadFileRequest(
        filename=input.filename,
        file_type=input.file_type,
    )

    with NbiClient(NbiConfig()) as client:
        response = client.files.download_sync(
            serial_number=input.serial_number,
            body=body,
        )

    # response es un dict/object con la respuesta del NBI (e.g. {"result": "success", ...})
    api_result = str(response) if response else "no_response"

    return FirmwareUpdateResult(
        serial_number=input.serial_number,
        filename=input.filename,
        status=api_result,
    )
