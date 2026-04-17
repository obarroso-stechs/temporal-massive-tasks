"""Temporal activities that persist task reporting data to PostgreSQL."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from temporalio import activity

from api.dependencies.task_dependency import get_task_service_scope
from db.models.task import DeviceTaskStatusEnum

logger = logging.getLogger(__name__)

@activity.defn
async def mark_task_started(workflow_id: str) -> None:
    """Transition task to started state and move SCHEDULED devices to PENDING."""
    started_at = datetime.now(UTC)
    async with get_task_service_scope() as task_service:
        result = await task_service.mark_started(workflow_id, started_at)
        if result is None:
            logger.warning("mark_task_started: task not found for workflow_id=%s", workflow_id)


@activity.defn
async def upsert_device_status(
    workflow_id: str,
    serial_number: str,
    status: str,
    detail: str | None = None,
    started_at: str | None = None,
    end_at: str | None = None,
) -> None:
    """Update a single device's execution status within a task."""
    async with get_task_service_scope() as task_service:
        updated = await task_service.upsert_device_status(
            workflow_id=workflow_id,
            serial_number=serial_number,
            status=DeviceTaskStatusEnum(status),
            detail=detail,
            started_at=datetime.fromisoformat(started_at) if started_at else None,
            end_at=datetime.fromisoformat(end_at) if end_at else None,
        )
        if not updated:
            logger.warning("upsert_device_status: task not found for workflow_id=%s", workflow_id)


@activity.defn
async def mark_task_completed(workflow_id: str) -> None:
    """Mark task as completed."""
    end_at = datetime.now(UTC)
    async with get_task_service_scope() as task_service:
        task = await task_service.mark_completed(workflow_id, end_at)
        if task is None:
            logger.warning("mark_task_completed: task not found for workflow_id=%s", workflow_id)


@activity.defn
async def mark_task_failed(workflow_id: str, detail: str) -> None:
    """Mark all pending/running devices as FAILED and close the task."""
    end_at = datetime.now(UTC)
    async with get_task_service_scope() as task_service:
        updated = await task_service.mark_failed(workflow_id, detail, end_at)
        if not updated:
            logger.warning("mark_task_failed: task not found for workflow_id=%s", workflow_id)


@activity.defn
async def mark_task_canceled(workflow_id: str, serial_numbers: list[str]) -> None:
    """Mark the given devices as CANCELED and close the task."""
    end_at = datetime.now(UTC)
    async with get_task_service_scope() as task_service:
        updated = await task_service.mark_canceled(workflow_id, serial_numbers, end_at)
        if not updated:
            logger.warning("mark_task_canceled: task not found for workflow_id=%s", workflow_id)
