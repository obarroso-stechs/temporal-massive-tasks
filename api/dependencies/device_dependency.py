from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_db
from db.services.device_service import DeviceService


async def get_device_service(db: AsyncSession = Depends(get_db)) -> DeviceService:
    return DeviceService(db)
