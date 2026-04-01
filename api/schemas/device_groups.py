from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from api.schemas.devices import DeviceResponse


class DeviceGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    device_ids: list[int] | None = None

    @model_validator(mode="after")
    def dedup_device_ids(self) -> "DeviceGroupCreate":
        if self.device_ids:
            self.device_ids = list(dict.fromkeys(self.device_ids))
        return self


class DeviceGroupUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class DeviceGroupResponse(BaseModel):
    id: int
    name: str
    description: str | None
    devices: list[DeviceResponse] = []

    model_config = {"from_attributes": True}


class AssignDevicesRequest(BaseModel):
    device_ids: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def dedup_device_ids(self) -> "AssignDevicesRequest":
        self.device_ids = list(dict.fromkeys(self.device_ids))
        return self
