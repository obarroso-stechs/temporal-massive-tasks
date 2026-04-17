from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.device_group_dependency import get_device_group_service
from api.schemas.device_groups import (
    AssignDevicesRequest,
    DeviceGroupCreate,
    DeviceGroupResponse,
    DeviceGroupUpdate,
)
from db.services.device_group_service import DeviceGroupService

router = APIRouter(prefix="/device-groups", tags=["device-groups"])


@router.post("", response_model=DeviceGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    payload: DeviceGroupCreate,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        return await service.create(
            name=payload.name,
            description=payload.description,
            device_ids=payload.device_ids,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("", response_model=list[DeviceGroupResponse])
async def list_groups(
    service: DeviceGroupService = Depends(get_device_group_service),
):
    return await service.list_all()


@router.get("/{group_id}", response_model=DeviceGroupResponse)
async def get_group(
    group_id: int,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        return await service.get_by_id(group_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{group_id}", response_model=DeviceGroupResponse)
async def update_group(
    group_id: int,
    payload: DeviceGroupUpdate,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        return await service.update(group_id, payload.name, payload.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        await service.delete(group_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{group_id}/devices", status_code=status.HTTP_204_NO_CONTENT)
async def assign_devices(
    group_id: int,
    payload: AssignDevicesRequest,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        await service.add_devices(group_id, payload.device_ids)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


@router.delete("/{group_id}/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_device_from_group(
    group_id: int,
    device_id: int,
    service: DeviceGroupService = Depends(get_device_group_service),
):
    try:
        await service.remove_device(group_id, device_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
