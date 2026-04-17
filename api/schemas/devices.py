from __future__ import annotations

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    serial_number: str = Field(min_length=1)
    description: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    software_version: str | None = None
    firmware_version: str | None = None


class DeviceUpdate(BaseModel):
    description: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    software_version: str | None = None
    firmware_version: str | None = None


class DeviceResponse(BaseModel):
    id: int
    serial_number: str
    description: str | None
    manufacturer: str | None
    model: str | None
    software_version: str | None
    firmware_version: str | None

    model_config = {"from_attributes": True}
