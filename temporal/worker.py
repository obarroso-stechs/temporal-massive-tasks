import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from temporal.activities import trigger_firmware_download, verify_device_exists
from temporal.constants import (
    TEMPORAL_NAMESPACE,
    TEMPORAL_TARGET_HOST,
    TEMPORAL_TASK_QUEUE,
)
from temporal.workflows import FirmwareUpdateBatchWorkflow, FirmwareUpdateChildWorkflow


async def run_worker() -> None:
    client = await Client.connect(TEMPORAL_TARGET_HOST, namespace=TEMPORAL_NAMESPACE)

    # Las activities son sync (def) porque NbiClient usa urllib3 bloqueante.
    # El ThreadPoolExecutor permite ejecutar múltiples activities en paralelo
    # sin bloquear el event loop de Temporal.
    print("WORKER STARTED")
    with ThreadPoolExecutor(max_workers=20) as executor:
        worker = Worker(
            client,
            task_queue=TEMPORAL_TASK_QUEUE,
            workflows=[FirmwareUpdateBatchWorkflow, FirmwareUpdateChildWorkflow],
            activities=[verify_device_exists, trigger_firmware_download],
            activity_executor=executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker())
