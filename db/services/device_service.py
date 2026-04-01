from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.device import Device
from db.repositories.device_repository import DeviceRepository
from db.schemas.device import DeviceResponse


class DeviceService:

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = DeviceRepository()

    async def create(
        self,
        serial_number: str,
        description: str | None,
        manufacturer: str | None,
        model: str | None,
        software_version: str | None,
        firmware_version: str | None,
    ) -> Device:
        existing = await self._repo.get_by_serial_number(serial_number, self._db)
        if existing:
            raise ValueError(f"Device with serial_number '{serial_number}' already exists.")
        return await self._repo.create(
            serial_number=serial_number,
            description=description,
            manufacturer=manufacturer,
            model=model,
            software_version=software_version,
            firmware_version=firmware_version,
            db=self._db,
        )

    async def update(
        self,
        serial_number: str,
        **fields,
    ) -> Device:
        await self._require_exists(serial_number)
        device = await self._repo.update(serial_number, self._db, **fields)
        if device is None:
            raise ValueError(f"Device '{serial_number}' not found.")
        return device

    async def delete(self, serial_number: str) -> None:
        await self._require_exists(serial_number)
        await self._repo.delete(serial_number, self._db)

    async def get_by_serial_number(self, serial_number: str) -> DeviceResponse:
        device = await self._repo.get_by_serial_number(serial_number, self._db)
        if device is None:
            raise ValueError(f"Device '{serial_number}' not found.")
        return device

    async def list_all(self) -> list[DeviceResponse]:
        return await self._repo.list_all(self._db)

    async def _require_exists(self, serial_number: str) -> None:
        if not await self._repo.get_by_serial_number(serial_number, self._db):
            raise ValueError(f"Device '{serial_number}' not found.")
