from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DeviceReportRow:
    """One row in the report table — keyed by serial_number."""

    serial_number: str
    model: str | None
    manufacturer: str | None
    task_status: str
    detail: str | None
    scheduled_at: datetime | None
    started_at: datetime | None
    end_at: datetime | None


@dataclass
class ReportData:
    """All data needed to render any report format."""

    task_name: str
    group_name: str           # "group not assigned" when no group is set
    total_devices: int
    processed_devices: int
    failed_devices: int
    rows: list[DeviceReportRow] = field(default_factory=list)
