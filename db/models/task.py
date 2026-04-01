from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class TaskTypeEnum(str, enum.Enum):
    FIRMWARE_UPDATE = "FIRMWARE_UPDATE"
    PARAMETER_UPDATE = "PARAMETER_UPDATE"
    PARAMETER_SET = "PARAMETER_SET"


class DeviceTaskStatusEnum(str, enum.Enum):
    SCHEDULED = "SCHEDULED"   # Part of a future-scheduled batch; start date not yet reached
    PENDING = "PENDING"       # Batch started but device not yet picked up by executor
    RUNNING = "RUNNING"       # Child workflow is actively executing
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    TIMED_OUT = "TIMED_OUT"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workflow_id: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    task_type: Mapped[TaskTypeEnum] = mapped_column(
        Enum(TaskTypeEnum, name="task_type_enum"), nullable=False
    )
    # Auto-generated human-readable label: "{Type} | {Group name or 'Group not assigned'} | {YYYY-MM-DD HH:mm}"
    task_name: Mapped[str] = mapped_column(String(300), nullable=False)
    group_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("device_groups.id", ondelete="SET NULL"), nullable=True
    )
    # scheduled_at: set only for future-scheduled batches (start_at in the request)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # started_at: when the Temporal worker actually began execution
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TaskDeviceStatus(Base):
    """Per-device execution status within a Task.

    One record per device per Task. This table is the source of truth for
    individual device progress and is used to derive batch-level aggregates
    (total_devices, processed_devices, failed_devices) on demand.
    """

    __tablename__ = "task_device_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    serial_number: Mapped[str] = mapped_column(String(100), nullable=False)
    # device_id is nullable: device may not be registered in our DB
    device_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("devices.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[DeviceTaskStatusEnum] = mapped_column(
        Enum(DeviceTaskStatusEnum, name="device_task_status_enum"),
        nullable=False,
        default=DeviceTaskStatusEnum.PENDING,
    )
    detail: Mapped[str | None] = mapped_column(String(500), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("task_id", "serial_number", name="uq_task_serial"),
    )
