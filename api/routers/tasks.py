from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.task_dependency import get_task_service
from api.schemas.tasks import TaskDetailResponse, TaskSummaryResponse, TaskDeviceStatusResponse
from db.models.task import TaskTypeEnum
from db.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskSummaryResponse])
async def list_tasks(
    task_type: TaskTypeEnum | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    service: TaskService = Depends(get_task_service),
):
    return await service.list_tasks(task_type=task_type, date_from=date_from, date_to=date_to)


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    try:
        detail = await service.get_task_detail(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return TaskDetailResponse(
        **{k: v for k, v in TaskSummaryResponse.model_validate(detail["task"]).model_dump().items()},
        total_devices=detail["total_devices"],
        processed_devices=detail["processed_devices"],
        failed_devices=detail["failed_devices"],
        devices=[TaskDeviceStatusResponse.model_validate(d) for d in detail["devices"]],
    )


