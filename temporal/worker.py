import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from temporal.activities.firmware_activities import trigger_firmware_download
from temporal.activities.parameter_update_activities import set_parameter_value
from temporal.activities.parameter_set_activities import set_parameter_value_parameter_set
from temporal.activities.common_activities import verify_device_exists
from temporal.activities.reporting_activities import (
    mark_task_started,
    mark_task_completed,
    mark_task_failed,
    mark_task_canceled,
    upsert_device_status,
)
from configurations.temporal import (
    TEMPORAL_NAMESPACE,
    TEMPORAL_TARGET_HOST,
    TEMPORAL_TASK_QUEUE,
)
from temporal.workflows import (
    FirmwareUpdateBatchWorkflow,
    FirmwareUpdateChildWorkflow,
    ParameterUpdateBatchWorkflow,
    ParameterUpdateChildWorkflow,
    ParameterSetBatchWorkflow,
    ParameterSetChildWorkflow,
)


async def run_worker() -> None:
    client = await Client.connect(TEMPORAL_TARGET_HOST, namespace=TEMPORAL_NAMESPACE)

    # Las activities registradas son async y usan I/O no bloqueante.
    print("WORKER STARTED")
    worker = Worker(
        client,
        task_queue=TEMPORAL_TASK_QUEUE,
        workflows=[
            FirmwareUpdateBatchWorkflow,
            FirmwareUpdateChildWorkflow,
            ParameterUpdateBatchWorkflow,
            ParameterUpdateChildWorkflow,
            ParameterSetBatchWorkflow,
            ParameterSetChildWorkflow,
        ],
        activities=[
            verify_device_exists,
            trigger_firmware_download,
            set_parameter_value,
            set_parameter_value_parameter_set,
            mark_task_started,
            mark_task_completed,
            mark_task_failed,
            mark_task_canceled,
            upsert_device_status,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker())
