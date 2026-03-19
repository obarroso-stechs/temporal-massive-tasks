from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FirmwareItem(BaseModel):
    serialNumber: str = Field(min_length=1)
    filename: str = Field(min_length=1)


class FirmwareBatchRequest(BaseModel):
    items: List[FirmwareItem] = Field(min_length=1)


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


class DeviceExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    TERMINATED = "TERMINATED"
    CANCELED = "CANCELED"


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
    workflow_id: str | None = None
    serial_number: str
    status: DeviceExecutionStatus
    message: str | None = None
    events: List[WorkflowEvent]


class DeviceStatusResponse(BaseModel):
    workflow_id: str
    serial_number: str
    status: DeviceExecutionStatus
    message: str | None = None
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


# ── Parameter Update ──────────────────────────────────────────────


class ParameterUpdateItem(BaseModel):
    serialNumber: str = Field(min_length=1)


class ParameterBatchRequest(BaseModel):
    items: List[ParameterUpdateItem] = Field(min_length=1)


class ParameterBatchScheduledRequest(ParameterBatchRequest):
    start_at: datetime = Field(
        description="Datetime con timezone cuando debe iniciar el workflow"
    )

    @field_validator("start_at")
    @classmethod
    def validate_start_at_is_future(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("start_at must include timezone information")
        if value.astimezone(UTC) <= datetime.now(UTC):
            raise ValueError("start_at must be in the future")
        return value


class ParameterBatchStartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: str
    run_id: str
    scheduled: bool
    accepted_at: datetime
    start_at: datetime | None = None
