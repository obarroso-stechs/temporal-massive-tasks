from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from temporalio.client import Client

from dependencies import get_temporal_client
from schemas import (
    FirmwareBatchRequest,
    FirmwareBatchScheduledRequest,
    FirmwareBatchStartResponse,
    WorkflowStatusResponse,
)
from service import _start_firmware_batch, compute_start_delay
from temporal.models import UpdateFirmware

router = APIRouter(prefix="/firmware", tags=["firmware"])


def _to_domain_items(payload: FirmwareBatchRequest) -> list[UpdateFirmware]:
    return [
        UpdateFirmware(
            serialNumber=item.serialNumber,
            filename=item.filename,
        )
        for item in payload.items
    ]


@router.post(
    "/batch/start-now",
    response_model=FirmwareBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_batch_now(
    payload: FirmwareBatchRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> FirmwareBatchStartResponse:
    workflow_id, run_id = await _start_firmware_batch(
        client=temporal_client,
        items=_to_domain_items(payload),
    )

    return FirmwareBatchStartResponse(
        workflow_id=workflow_id,
        run_id=run_id,
        scheduled=False,
        accepted_at=datetime.now(UTC),
    )


@router.post(
    "/batch/schedule",
    response_model=FirmwareBatchStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def schedule_batch(
    payload: FirmwareBatchScheduledRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> FirmwareBatchStartResponse:
    try:
        start_delay = compute_start_delay(payload.start_at.astimezone(UTC))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    workflow_id, run_id = await _start_firmware_batch(
        client=temporal_client,
        items=_to_domain_items(payload),
        start_delay=start_delay,
    )

    return FirmwareBatchStartResponse(
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
    """Consulta el estado de un workflow de firmware batch.

    - Si el workflow terminó (COMPLETED), retorna el resultado.
    - Si sigue corriendo (RUNNING), retorna solo el status.
    - Si falló (FAILED/TERMINATED/TIMED_OUT), retorna el status.
    """
    handle = temporal_client.get_workflow_handle(workflow_id)

    try:
        description = await handle.describe()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found: {exc}",
        ) from exc

    wf_status = description.status.name if description.status else "UNKNOWN"

    # Si ya completó, obtenemos el resultado
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
