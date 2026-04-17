from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_atomic
from db.models.device import Device
from db.schemas.device import DeviceResponse


class DeviceRepository:

    # ── Write operations ─────────────────────────────────────────────────────

    @async_atomic
    async def create(
        self,
        serial_number: str,
        description: str | None,
        manufacturer: str | None,
        model: str | None,
        software_version: str | None,
        firmware_version: str | None,
        db: AsyncSession,
    ) -> Device:
        device = Device(
            serial_number=serial_number,
            description=description,
            manufacturer=manufacturer,
            model=model,
            software_version=software_version,
            firmware_version=firmware_version,
        )
        db.add(device)
        await db.flush()
        await db.refresh(device)
        return device

    @async_atomic
    async def update(self, serial_number: str, db: AsyncSession, **fields) -> Device | None:
        result = await db.execute(
            select(Device).where(Device.serial_number == serial_number)
        )
        device = result.scalar_one_or_none()
        if device is None:
            return None
        for key, value in fields.items():
            if hasattr(device, key) and value is not None:
                setattr(device, key, value)
        await db.flush()
        return device

    @async_atomic
    async def delete(self, serial_number: str, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Device).where(Device.serial_number == serial_number)
        )
        device = result.scalar_one_or_none()
        if device is None:
            return False
        await db.delete(device)
        return True

    # ── Read operations (async for FastAPI) ───────────────────────────────────

    async def get_by_serial_number(self, serial_number: str, db: AsyncSession) -> DeviceResponse | None:
        result = await db.execute(
            select(Device).where(Device.serial_number == serial_number)
        )
        device = result.scalar_one_or_none()
        if device is None:
            return None
        return DeviceResponse.model_validate(device)

    async def get_by_id(self, device_id: int, db: AsyncSession) -> DeviceResponse | None:
        result = await db.execute(select(Device).where(Device.id == device_id))
        device = result.scalar_one_or_none()
        if device is None:
            return None
        return DeviceResponse.model_validate(device)

    async def list_all(self, db: AsyncSession) -> list[DeviceResponse]:
        result = await db.execute(select(Device).order_by(Device.serial_number))
        devices = result.scalars().all()
        return [DeviceResponse.model_validate(device) for device in devices]

    async def get_by_group_id(self, group_id: int, db: AsyncSession) -> list[DeviceResponse]:
        from db.models.device_group import DeviceGroupMembership

        result = await db.execute(
            select(Device)
            .join(DeviceGroupMembership, DeviceGroupMembership.device_id == Device.id)
            .where(DeviceGroupMembership.group_id == group_id)
            .order_by(Device.serial_number)
        )
        devices = result.scalars().all()
        return [DeviceResponse.model_validate(device) for device in devices]
