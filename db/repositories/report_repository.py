from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_atomic
from db.models.report import Report, ReportFormatEnum
from db.schemas.report import ReportResponse


class ReportRepository:

    # ── Write operations ─────────────────────────────────────────────────────

    @async_atomic
    async def create(
        self,
        task_id: int,
        generate_report: bool,
        report_format: ReportFormatEnum | None,
        db: AsyncSession,
    ) -> Report:
        report = Report(
            task_id=task_id,
            generate_report=generate_report,
            report_format=report_format,
        )
        db.add(report)
        await db.flush()
        await db.refresh(report)
        return report

    @async_atomic
    async def set_report_path(
        self, task_id: int, report_format: ReportFormatEnum, path: str, db: AsyncSession
    ) -> Report | None:
        result = await db.execute(
            select(Report).where(Report.task_id == task_id, Report.report_format == report_format)
        )
        report = result.scalar_one_or_none()
        if report is None:
            return None
        report.report_path = path
        await db.flush()
        return report

    @async_atomic
    async def delete(self, report_id: int, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Report).where(Report.id == report_id)
        )
        report = result.scalar_one_or_none()
        if report is None:
            return False
        await db.delete(report)
        return True

    # ── Read operations (async for FastAPI) ───────────────────────────────────

    async def get_all(self, db: AsyncSession) -> list[ReportResponse]:
        result = await db.execute(select(Report).order_by(Report.created_at.desc()))
        reports = result.scalars().all()
        return [ReportResponse.model_validate(report) for report in reports]

    async def get_by_id(self, report_id: int, db: AsyncSession) -> ReportResponse | None:
        result = await db.execute(select(Report).where(Report.id == report_id))
        report = result.scalar_one_or_none()
        if report is None:
            return None
        return ReportResponse.model_validate(report)

    async def get_by_task_id(self, task_id: int, db: AsyncSession) -> list[ReportResponse]:
        result = await db.execute(select(Report).where(Report.task_id == task_id))
        reports = result.scalars().all()
        return [ReportResponse.model_validate(r) for r in reports]

    async def get_by_task_and_format(
        self, task_id: int, report_format: ReportFormatEnum, db: AsyncSession
    ) -> ReportResponse | None:
        result = await db.execute(
            select(Report).where(Report.task_id == task_id, Report.report_format == report_format)
        )
        report = result.scalar_one_or_none()
        if report is None:
            return None
        return ReportResponse.model_validate(report)
