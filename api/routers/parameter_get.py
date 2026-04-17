from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from temporalio.client import Client
from temporalio.service import RPCError

from api.schemas.parameter_get import (
    ParameterGetBatchRequest,
    ParameterGetBatchScheduledRequest,
    ParameterGetBatchStartResponse,
)
from api.schemas.workflow import (
    BatchGroupStatusRequest,
    BatchGroupStatusResponse,
    DeviceStatusResponse,
    WorkflowStatusResponse,
)
from api.dependencies.task_dependency import get_task_service
from api.dependencies.temporal import get_temporal_client
from api.services.service import BatchOrchestrationService, get_batch_orchestration_service
from api.services.workflow_status_service import WorkflowStatusService
from db.services.task_service import TaskService
from temporal.workflows.get_parameter_values.get_parameter_values_workflow import GetParameterValuesBatchWorkflow

router = APIRouter(prefix="/parameter-get", tags=["parameter-get"])


def get_workflow_status_service() -> WorkflowStatusService:
    return WorkflowStatusService(GetParameterValuesBatchWorkflow)


@router.post(
    "/batch/start-now",
    response_model=ParameterGetBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_batch_now(
    payload: ParameterGetBatchRequest,
    temporal_client: Client = Depends(get_temporal_client),
    orchestration: BatchOrchestrationService = Depends(get_batch_orchestration_service),
) -> ParameterGetBatchStartResponse:
    try:
        workflow_id, run_id = await orchestration.start_get_parameter_values_batch(
            client=temporal_client,
            serial_numbers=[i.serialNumber for i in payload.items] if payload.items else None,
            group_id=payload.group_id,
            paths=payload.paths,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return ParameterGetBatchStartResponse(
        workflow_id=workflow_id,
        run_id=run_id,
        scheduled=False,
        accepted_at=datetime.now(UTC),
    )


@router.post(
    "/batch/schedule",
    response_model=ParameterGetBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def schedule_batch(
    payload: ParameterGetBatchScheduledRequest,
    temporal_client: Client = Depends(get_temporal_client),
    orchestration: BatchOrchestrationService = Depends(get_batch_orchestration_service),
) -> ParameterGetBatchStartResponse:
    try:
        start_delay = BatchOrchestrationService.compute_start_delay(payload.start_at.astimezone(UTC))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    try:
        workflow_id, run_id = await orchestration.start_get_parameter_values_batch(
            client=temporal_client,
            serial_numbers=[i.serialNumber for i in payload.items] if payload.items else None,
            group_id=payload.group_id,
            paths=payload.paths,
            start_delay=start_delay,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return ParameterGetBatchStartResponse(
        workflow_id=workflow_id,
        run_id=run_id,
        scheduled=True,
        accepted_at=datetime.now(UTC),
        start_at=payload.start_at.astimezone(UTC),
    )


@router.get(
    "/batch/{workflow_id}/device/{serial_number}/status",
    response_model=DeviceStatusResponse,
)
async def get_device_status(
    workflow_id: str,
    serial_number: str,
    temporal_client: Client = Depends(get_temporal_client),
    wf_service: WorkflowStatusService = Depends(get_workflow_status_service),
    task_service: TaskService = Depends(get_task_service),
) -> DeviceStatusResponse:
    try:
        return await wf_service.get_device_status(
            workflow_id=workflow_id,
            serial_number=serial_number,
            temporal_client=temporal_client,
            raise_if_missing=True,
        )
    except HTTPException as exc:
        if exc.status_code != status.HTTP_404_NOT_FOUND:
            raise
        return await wf_service.get_device_status_from_db(workflow_id, serial_number, task_service)


@router.get(
    "/batch/{workflow_id}/status",
    response_model=WorkflowStatusResponse,
)
async def get_batch_status(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
    wf_service: WorkflowStatusService = Depends(get_workflow_status_service),
    task_service: TaskService = Depends(get_task_service),
) -> WorkflowStatusResponse:
    try:
        return await wf_service.get_batch_status(workflow_id, temporal_client, task_service)
    except HTTPException as exc:
        if exc.status_code != status.HTTP_404_NOT_FOUND:
            raise
        return await wf_service.get_batch_status_from_db(workflow_id, task_service)


@router.post("/batch/{workflow_id}/pause")
async def pause_batch(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> dict:
    handle = temporal_client.get_workflow_handle(workflow_id)
    try:
        await handle.signal(GetParameterValuesBatchWorkflow.pause_batch)
    except RPCError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"workflow_id": workflow_id, "action": "pause"}


@router.post("/batch/{workflow_id}/resume")
async def resume_batch(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> dict:
    handle = temporal_client.get_workflow_handle(workflow_id)
    try:
        await handle.signal(GetParameterValuesBatchWorkflow.resume_batch)
    except RPCError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"workflow_id": workflow_id, "action": "resume"}


@router.post("/batch/{workflow_id}/cancel")
async def cancel_batch(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
    task_service: TaskService = Depends(get_task_service),
) -> dict:
    handle = temporal_client.get_workflow_handle(workflow_id)
    try:
        await handle.cancel()
    except RPCError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    raw = await task_service.get_batch_status_raw(workflow_id)
    if raw:
        non_terminal = [
            d.serial_number for d in raw["devices"]
            if d.status.value not in ("COMPLETED", "FAILED", "CANCELED", "TIMED_OUT")
        ]
        await task_service.mark_canceled(workflow_id, non_terminal, datetime.now(UTC))

    return {"workflow_id": workflow_id, "action": "cancel"}


@router.post(
    "/batch/group/status",
    response_model=BatchGroupStatusResponse,
)
async def get_group_status(
    payload: BatchGroupStatusRequest,
    temporal_client: Client = Depends(get_temporal_client),
    wf_service: WorkflowStatusService = Depends(get_workflow_status_service),
) -> BatchGroupStatusResponse:
    return await wf_service.get_group_status(payload, temporal_client)
