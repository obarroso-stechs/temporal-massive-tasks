from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi_client_async import AsyncNbiClient, NbiConfig


@activity.defn
async def verify_device_exists(serial_number: str) -> str:
    """Verifica que el serial number corresponde a un dispositivo registrado.

    Consulta la API filtrando por serial_number con projection [_deviceId].
    Si la respuesta contiene al menos un item, el dispositivo existe y
    se retorna el serial_number recibido. Si viene vacío, lanza error.
    """
    print(NbiConfig(), " configuracion del nbi")
    async with AsyncNbiClient(NbiConfig()) as client:
        devices = await client.devices.list(
            serial_number=serial_number,
            projection=["_deviceId._SerialNumber"],
        )
    print(f"verify_device_exists: API response for serial_number={serial_number!r}: {devices}")
    if devices:
        return serial_number

    raise ApplicationError(
        f"Device not found for serialNumber={serial_number!r}",
        type="DEVICE_NOT_FOUND",
        non_retryable=True,
    )