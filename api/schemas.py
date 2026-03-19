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
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    TERMINATED = "TERMINATED"
    CANCELED = "CANCELED"


class BatchProgress(BaseModel):
    total: int
    processed: int
    pending: int
    failed: int


class DeviceStatusItem(BaseModel):
    serial_number: str
    status: DeviceExecutionStatus
    detail: str | None = None


class DeviceStatusResponse(BaseModel):
    workflow_id: str
    serial_number: str
    status: DeviceExecutionStatus
    detail: str | None = None


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    progress: BatchProgress | None = None
    devices: List[DeviceStatusItem]


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
