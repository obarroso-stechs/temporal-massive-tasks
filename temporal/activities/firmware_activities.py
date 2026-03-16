from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi import NbiClient, NbiConfig
from openapi_client.models import DownloadFileRequest

from temporal.models import (
    FirmwareDownloadInput,
    FirmwareUpdateResult,
)


@activity.defn
def verify_device_exists(serial_number: str) -> str:
    """Verifica que el serial number corresponde a un dispositivo registrado.

    Consulta la API filtrando por serial_number con projection [_deviceId].
    Si la respuesta contiene al menos un item, el dispositivo existe y
    se retorna el serial_number recibido. Si viene vacío, lanza error.
    """
    with NbiClient(NbiConfig()) as client:
        devices = client.devices.list_sync(
            serial_number=serial_number,
            projection=["_deviceId._SerialNumber"],
        )

    if devices:
        return serial_number

    raise ApplicationError(
        f"Device not found for serialNumber={serial_number!r}",
        type="DEVICE_NOT_FOUND",
        non_retryable=True,
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
