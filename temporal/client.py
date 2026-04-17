import asyncio
import uuid
from typing import List, Union

from temporalio.client import Client

from configurations.temporal import (
    TEMPORAL_NAMESPACE,
    TEMPORAL_TARGET_HOST,
    TEMPORAL_TASK_QUEUE,
)
from temporal.models import FirmwareUpdateBatchInput, FirmwareUpdateResult, UpdateFirmware
from temporal.workflows import FirmwareUpdateBatchWorkflow


async def run_firmware_update_batch(
    items: List[UpdateFirmware],
) -> List[Union[FirmwareUpdateResult, str]]:
    """Lanza el workflow de batch firmware update y espera el resultado."""
    client = await Client.connect(TEMPORAL_TARGET_HOST, namespace=TEMPORAL_NAMESPACE)

    workflow_id = f"firmware-update-batch-{uuid.uuid4().hex[:8]}"

    return await client.execute_workflow(
        FirmwareUpdateBatchWorkflow.run,
        FirmwareUpdateBatchInput(items=items),
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
    )


if __name__ == "__main__":
    # Ejemplo de uso con datos de prueba
    test_items = [
        UpdateFirmware(serialNumber="ZTEEQHBK6L03296", filename="fw-v2.1.bin"),
        UpdateFirmware(serialNumber="ZTEEQHBK6L00001", filename="fw-v3.0.bin"),
        UpdateFirmware(serialNumber="ZTEEQHBK6L00002", filename="fw-v1.5.bin"),
    ]

    results = asyncio.run(run_firmware_update_batch(test_items))
    for r in results:
        print(r)
