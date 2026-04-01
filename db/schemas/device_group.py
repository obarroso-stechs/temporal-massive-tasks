from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from db.schemas.device import DeviceResponse


class DeviceGroupCreate(BaseModel):
    """Schema for creating a new device group."""

    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    device_ids: list[int] | None = None


class DeviceGroupUpdate(BaseModel):
    """Schema for updating a device group."""

    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class DeviceGroupResponse(BaseModel):
    """Schema for device group read operations."""

    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeviceGroupDetailResponse(BaseModel):
    """Schema for device group with member devices."""

    id: int
    name: str
    description: str | None
    devices: list[DeviceResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
