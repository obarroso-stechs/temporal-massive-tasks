from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from db.models.report import ReportFormatEnum


class ReportCreate(BaseModel):
    """Schema for creating a new report."""

    task_id: int
    generate_report: bool
    report_format: ReportFormatEnum | None = ReportFormatEnum.PDF


class ReportUpdate(BaseModel):
    """Schema for updating a report."""

    generate_report: bool | None = None
    report_format: ReportFormatEnum | None = None


class ReportResponse(BaseModel):
    """Schema for report read operations."""

    id: int
    task_id: int
    generate_report: bool
    report_format: ReportFormatEnum | None
    report_path: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
