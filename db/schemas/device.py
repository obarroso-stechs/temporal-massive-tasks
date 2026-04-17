from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    """Schema for creating a new device."""

    serial_number: str = Field(min_length=1)
    description: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    software_version: str | None = None
    firmware_version: str | None = None


class DeviceUpdate(BaseModel):
    """Schema for updating a device."""

    description: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    software_version: str | None = None
    firmware_version: str | None = None


class DeviceResponse(BaseModel):
    """Schema for device read operations."""

    id: int
    serial_number: str
    description: str | None
    manufacturer: str | None
    model: str | None
    software_version: str | None
    firmware_version: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
