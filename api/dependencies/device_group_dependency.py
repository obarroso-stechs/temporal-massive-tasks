from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_db
from db.services.device_group_service import DeviceGroupService


async def get_device_group_service(db: AsyncSession = Depends(get_db)) -> DeviceGroupService:
    return DeviceGroupService(db)
