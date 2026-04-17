from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from db.models.task import DeviceTaskStatusEnum, TaskTypeEnum


class TaskDeviceStatusResponse(BaseModel):
    serial_number: str
    status: DeviceTaskStatusEnum
    detail: str | None
    started_at: datetime | None
    end_at: datetime | None

    model_config = {"from_attributes": True}


class TaskSummaryResponse(BaseModel):
    id: int
    workflow_id: str
    task_type: TaskTypeEnum
    task_name: str
    group_id: int | None
    scheduled_at: datetime | None
    started_at: datetime | None
    end_at: datetime | None
    created_at: datetime
    is_canceled: bool = False

    model_config = {"from_attributes": True}


class TaskDetailResponse(TaskSummaryResponse):
    total_devices: int
    processed_devices: int
    failed_devices: int
    devices: list[TaskDeviceStatusResponse]
