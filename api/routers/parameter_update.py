from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from temporalio.client import Client

from dependencies import get_temporal_client
from schemas import (
    ParameterBatchRequest,
    ParameterBatchScheduledRequest,
    ParameterBatchStartResponse,
    WorkflowStatusResponse,
)
from service import _start_parameter_batch, compute_start_delay
from temporal.models import UpdateParameter

router = APIRouter(prefix="/parameter-update", tags=["parameter-update"])


def _to_domain_items(payload: ParameterBatchRequest) -> list[UpdateParameter]:
    return [
        UpdateParameter(serialNumber=item.serialNumber)
        for item in payload.items
    ]


@router.post(
    "/batch/start-now",
    response_model=ParameterBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_batch_now(
    payload: ParameterBatchRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> ParameterBatchStartResponse:
    workflow_id, run_id = await _start_parameter_batch(
        client=temporal_client,
        items=_to_domain_items(payload),
    )

    return ParameterBatchStartResponse(
        workflow_id=workflow_id,
        run_id=run_id,
        scheduled=False,
        accepted_at=datetime.now(UTC),
    )


@router.post(
    "/batch/schedule",
    response_model=ParameterBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def schedule_batch(
    payload: ParameterBatchScheduledRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> ParameterBatchStartResponse:
    try:
        start_delay = compute_start_delay(payload.start_at.astimezone(UTC))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    workflow_id, run_id = await _start_parameter_batch(
        client=temporal_client,
        items=_to_domain_items(payload),
        start_delay=start_delay,
    )

    return ParameterBatchStartResponse(
        workflow_id=workflow_id,
        run_id=run_id,
        scheduled=True,
        accepted_at=datetime.now(UTC),
        start_at=payload.start_at.astimezone(UTC),
    )


@router.get(
    "/batch/{workflow_id}/status",
    response_model=WorkflowStatusResponse,
)
async def get_batch_status(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> WorkflowStatusResponse:
    handle = temporal_client.get_workflow_handle(workflow_id)

    try:
        description = await handle.describe()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found: {exc}",
        ) from exc

    wf_status = description.status.name if description.status else "UNKNOWN"

    result = None
    if wf_status == "COMPLETED":
        try:
            raw_result = await handle.result()
            result = raw_result
        except Exception:
            pass

    return WorkflowStatusResponse(
        workflow_id=workflow_id,
        status=wf_status,
        result=result,
    )
