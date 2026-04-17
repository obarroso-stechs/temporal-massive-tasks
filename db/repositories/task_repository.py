from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_atomic
from db.models.task import Task, TaskTypeEnum
from db.schemas.task import TaskResponse


class TaskRepository:

    # ── Write operations ─────────────────────────────────────────────────────

    @async_atomic
    async def create(
        self,
        workflow_id: str,
        task_type: TaskTypeEnum,
        task_name: str,
        group_id: int | None = None,
        scheduled_at: datetime | None = None,
        *,
        db: AsyncSession,
    ) -> Task:
        task = Task(
            workflow_id=workflow_id,
            task_type=task_type,
            task_name=task_name,
            group_id=group_id,
            scheduled_at=scheduled_at,
        )
        db.add(task)
        await db.flush()
        await db.refresh(task)
        return task

    @async_atomic
    async def set_started(self, workflow_id: str, started_at: datetime, db: AsyncSession) -> int | None:
        result = await db.execute(
            select(Task).where(Task.workflow_id == workflow_id)
        )
        task = result.scalar_one_or_none()
        if task is None:
            return None
        task.started_at = started_at
        await db.flush()
        return task.id

    @async_atomic
    async def set_completed(self, workflow_id: str, end_at: datetime, db: AsyncSession) -> int | None:
        result = await db.execute(
            select(Task).where(Task.workflow_id == workflow_id)
        )
        task = result.scalar_one_or_none()
        if task is None:
            return None
        task.end_at = end_at
        await db.flush()
        return task.id

    # ── Read operations (async for FastAPI) ───────────────────────────────────

    async def get_by_id(self, task_id: int, db: AsyncSession) -> TaskResponse | None:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            return None
        return TaskResponse.model_validate(task)

    async def get_by_workflow_id(self, workflow_id: str, db: AsyncSession) -> TaskResponse | None:
        result = await db.execute(select(Task).where(Task.workflow_id == workflow_id))
        task = result.scalar_one_or_none()
        if task is None:
            return None
        return TaskResponse.model_validate(task)

    async def list_all(self, db: AsyncSession) -> Sequence[TaskResponse]:
        result = await db.execute(select(Task).order_by(Task.created_at.desc()))
        tasks = result.scalars().all()
        return [TaskResponse.model_validate(task) for task in tasks]

    async def list_filtered(
        self,
        db: AsyncSession,
        task_type: TaskTypeEnum | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> Sequence[TaskResponse]:
        stmt = select(Task).order_by(Task.created_at.desc())
        if task_type:
            stmt = stmt.where(Task.task_type == task_type)
        if date_from:
            stmt = stmt.where(Task.created_at >= date_from)
        if date_to:
            stmt = stmt.where(Task.created_at <= date_to)
        result = await db.execute(stmt)
        tasks = result.scalars().all()
        return [TaskResponse.model_validate(task) for task in tasks]

