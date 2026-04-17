from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_db
from db.services.report_service import ReportService


async def get_report_service(db: AsyncSession = Depends(get_db)) -> ReportService:
    return ReportService(db)
