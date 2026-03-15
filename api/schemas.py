from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FirmwareItem(BaseModel):
    serialNumber: str = Field(min_length=1)
    filename: str = Field(min_length=1)


class FirmwareBatchRequest(BaseModel):
    items: List[FirmwareItem] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_serial_numbers(self) -> "FirmwareBatchRequest":
        seen: set[str] = set()
        duplicated: list[str] = []

        for item in self.items:
            if item.serialNumber in seen and item.serialNumber not in duplicated:
                duplicated.append(item.serialNumber)
            seen.add(item.serialNumber)

        if duplicated:
            duplicates = ", ".join(duplicated)
            raise ValueError(
                f"serialNumber values must be unique. Duplicates: {duplicates}"
            )

        return self


class FirmwareBatchScheduledRequest(FirmwareBatchRequest):
    start_at: datetime = Field(
        description="UTC datetime when workflow should start"
    )

    @field_validator("start_at")
    @classmethod
    def validate_start_at_is_future(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("start_at must include timezone information")
        if value.astimezone(UTC) <= datetime.now(UTC):
            raise ValueError("start_at must be in the future")
        return value


class FirmwareBatchStartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: str
    run_id: str
    scheduled: bool
    accepted_at: datetime
    start_at: datetime | None = None


class FirmwareResultItem(BaseModel):
    serial_number: str | None = None
    filename: str | None = None
    status: str | None = None


# ── Enum de estados de ejecucion ─────────────────────────────────


class DeviceExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    TERMINATED = "TERMINATED"
    CANCELED = "CANCELED"


# ── Modelos de event history ─────────────────────────────────────


class WorkflowEvent(BaseModel):
    event_id: int
    timestamp: str | None
    event_type: str
    details: dict


class BatchProgress(BaseModel):
    total: int
    processed: int
    pending: int
    failed: int


class DeviceWithEvents(BaseModel):
    serial_number: str
    status: DeviceExecutionStatus
    events: List[WorkflowEvent]


# ── Responses ────────────────────────────────────────────────────


class DeviceStatusResponse(BaseModel):
    workflow_id: str
    serial_number: str
    status: DeviceExecutionStatus
    result: FirmwareResultItem | None = None
    events: List[WorkflowEvent]


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    progress: BatchProgress | None = None
    devices: List[DeviceWithEvents]


class BatchGroupStatusRequest(BaseModel):
    workflow_ids: List[str] = Field(min_length=1)


class BatchGroupSummary(BaseModel):
    total_batches: int
    completed_batches: int
    running_batches: int
    failed_batches: int
    total_devices: int
    total_processed: int
    total_pending: int
    total_failed: int
    all_completed: bool


class BatchGroupStatusResponse(BaseModel):
    batches: List[WorkflowStatusResponse]
    summary: BatchGroupSummary
