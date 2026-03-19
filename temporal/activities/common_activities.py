from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi import NbiClient, NbiConfig


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