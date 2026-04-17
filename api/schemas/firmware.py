from __future__ import annotations

from datetime import UTC, datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FirmwareItem(BaseModel):
    serialNumber: str = Field(min_length=1)


class FirmwareBatchRequest(BaseModel):
    items: List[FirmwareItem] | None = None
    group_id: int | None = None

    @model_validator(mode="after")
    def validate_items_or_group(self) -> "FirmwareBatchRequest":
        has_items = bool(self.items)
        has_group = self.group_id is not None
        if not has_items and not has_group:
            raise ValueError("Debe enviar 'items' o 'group_id', no pueden ser ambos nulos.")
        if has_items and has_group:
            raise ValueError("No puede enviar 'items' y 'group_id' al mismo tiempo. Elija uno.")
        if has_items:
            seen: set[str] = set()
            deduped: list[FirmwareItem] = []
            for item in self.items:
                if item.serialNumber not in seen:
                    seen.add(item.serialNumber)
                    deduped.append(item)
            self.items = deduped
        return self


class FirmwareBatchScheduledRequest(FirmwareBatchRequest):
    start_at: datetime = Field(
        description=(
            "Datetime when the workflow should start. "
            "Must include timezone offset (e.g. 2026-03-18T11:20:00-03:00 for Argentina). "
            "Do NOT use 'Z' (UTC) unless you intend UTC time."
        )
    )

    @field_validator("start_at")
    @classmethod
    def validate_start_at_is_future(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("start_at must include timezone information")
        now_utc = datetime.now(UTC)
        if value.astimezone(UTC) <= now_utc:
            raise ValueError(
                f"start_at must be in the future. "
                f"Received {value.isoformat()} (= {value.astimezone(UTC).strftime('%H:%M:%S')} UTC), "
                f"but current UTC time is {now_utc.strftime('%H:%M:%S')} UTC. "
                f"If you are in Argentina (UTC-3), send the time with offset -03:00, "
                f"e.g.: {value.replace(tzinfo=None).isoformat()}-03:00"
            )
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
