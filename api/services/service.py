from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client

from configurations.temporal import TEMPORAL_TASK_QUEUE
from db.dependencies import get_db
from db.models.task import TaskTypeEnum
from db.services.device_group_service import DeviceGroupService
from db.services.task_service import TaskService
from temporal.models import (
    FirmwareUpdateBatchInput,
    ParameterSetBatchInput,
    ParameterUpdateBatchInput,
    UpdateFirmware,
    UpdateParameterSet,
    UpdateParameter,
)
from temporal.workflows.firmware_update.firmware_update_workflow import FirmwareUpdateBatchWorkflow
from temporal.workflows.parameter_set.parameter_set_workflow import ParameterSetBatchWorkflow
from temporal.workflows.parameter_update.parameter_update_workflow import ParameterUpdateBatchWorkflow


class BatchOrchestrationService:
    """Orchestrates starting Temporal batch workflows and persisting task records."""

    def __init__(self, task_service: TaskService, group_service: DeviceGroupService) -> None:
        self._task_service = task_service
        self._group_service = group_service

    async def start_firmware_batch(
        self,
        *,
        client: Client,
        serial_numbers: list[str] | None = None,
        group_id: int | None = None,
        filename: str,
        group_name: str | None = None,
        start_delay: timedelta | None = None,
    ) -> tuple[str, str]:
        if group_id is not None:
            group = await self._group_service.get_by_id(group_id)
            group_name = group.name
            serials = await self._group_service.resolve_serials_for_batch(group_id)
            if not serials:
                raise ValueError(f"El grupo '{group_id}' no tiene dispositivos.")
        else:
            serials = serial_numbers or []

        items = [UpdateFirmware(serialNumber=sn, filename=filename) for sn in serials]

        workflow_id = f"firmware-update-batch-{uuid.uuid4().hex}"
        scheduled_at = datetime.now(UTC) + start_delay if start_delay else None

        handle = await client.start_workflow(
            FirmwareUpdateBatchWorkflow.run,
            FirmwareUpdateBatchInput(items=items),
            id=workflow_id,
            task_queue=TEMPORAL_TASK_QUEUE,
            start_delay=start_delay,
        )

        await self._task_service.create_task(
            workflow_id=workflow_id,
            task_type=TaskTypeEnum.FIRMWARE_UPDATE,
            serial_numbers=serials,
            group_id=group_id,
            group_name=group_name,
            scheduled_at=scheduled_at,
        )
        return handle.id, handle.result_run_id

    async def start_parameter_batch(
        self,
        *,
        client: Client,
        serial_numbers: list[str] | None = None,
        group_id: int | None = None,
        group_name: str | None = None,
        start_delay: timedelta | None = None,
    ) -> tuple[str, str]:
        if group_id is not None:
            group = await self._group_service.get_by_id(group_id)
            group_name = group.name
            serials = await self._group_service.resolve_serials_for_batch(group_id)
            if not serials:
                raise ValueError(f"El grupo '{group_id}' no tiene dispositivos.")
        else:
            serials = serial_numbers or []

        items = [UpdateParameter(serialNumber=sn) for sn in serials]

        workflow_id = f"parameter-update-batch-{uuid.uuid4().hex}"
        scheduled_at = datetime.now(UTC) + start_delay if start_delay else None

        handle = await client.start_workflow(
            ParameterUpdateBatchWorkflow.run,
            ParameterUpdateBatchInput(items=items),
            id=workflow_id,
            task_queue=TEMPORAL_TASK_QUEUE,
            start_delay=start_delay,
        )

        await self._task_service.create_task(
            workflow_id=workflow_id,
            task_type=TaskTypeEnum.PARAMETER_UPDATE,
            serial_numbers=serials,
            group_id=group_id,
            group_name=group_name,
            scheduled_at=scheduled_at,
        )
        return handle.id, handle.result_run_id

    async def start_parameter_set_batch(
        self,
        *,
        client: Client,
        serial_numbers: list[str] | None = None,
        group_id: int | None = None,
        parameters: dict[str, str | bool | int | float],
        group_name: str | None = None,
        start_delay: timedelta | None = None,
    ) -> tuple[str, str]:
        if group_id is not None:
            group = await self._group_service.get_by_id(group_id)
            group_name = group.name
            serials = await self._group_service.resolve_serials_for_batch(group_id)
            if not serials:
                raise ValueError(f"El grupo '{group_id}' no tiene dispositivos.")
        else:
            serials = serial_numbers or []

        items = [
            UpdateParameterSet(serialNumber=sn, parameters=parameters)
            for sn in serials
        ]

        workflow_id = f"parameter-set-batch-{uuid.uuid4().hex}"
        scheduled_at = datetime.now(UTC) + start_delay if start_delay else None

        handle = await client.start_workflow(
            ParameterSetBatchWorkflow.run,
            ParameterSetBatchInput(items=items),
            id=workflow_id,
            task_queue=TEMPORAL_TASK_QUEUE,
            start_delay=start_delay,
        )

        await self._task_service.create_task(
            workflow_id=workflow_id,
            task_type=TaskTypeEnum.PARAMETER_SET,
            serial_numbers=serials,
            group_id=group_id,
            group_name=group_name,
            scheduled_at=scheduled_at,
        )
        return handle.id, handle.result_run_id

    @staticmethod
    def compute_start_delay(start_at: datetime) -> timedelta:
        delay = start_at - datetime.now(UTC)
        if delay <= timedelta(0):
            raise ValueError("start_at must be in the future")
        return delay


# ── Provider functions ────────────────────────────────────────────────────────

async def get_batch_orchestration_service(
    db: AsyncSession = Depends(get_db),
) -> BatchOrchestrationService:
    return BatchOrchestrationService(
        task_service=TaskService(db),
        group_service=DeviceGroupService(db),
    )
