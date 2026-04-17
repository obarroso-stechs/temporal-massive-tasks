from __future__ import annotations

from datetime import UTC, datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.task import DeviceTaskStatusEnum, Task, TaskTypeEnum
from db.repositories.task_repository import TaskRepository
from db.repositories.task_device_status_repository import TaskDeviceStatusRepository
from db.schemas.task import TaskResponse


def _build_task_name(
    task_type: TaskTypeEnum,
    group_name: str | None,
    created_at: datetime,
) -> str:
    type_label_map = {
        TaskTypeEnum.FIRMWARE_UPDATE: "Firmware Update",
        TaskTypeEnum.PARAMETER_UPDATE: "Parameter Update",
        TaskTypeEnum.PARAMETER_SET: "Parameter Set",
        TaskTypeEnum.GET_PARAMETER_VALUES: "Get Parameter Values",
    }
    type_label = type_label_map.get(task_type, "Unknown Task")
    group_label = group_name or "Group not assigned"
    date_label = created_at.strftime("%Y-%m-%d %H:%M")
    return f"{type_label} | {group_label} | {date_label}"


class TaskService:

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db
        self._task_repo = TaskRepository()
        self._status_repo = TaskDeviceStatusRepository()

    async def create_task(
        self,
        workflow_id: str,
        task_type: TaskTypeEnum,
        serial_numbers: list[str],
        group_id: int | None = None,
        group_name: str | None = None,
        scheduled_at: datetime | None = None,
    ) -> Task:
        """Create a Task record and one TaskDeviceStatus per device."""
        now = datetime.now(UTC)
        task_name = _build_task_name(task_type, group_name, now)

        initial_status = (
            DeviceTaskStatusEnum.SCHEDULED if scheduled_at else DeviceTaskStatusEnum.PENDING
        )

        task = await self._task_repo.create(
            workflow_id=workflow_id,
            task_type=task_type,
            task_name=task_name,
            group_id=group_id,
            scheduled_at=scheduled_at,
            db=self._db,
        )
        await self._status_repo.bulk_create(task.id, serial_numbers, initial_status, self._db)
        return task

    async def mark_started(self, workflow_id: str, started_at: datetime) -> int | None:
        """Mark task as started and transition SCHEDULED devices to PENDING."""
        task_id = await self._task_repo.set_started(workflow_id, started_at, self._db)
        if task_id is None:
            return None
        await self._status_repo.transition_scheduled_to_pending(task_id, self._db)
        return task_id

    async def mark_completed(self, workflow_id: str, end_at: datetime) -> int | None:
        return await self._task_repo.set_completed(workflow_id, end_at, self._db)

    async def upsert_device_status(
        self,
        workflow_id: str,
        serial_number: str,
        status: DeviceTaskStatusEnum,
        detail: str | None = None,
        started_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> bool:
        task = await self._task_repo.get_by_workflow_id(workflow_id, self._db)
        if task is None:
            return False
        await self._status_repo.upsert_status(
            task_id=task.id,
            serial_number=serial_number,
            status=status,
            detail=detail,
            started_at=started_at,
            end_at=end_at,
            db=self._db,
        )
        return True

    async def mark_failed(self, workflow_id: str, detail: str, end_at: datetime) -> bool:
        """Mark all pending/running devices as FAILED and close the task."""
        task = await self._task_repo.get_by_workflow_id(workflow_id, self._db)
        if task is None:
            return False

        await self._status_repo.bulk_fail(task.id, detail=detail, end_at=end_at, db=self._db)
        await self._task_repo.set_completed(workflow_id, end_at, self._db)
        return True

    async def mark_canceled(self, workflow_id: str, serial_numbers: list[str], end_at: datetime) -> bool:
        """Mark given devices as CANCELED and close the task."""
        task = await self._task_repo.get_by_workflow_id(workflow_id, self._db)
        if task is None:
            return False

        if serial_numbers:
            await self._status_repo.bulk_cancel(task.id, serial_numbers, end_at=end_at, db=self._db)
        await self._task_repo.set_completed(workflow_id, end_at, self._db)
        return True

    async def get_batch_status_raw(self, workflow_id: str) -> dict | None:
        """Return raw DB data for building a WorkflowStatusResponse fallback."""
        task = await self._task_repo.get_by_workflow_id(workflow_id, self._db)
        if task is None:
            return None
        devices = await self._status_repo.list_by_task(task.id, self._db)
        counts = await self._status_repo.get_counts(task.id, self._db)
        return {"task": task, "devices": devices, "counts": counts}

    # ── Async reads for FastAPI ────────────────────────────────────────────────

    async def get_task_detail(self, task_id: int) -> dict:
        """Return task with computed aggregates and device list."""
        task = await self._task_repo.get_by_id(task_id, self._db)
        if task is None:
            raise ValueError(f"Task '{task_id}' not found.")

        counts = await self._status_repo.get_counts(task_id, self._db)
        devices = await self._status_repo.list_by_task(task_id, self._db)

        return {
            "task": task,
            "total_devices": counts["total"],
            "processed_devices": counts["processed"],
            "failed_devices": counts["failed"],
            "devices": devices,
        }

    async def list_tasks(
        self,
        task_type: TaskTypeEnum | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict]:
        tasks = await self._task_repo.list_filtered(self._db, task_type, date_from, date_to)
        task_ids = [t.id for t in tasks]
        canceled_ids = await self._status_repo.get_canceled_task_ids(task_ids, self._db)
        return [
            {**t.model_dump(), "is_canceled": t.id in canceled_ids}
            for t in tasks
        ]
