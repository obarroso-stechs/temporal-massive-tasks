from __future__ import annotations

from datetime import UTC, datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ParameterGetItem(BaseModel):
    serialNumber: str = Field(min_length=1)


class ParameterGetBatchRequest(BaseModel):
    items: List[ParameterGetItem] | None = None
    group_id: int | None = None
    paths: list[str]

    @field_validator("paths")
    @classmethod
    def validate_paths_not_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("paths no puede estar vacio")
        return value

    @model_validator(mode="after")
    def validate_items_or_group(self) -> "ParameterGetBatchRequest":
        has_items = bool(self.items)
        has_group = self.group_id is not None
        if not has_items and not has_group:
            raise ValueError("Debe enviar 'items' o 'group_id', no pueden ser ambos nulos.")
        if has_items and has_group:
            raise ValueError("No puede enviar 'items' y 'group_id' al mismo tiempo. Elija uno.")
        if has_items:
            seen: set[str] = set()
            deduped: list[ParameterGetItem] = []
            for item in self.items:
                if item.serialNumber not in seen:
                    seen.add(item.serialNumber)
                    deduped.append(item)
            self.items = deduped
        return self


class ParameterGetBatchScheduledRequest(ParameterGetBatchRequest):
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


class ParameterGetBatchStartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: str
    run_id: str
    scheduled: bool
    accepted_at: datetime
    start_at: datetime | None = None
