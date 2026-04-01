from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from db.models.report import ReportFormatEnum
from db.models.task import DeviceTaskStatusEnum, TaskTypeEnum


class ReportDeviceResponse(BaseModel):
    serial_number: str
    model: str | None
    manufacturer: str | None
    status: DeviceTaskStatusEnum
    detail: str | None
    started_at: datetime | None
    end_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ReportSummaryResponse(BaseModel):
    id: int
    task_id: int
    workflow_id: str
    task_name: str
    task_type: TaskTypeEnum | None
    report_format: ReportFormatEnum
    has_file: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportDetailResponse(ReportSummaryResponse):
    devices: list[ReportDeviceResponse]
