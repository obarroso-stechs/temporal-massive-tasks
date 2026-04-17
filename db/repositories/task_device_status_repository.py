from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_atomic
from db.models.task import DeviceTaskStatusEnum, TaskDeviceStatus
from db.schemas.task import TaskDeviceStatusResponse


class TaskDeviceStatusRepository:

    # ── Write operations ─────────────────────────────────────────────────────

    @async_atomic
    async def bulk_create(
        self,
        task_id: int,
        serial_numbers: list[str],
        initial_status: DeviceTaskStatusEnum,
        db: AsyncSession,
    ) -> None:
        """Create one TaskDeviceStatus record per device in the initial state."""
        records = [
            TaskDeviceStatus(
                task_id=task_id,
                serial_number=sn,
                status=initial_status,
            )
            for sn in serial_numbers
        ]
        db.add_all(records)

    @async_atomic
    async def upsert_status(
        self,
        task_id: int,
        serial_number: str,
        status: DeviceTaskStatusEnum,
        detail: str | None = None,
        started_at: datetime | None = None,
        end_at: datetime | None = None,
        *,
        db: AsyncSession,
    ) -> TaskDeviceStatus:
        """Insert or update a device's status record within a task."""
        stmt = (
            insert(TaskDeviceStatus)
            .values(
                task_id=task_id,
                serial_number=serial_number,
                status=status,
                detail=detail,
                started_at=started_at,
                end_at=end_at,
            )
            .on_conflict_do_update(
                constraint="uq_task_serial",
                set_=dict(
                    status=status,
                    detail=detail,
                    started_at=started_at,
                    end_at=end_at,
                ),
            )
            .returning(TaskDeviceStatus)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    @async_atomic
    async def transition_scheduled_to_pending(
        self,
        task_id: int,
        db: AsyncSession,
    ) -> None:
        """Move all SCHEDULED devices for a task to PENDING state."""
        from sqlalchemy import update as sa_update

        await db.execute(
            sa_update(TaskDeviceStatus)
            .where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.status == DeviceTaskStatusEnum.SCHEDULED,
            )
            .values(status=DeviceTaskStatusEnum.PENDING)
        )

    @async_atomic
    async def bulk_fail(
        self,
        task_id: int,
        detail: str,
        end_at: datetime,
        db: AsyncSession,
    ) -> None:
        """Mark all PENDING/RUNNING devices as FAILED."""
        from sqlalchemy import update as sa_update

        await db.execute(
            sa_update(TaskDeviceStatus)
            .where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.status.in_(
                    [DeviceTaskStatusEnum.PENDING, DeviceTaskStatusEnum.RUNNING]
                ),
            )
            .values(status=DeviceTaskStatusEnum.FAILED, detail=detail, end_at=end_at)
        )

    @async_atomic
    async def bulk_cancel(
        self,
        task_id: int,
        serial_numbers: list[str],
        end_at: datetime,
        db: AsyncSession,
    ) -> None:
        """Mark non-terminal devices in serial_numbers list as CANCELED."""
        from sqlalchemy import update as sa_update

        await db.execute(
            sa_update(TaskDeviceStatus)
            .where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.serial_number.in_(serial_numbers),
                TaskDeviceStatus.status.in_([
                    DeviceTaskStatusEnum.SCHEDULED,
                    DeviceTaskStatusEnum.PENDING,
                    DeviceTaskStatusEnum.RUNNING,
                ]),
            )
            .values(status=DeviceTaskStatusEnum.CANCELED, detail="Batch cancelado por el usuario", end_at=end_at)
        )

    @async_atomic
    async def bulk_fail_non_terminal_async(
        self,
        task_id: int,
        detail: str,
        end_at: datetime,
        db: AsyncSession,
    ) -> None:
        """Marca como FAILED todos los dispositivos en estado no-terminal (async)."""
        from sqlalchemy import update as sa_update

        await db.execute(
            sa_update(TaskDeviceStatus)
            .where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.status.in_([
                    DeviceTaskStatusEnum.SCHEDULED,
                    DeviceTaskStatusEnum.PENDING,
                    DeviceTaskStatusEnum.RUNNING,
                ]),
            )
            .values(status=DeviceTaskStatusEnum.FAILED, detail=detail, end_at=end_at)
        )

    # ── Read operations (async for FastAPI) ───────────────────────────────────

    async def list_by_task(
        self, task_id: int, db: AsyncSession
    ) -> Sequence[TaskDeviceStatusResponse]:
        result = await db.execute(
            select(TaskDeviceStatus)
            .where(TaskDeviceStatus.task_id == task_id)
            .order_by(TaskDeviceStatus.serial_number)
        )
        statuses = result.scalars().all()
        return [TaskDeviceStatusResponse.model_validate(status) for status in statuses]

    async def get_counts(self, task_id: int, db: AsyncSession) -> dict[str, int]:
        """Return total, processed, and failed device counts for a task."""
        total_result = await db.execute(
            select(func.count()).where(TaskDeviceStatus.task_id == task_id)
        )
        total = total_result.scalar_one()

        processed_result = await db.execute(
            select(func.count()).where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.status.notin_(
                    [DeviceTaskStatusEnum.PENDING, DeviceTaskStatusEnum.SCHEDULED]
                ),
            )
        )
        processed = processed_result.scalar_one()

        failed_result = await db.execute(
            select(func.count()).where(
                TaskDeviceStatus.task_id == task_id,
                TaskDeviceStatus.status == DeviceTaskStatusEnum.FAILED,
            )
        )
        failed = failed_result.scalar_one()

        return {"total": total, "processed": processed, "failed": failed}

    async def get_canceled_task_ids(self, task_ids: list[int], db: AsyncSession) -> set[int]:
        """Retorna el conjunto de task_ids que tienen al menos un dispositivo CANCELED."""
        if not task_ids:
            return set()
        result = await db.execute(
            select(TaskDeviceStatus.task_id).where(
                TaskDeviceStatus.task_id.in_(task_ids),
                TaskDeviceStatus.status == DeviceTaskStatusEnum.CANCELED,
            ).distinct()
        )
        return {row[0] for row in result.all()}
