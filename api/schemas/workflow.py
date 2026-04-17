from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


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
    is_paused: bool = False


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
