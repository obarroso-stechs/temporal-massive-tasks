from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from db.models.task import DeviceTaskStatusEnum, TaskTypeEnum


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    workflow_id: str
    task_type: TaskTypeEnum
    task_name: str
    group_id: int | None = None
    scheduled_at: datetime | None = None


class TaskResponse(BaseModel):
    """Schema for task read operations."""

    id: int
    workflow_id: str
    task_type: TaskTypeEnum
    task_name: str
    group_id: int | None
    scheduled_at: datetime | None
    started_at: datetime | None
    end_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskDeviceStatusCreate(BaseModel):
    """Schema for creating device status records."""

    task_id: int
    serial_number: str
    status: DeviceTaskStatusEnum


class TaskDeviceStatusResponse(BaseModel):
    """Schema for device status read operations."""

    id: int
    task_id: int
    serial_number: str
    device_id: int | None
    status: DeviceTaskStatusEnum
    detail: str | None
    started_at: datetime | None
    end_at: datetime | None
    updated_at: datetime

    model_config = {"from_attributes": True}
