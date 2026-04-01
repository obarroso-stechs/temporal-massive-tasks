"""Firmware update activities.

Activities async para llamadas NBI no bloqueantes mediante AsyncNbiClient.
"""

from temporalio import activity

from nbi_client_async import AsyncNbiClient, NbiConfig

from temporal.models import (
    FirmwareDownloadInput,
    FirmwareUpdateResult,
)


@activity.defn
async def trigger_firmware_download(input: FirmwareDownloadInput) -> FirmwareUpdateResult:
    """Dispara la descarga de firmware hacia el dispositivo via TR-069.

    Llama a files/{serial_number}/download con el body:
      { "filename": "...", "file_type": "1 Firmware Upgrade Image" }
    """
    body = {
        "filename": input.filename,
        "file_type": input.file_type,
    }

    async with AsyncNbiClient(NbiConfig()) as client:
        response = await client.files.download(
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
