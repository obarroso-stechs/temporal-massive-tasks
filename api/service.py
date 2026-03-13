from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from temporalio.client import Client

from temporal.constants import TEMPORAL_TASK_QUEUE
from temporal.models import FirmwareUpdateBatchInput, UpdateFirmware
from temporal.workflows.parent_workflow import FirmwareUpdateBatchWorkflow


async def _start_firmware_batch(
    *,
    client: Client,
    items: list[UpdateFirmware],
    start_delay: timedelta | None = None,
) -> tuple[str, str]:
    workflow_id = f"firmware-update-batch-{uuid.uuid4().hex}"

    handle = await client.start_workflow(
        FirmwareUpdateBatchWorkflow.run,
        FirmwareUpdateBatchInput(items=items),
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        start_delay=start_delay,
    )
    return handle.id, handle.result_run_id


def compute_start_delay(start_at: datetime) -> timedelta:
    delay = start_at - datetime.now(UTC)
    if delay <= timedelta(0):
        raise ValueError("start_at must be in the future")
    return delay
