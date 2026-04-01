from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ReportFormatEnum(str, enum.Enum):
    PDF = "PDF"
    WORD = "WORD"
    EXCEL = "EXCEL"
    CSV = "CSV"


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        UniqueConstraint("task_id", "report_format", name="uq_report_task_format"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    generate_report: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    report_format: Mapped[ReportFormatEnum | None] = mapped_column(
        Enum(ReportFormatEnum, name="report_format_enum"),
        nullable=True,
        default=ReportFormatEnum.PDF,
    )
    # Filled once the file is generated and saved to disk
    report_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
