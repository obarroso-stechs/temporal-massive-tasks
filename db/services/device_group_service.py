from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.device_group_repository import DeviceGroupRepository
from db.repositories.device_repository import DeviceRepository
from db.schemas.device_group import DeviceGroupDetailResponse


class DeviceGroupService:

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._group_repo = DeviceGroupRepository()
        self._device_repo = DeviceRepository()

    async def create(
        self,
        name: str,
        description: str | None = None,
        device_ids: list[int] | None = None,
    ) -> DeviceGroupDetailResponse:
        all_groups = await self._group_repo.list_all(self._db)
        if any(g.name == name for g in all_groups):
            raise ValueError(f"Ya existe un grupo con el nombre '{name}'.")

        if device_ids:
            invalid = [did for did in device_ids if not await self._device_repo.get_by_id(did, self._db)]
            if invalid:
                raise ValueError(f"IDs de dispositivo no encontrados: {invalid}")

        group = await self._group_repo.create(name=name, description=description, db=self._db)

        if device_ids:
            await self._group_repo.add_devices(group.id, device_ids, self._db)

        return await self._build_response(group.id)

    async def update(self, group_id: int, name: str, description: str | None = None) -> DeviceGroupDetailResponse:
        await self._require_group(group_id)
        group = await self._group_repo.update(group_id, name, description, self._db)
        if group is None:
            raise ValueError(f"Grupo '{group_id}' no encontrado.")
        return await self._build_response(group_id)

    async def delete(self, group_id: int) -> None:
        await self._require_group(group_id)
        await self._group_repo.delete(group_id, self._db)

    async def add_devices(self, group_id: int, device_ids: list[int]) -> None:
        await self._require_group(group_id)
        invalid = [did for did in device_ids if not await self._device_repo.get_by_id(did, self._db)]
        if invalid:
            raise ValueError(f"IDs de dispositivo no encontrados: {invalid}")
        await self._group_repo.add_devices(group_id, device_ids, self._db)

    async def remove_device(self, group_id: int, device_id: int) -> None:
        await self._require_group(group_id)
        removed = await self._group_repo.remove_device(group_id, device_id, self._db)
        if not removed:
            raise ValueError(f"El dispositivo {device_id} no pertenece al grupo {group_id}.")

    async def get_by_id(self, group_id: int) -> DeviceGroupDetailResponse:
        await self._require_group(group_id)
        return await self._build_response(group_id)

    async def list_all(self) -> list[DeviceGroupDetailResponse]:
        groups = await self._group_repo.list_all(self._db)
        return [await self._build_response(g.id) for g in groups]

    async def resolve_serials_for_batch(self, group_id: int) -> list[str]:
        return await self._group_repo.get_serial_numbers(group_id, self._db)

    async def _build_response(self, group_id: int) -> DeviceGroupDetailResponse:
        group = await self._group_repo.get_by_id(group_id, self._db)
        devices = await self._device_repo.get_by_group_id(group_id, self._db)
        return DeviceGroupDetailResponse(
            id=group.id,
            name=group.name,
            description=group.description,
            devices=devices,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )

    async def _require_group(self, group_id: int) -> None:
        if not await self._group_repo.get_by_id(group_id, self._db):
            raise ValueError(f"Grupo '{group_id}' no encontrado.")
