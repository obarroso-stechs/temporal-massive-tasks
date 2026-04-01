from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_atomic
from db.models.device import Device
from db.models.device_group import DeviceGroup, DeviceGroupMembership
from db.schemas.device_group import DeviceGroupResponse


class DeviceGroupRepository:

    # ── Write operations ─────────────────────────────────────────────────────

    @async_atomic
    async def create(self, name: str, description: str | None, db: AsyncSession) -> DeviceGroup:
        group = DeviceGroup(name=name, description=description)
        db.add(group)
        await db.flush()
        await db.refresh(group)
        return group

    @async_atomic
    async def update(self, group_id: int, name: str, description: str | None, db: AsyncSession) -> DeviceGroup | None:
        result = await db.execute(
            select(DeviceGroup).where(DeviceGroup.id == group_id)
        )
        group = result.scalar_one_or_none()
        if group is None:
            return None
        group.name = name
        group.description = description
        await db.flush()
        return group

    @async_atomic
    async def delete(self, group_id: int, db: AsyncSession) -> bool:
        result = await db.execute(
            select(DeviceGroup).where(DeviceGroup.id == group_id)
        )
        group = result.scalar_one_or_none()
        if group is None:
            return False
        await db.delete(group)
        return True

    @async_atomic
    async def add_devices(self, group_id: int, device_ids: list[int], db: AsyncSession) -> None:
        """Insert memberships; silently skip duplicates."""
        existing_result = await db.execute(
            select(DeviceGroupMembership.device_id).where(
                DeviceGroupMembership.group_id == group_id
            )
        )
        existing_ids = {row[0] for row in existing_result}
        new_members = [
            DeviceGroupMembership(group_id=group_id, device_id=did)
            for did in device_ids
            if did not in existing_ids
        ]
        db.add_all(new_members)

    @async_atomic
    async def remove_device(self, group_id: int, device_id: int, db: AsyncSession) -> bool:
        result = await db.execute(
            delete(DeviceGroupMembership).where(
                DeviceGroupMembership.group_id == group_id,
                DeviceGroupMembership.device_id == device_id,
            )
        )
        return result.rowcount > 0

    # ── Read operations (async) ───────────────────────────────────────────────

    async def get_by_id(self, group_id: int, db: AsyncSession) -> DeviceGroupResponse | None:
        result = await db.execute(select(DeviceGroup).where(DeviceGroup.id == group_id))
        group = result.scalar_one_or_none()
        if group is None:
            return None
        return DeviceGroupResponse.model_validate(group)

    async def list_all(self, db: AsyncSession) -> list[DeviceGroupResponse]:
        result = await db.execute(select(DeviceGroup).order_by(DeviceGroup.name))
        groups = result.scalars().all()
        return [DeviceGroupResponse.model_validate(group) for group in groups]

    async def get_device_ids(self, group_id: int, db: AsyncSession) -> list[int]:
        result = await db.execute(
            select(DeviceGroupMembership.device_id).where(
                DeviceGroupMembership.group_id == group_id
            )
        )
        return [row[0] for row in result]

    async def get_serial_numbers(self, group_id: int, db: AsyncSession) -> list[str]:
        """Return serial_numbers of all devices in a group (for workflow input)."""
        result = await db.execute(
            select(Device.serial_number)
            .join(DeviceGroupMembership, DeviceGroupMembership.device_id == Device.id)
            .where(DeviceGroupMembership.group_id == group_id)
        )
        return [row[0] for row in result]
