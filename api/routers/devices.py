from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.device_dependency import get_device_service
from api.schemas.devices import DeviceCreate, DeviceResponse, DeviceUpdate
from db.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    payload: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
):
    try:
        return await service.create(
            serial_number=payload.serial_number,
            description=payload.description,
            manufacturer=payload.manufacturer,
            model=payload.model,
            software_version=payload.software_version,
            firmware_version=payload.firmware_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("", response_model=list[DeviceResponse])
async def list_devices(
    service: DeviceService = Depends(get_device_service),
):
    return await service.list_all()


@router.get("/{serial_number}", response_model=DeviceResponse)
async def get_device(
    serial_number: str,
    service: DeviceService = Depends(get_device_service),
):
    try:
        return await service.get_by_serial_number(serial_number)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{serial_number}", response_model=DeviceResponse)
async def update_device(
    serial_number: str,
    payload: DeviceUpdate,
    service: DeviceService = Depends(get_device_service),
):
    try:
        return await service.update(serial_number, **payload.model_dump(exclude_none=True))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    serial_number: str,
    service: DeviceService = Depends(get_device_service),
):
    try:
        await service.delete(serial_number)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
