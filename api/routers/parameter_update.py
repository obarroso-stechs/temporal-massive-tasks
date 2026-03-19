from __future__ import annotations

import asyncio
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from temporalio.client import Client
from temporalio.service import RPCError

from dependencies import get_temporal_client
from schemas import (
    BatchGroupStatusRequest,
    BatchGroupStatusResponse,
    BatchGroupSummary,
    BatchProgress,
    DeviceExecutionStatus,
    DeviceStatusResponse,
    DeviceWithEvents,
    ParameterBatchRequest,
    ParameterBatchScheduledRequest,
    ParameterBatchStartResponse,
    WorkflowStatusResponse,
)
from service import _start_parameter_batch, compute_start_delay
from temporal.models import UpdateParameter
from temporal.workflows.parameter_update.parameter_update_workflow import ParameterUpdateBatchWorkflow
from utils import enrich_events_with_pending_activities, group_child_events_by_device, parse_workflow_events

router = APIRouter(prefix="/parameter-update", tags=["parameter-update"])


def _to_domain_items(payload: ParameterBatchRequest) -> list[UpdateParameter]:
    return [
        UpdateParameter(serialNumber=item.serialNumber)
        for item in payload.items
    ]


# ── Endpoints de inicio ──────────────────────────────────────────


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


# ── Caso 1: Estado individual de un equipo ───────────────────────


@router.get(
    "/batch/{workflow_id}/device/{serial_number}/status",
    response_model=DeviceStatusResponse,
)
async def get_device_status(
    workflow_id: str,
    serial_number: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> DeviceStatusResponse:
    """Consulta el estado de un equipo individual dentro de un batch.

    Construye el child workflow ID como {workflow_id}-{serial_number}
    y consulta su estado y event history completo.
    """
    return await _build_device_status_detail(
        workflow_id=workflow_id,
        serial_number=serial_number,
        temporal_client=temporal_client,
        raise_if_missing=True,
    )


# ── Caso 2: Estado del batch con devices y events ────────────────


@router.get(
    "/batch/{workflow_id}/status",
    response_model=WorkflowStatusResponse,
)
async def get_batch_status(
    workflow_id: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> WorkflowStatusResponse:
    """Consulta el estado de un batch con detalle por equipo."""
    return await _build_batch_status(workflow_id, temporal_client)


# ── Caso 3: Estado de múltiples batches ──────────────────────────


@router.post(
    "/batch/group/status",
    response_model=BatchGroupStatusResponse,
)
async def get_group_status(
    payload: BatchGroupStatusRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> BatchGroupStatusResponse:
    """Consulta el estado agregado de múltiples batches."""
    batches: list[WorkflowStatusResponse] = []

    for wf_id in payload.workflow_ids:
        try:
            batch_status = await _build_batch_status(wf_id, temporal_client)
            batches.append(batch_status)
        except HTTPException:
            batches.append(
                WorkflowStatusResponse(
                    workflow_id=wf_id,
                    status="NOT_FOUND",
                    progress=None,
                    devices=[],
                )
            )

    total_devices = total_processed = total_pending = total_failed = 0
    completed_batches = running_batches = failed_batches = 0

    for b in batches:
        if b.progress:
            total_devices += b.progress.total
            total_processed += b.progress.processed
            total_pending += b.progress.pending
            total_failed += b.progress.failed
        else:
            total_devices += len(b.devices)

        if b.status == "COMPLETED":
            completed_batches += 1
        elif b.status == "RUNNING":
            running_batches += 1
        elif b.status in ("FAILED", "TERMINATED", "TIMED_OUT", "CANCELED"):
            failed_batches += 1

    return BatchGroupStatusResponse(
        batches=batches,
        summary=BatchGroupSummary(
            total_batches=len(batches),
            completed_batches=completed_batches,
            running_batches=running_batches,
            failed_batches=failed_batches,
            total_devices=total_devices,
            total_processed=total_processed,
            total_pending=total_pending,
            total_failed=total_failed,
            all_completed=completed_batches == len(batches),
        ),
    )


# ── Helpers ───────────────────────────────────────────────────────


async def _build_batch_status(
    workflow_id: str,
    temporal_client: Client,
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

    progress = None
    device_statuses: dict[str, str] = {}
    if wf_status == "RUNNING":
        try:
            raw_progress = await handle.query(ParameterUpdateBatchWorkflow.get_progress)
            progress = BatchProgress(**raw_progress)
        except Exception:
            pass

        try:
            device_statuses = await handle.query(
                ParameterUpdateBatchWorkflow.get_device_statuses
            )
        except Exception:
            pass

    history = await handle.fetch_history()
    events_by_device = group_child_events_by_device(history, workflow_id)

    if wf_status == "COMPLETED":
        try:
            completed_result = _normalize_workflow_result(await handle.result())
        except Exception:
            completed_result = None

        if completed_result and not device_statuses:
            for item in completed_result:
                if isinstance(item, dict) and "serial_number" in item:
                    sn = item.get("serial_number")
                    if sn:
                        device_statuses[sn] = "COMPLETED"
                elif isinstance(item, str) and item.startswith("ERROR ["):
                    try:
                        sn = item.split("[")[1].split("]")[0]
                        device_statuses[sn] = "FAILED"
                    except (IndexError, ValueError):
                        pass

    all_serials = set(device_statuses.keys()) | set(events_by_device.keys())
    device_details = await asyncio.gather(
        *[
            _build_device_status_detail(
                workflow_id=workflow_id,
                serial_number=serial,
                temporal_client=temporal_client,
                known_status=DeviceExecutionStatus(device_statuses.get(serial, "PENDING")),
                fallback_events=events_by_device.get(serial, []),
                raise_if_missing=False,
            )
            for serial in sorted(all_serials)
        ]
    )

    devices: list[DeviceWithEvents] = [
        DeviceWithEvents(
            workflow_id=item.workflow_id,
            serial_number=item.serial_number,
            status=item.status,
            message=item.message,
            events=item.events,
        )
        for item in device_details
    ]

    if wf_status == "COMPLETED" and progress is None and devices:
        completed = sum(1 for d in devices if d.status == DeviceExecutionStatus.COMPLETED)
        failed = sum(1 for d in devices if d.status == DeviceExecutionStatus.FAILED)
        progress = BatchProgress(
            total=len(devices),
            processed=completed + failed,
            pending=0,
            failed=failed,
        )

    return WorkflowStatusResponse(
        workflow_id=workflow_id,
        status=wf_status,
        progress=progress,
        devices=devices,
    )


def _temporal_status_to_device_status(temporal_status: str) -> DeviceExecutionStatus:
    mapping = {
        "RUNNING": DeviceExecutionStatus.RUNNING,
        "COMPLETED": DeviceExecutionStatus.COMPLETED,
        "FAILED": DeviceExecutionStatus.FAILED,
        "TIMED_OUT": DeviceExecutionStatus.TIMED_OUT,
        "TERMINATED": DeviceExecutionStatus.TERMINATED,
        "CANCELED": DeviceExecutionStatus.CANCELED,
    }
    return mapping.get(temporal_status, DeviceExecutionStatus.PENDING)


def _normalize_result_item(item: object) -> dict | str | None:
    if item is None:
        return None
    if isinstance(item, (dict, str)):
        return item
    if is_dataclass(item):
        return asdict(item)

    serial_number = getattr(item, "serial_number", None)
    status_val = getattr(item, "status", None)
    message = getattr(item, "message", None)
    if serial_number is not None or status_val is not None:
        return {"serial_number": serial_number, "status": status_val, "message": message}
    return None


def _normalize_workflow_result(result: object) -> list[dict | str] | None:
    if result is None:
        return None
    if not isinstance(result, list):
        normalized_item = _normalize_result_item(result)
        return [normalized_item] if normalized_item is not None else None

    normalized: list[dict | str] = []
    for item in result:
        normalized_item = _normalize_result_item(item)
        if normalized_item is not None:
            normalized.append(normalized_item)
    return normalized


def _normalize_device_result(result: object) -> dict | None:
    normalized = _normalize_result_item(result)
    if isinstance(normalized, dict):
        return normalized
    return None


async def _build_device_status_detail(
    workflow_id: str,
    serial_number: str,
    temporal_client: Client,
    *,
    known_status: DeviceExecutionStatus | None = None,
    fallback_events: list[dict] | None = None,
    raise_if_missing: bool,
) -> DeviceStatusResponse:
    child_workflow_id = f"{workflow_id}-{serial_number}"
    child_handle = temporal_client.get_workflow_handle(child_workflow_id)

    try:
        description = await child_handle.describe()
    except RPCError:
        if known_status is None:
            parent_handle = temporal_client.get_workflow_handle(workflow_id)
            try:
                device_statuses = await parent_handle.query(
                    ParameterUpdateBatchWorkflow.get_device_statuses
                )
            except Exception:
                device_statuses = {}

            if serial_number in device_statuses:
                known_status = DeviceExecutionStatus(device_statuses[serial_number])

        if known_status is not None:
            return DeviceStatusResponse(
                workflow_id=child_workflow_id,
                serial_number=serial_number,
                status=known_status,
                message=None,
                events=fallback_events or [],
            )

        if raise_if_missing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device '{serial_number}' not found in workflow '{workflow_id}'",
            )

        return DeviceStatusResponse(
            workflow_id=child_workflow_id,
            serial_number=serial_number,
            status=DeviceExecutionStatus.PENDING,
            message=None,
            events=fallback_events or [],
        )

    wf_status = description.status.name if description.status else "UNKNOWN"
    device_status = _temporal_status_to_device_status(wf_status)

    history = await child_handle.fetch_history()
    events = parse_workflow_events(history)
    events = enrich_events_with_pending_activities(events, description.raw_description)

    message = None
    if wf_status == "COMPLETED":
        try:
            normalized_result = _normalize_device_result(await child_handle.result())
            if normalized_result:
                raw_message = normalized_result.get("message")
                if isinstance(raw_message, str):
                    message = raw_message
        except Exception:
            pass

    return DeviceStatusResponse(
        workflow_id=child_workflow_id,
        serial_number=serial_number,
        status=device_status,
        message=message,
        events=events,
    )
