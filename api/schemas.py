from __future__ import annotations

from datetime import UTC, datetime
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


class FirmwareResultItem(BaseModel):
    serial_number: str | None = None
    filename: str | None = None
    status: str | None = None


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    result: List[FirmwareResultItem | str] | None = None
