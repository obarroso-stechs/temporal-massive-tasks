from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.firmware_activities import trigger_firmware_download
    from temporal.activities.common_activities import verify_device_exists
    from temporal.models import (
        FirmwareDownloadInput,
        FirmwareUpdateResult,
        UpdateFirmware,
    )


@workflow.defn
class FirmwareUpdateChildWorkflow:
    """Workflow hijo: actualiza firmware en un solo dispositivo.

    Paso 1 → verify_device_exists   (valida que el serialNumber existe en el ACS)
    Paso 2 → trigger_firmware_download (descarga firmware al dispositivo)
    """

    @workflow.run
    async def run(self, input: UpdateFirmware) -> FirmwareUpdateResult:
        # Paso 1: verificar que el serial number corresponde a un equipo registrado
        serial_number = await workflow.execute_activity(
            verify_device_exists,
            input.serialNumber,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        # Paso 2: disparar descarga de firmware al dispositivo
        result = await workflow.execute_activity(
            trigger_firmware_download,
            FirmwareDownloadInput(
                serial_number=serial_number,
                filename=input.filename,
            ),
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )
        return result
