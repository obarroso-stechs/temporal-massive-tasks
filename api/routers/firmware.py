from __future__ import annotations

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
    FirmwareBatchRequest,
    FirmwareBatchScheduledRequest,
    FirmwareBatchStartResponse,
    WorkflowStatusResponse,
)
from service import _start_firmware_batch, compute_start_delay
from temporal.models import UpdateFirmware
from temporal.workflows.parent_workflow import FirmwareUpdateBatchWorkflow
from utils import enrich_events_with_pending_activities, group_child_events_by_device, parse_workflow_events

router = APIRouter(prefix="/firmware", tags=["firmware"])


def _to_domain_items(payload: FirmwareBatchRequest) -> list[UpdateFirmware]:
    return [
        UpdateFirmware(
            serialNumber=item.serialNumber,
            filename=item.filename,
        )
        for item in payload.items
    ]


# ── Endpoints de inicio ──────────────────────────────────────────


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
    child_workflow_id = f"{workflow_id}-{serial_number}"
    child_handle = temporal_client.get_workflow_handle(child_workflow_id)

    try:
        description = await child_handle.describe()
    except RPCError:
        # Child workflow no existe: verificar si esta PENDING en el parent
        parent_handle = temporal_client.get_workflow_handle(workflow_id)
        try:
            device_statuses = await parent_handle.query(
                FirmwareUpdateBatchWorkflow.get_device_statuses
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device '{serial_number}' not found in workflow '{workflow_id}'",
            )

        if serial_number in device_statuses:
            return DeviceStatusResponse(
                workflow_id=child_workflow_id,
                serial_number=serial_number,
                status=DeviceExecutionStatus(device_statuses[serial_number]),
                result=None,
                events=[],
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{serial_number}' not found in workflow '{workflow_id}'",
        )

    # Child workflow existe: obtener status, history y resultado
    wf_status = description.status.name if description.status else "UNKNOWN"
    device_status = _temporal_status_to_device_status(wf_status)

    # Fetch event history
    history = await child_handle.fetch_history()
    events = parse_workflow_events(history)

    # Enriquecer ACTIVITY_TASK_SCHEDULED con activity_result de pending activities
    events = enrich_events_with_pending_activities(events, description.raw_description)

    # Resultado si completó
    result = None
    if wf_status == "COMPLETED":
        try:
            result = _normalize_device_result(await child_handle.result())
        except Exception:
            pass

    return DeviceStatusResponse(
        workflow_id=child_workflow_id,
        serial_number=serial_number,
        status=device_status,
        result=result,
        events=events,
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
    """Consulta el estado de un batch con detalle por equipo.

    Retorna el progreso, la lista de devices con su status y events
    agrupados del parent history, y el resultado si completó.
    """
    return await _build_batch_status(workflow_id, temporal_client)


# ── Caso 3: Estado de multiples batches ──────────────────────────


@router.post(
    "/batch/group/status",
    response_model=BatchGroupStatusResponse,
)
async def get_group_status(
    payload: BatchGroupStatusRequest,
    temporal_client: Client = Depends(get_temporal_client),
) -> BatchGroupStatusResponse:
    """Consulta el estado agregado de multiples batches."""
    batches: list[WorkflowStatusResponse] = []

    for wf_id in payload.workflow_ids:
        try:
            batch_status = await _build_batch_status(wf_id, temporal_client)
            batches.append(batch_status)
        except HTTPException:
            # Si un workflow no existe, reportar como NOT_FOUND
            batches.append(
                WorkflowStatusResponse(
                    workflow_id=wf_id,
                    status="NOT_FOUND",
                    progress=None,
                    devices=[],
                )
            )

    # Calcular summary
    total_devices = 0
    total_processed = 0
    total_pending = 0
    total_failed = 0
    completed_batches = 0
    running_batches = 0
    failed_batches = 0

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
    """Construye el status completo de un batch con devices y events."""
    handle = temporal_client.get_workflow_handle(workflow_id)

    try:
        description = await handle.describe()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found: {exc}",
        ) from exc

    wf_status = description.status.name if description.status else "UNKNOWN"

    # Obtener progreso y estados de devices via queries
    progress = None
    device_statuses: dict[str, str] = {}
    if wf_status == "RUNNING":
        try:
            raw_progress = await handle.query(
                FirmwareUpdateBatchWorkflow.get_progress
            )
            progress = BatchProgress(**raw_progress)
        except Exception:
            pass

        try:
            device_statuses = await handle.query(
                FirmwareUpdateBatchWorkflow.get_device_statuses
            )
        except Exception:
            pass

    # Fetch event history del parent y agrupar por device
    history = await handle.fetch_history()
    events_by_device = group_child_events_by_device(history, workflow_id)

    # Resultado interno si completó (solo para derivar estados finales)
    completed_result = None
    if wf_status == "COMPLETED":
        try:
            completed_result = _normalize_workflow_result(await handle.result())
        except Exception:
            pass

        # Cuando el workflow completó, derivar device statuses del resultado
        if completed_result and not device_statuses:
            for item in completed_result:
                if isinstance(item, dict) and "serial_number" in item:
                    serial_number = item.get("serial_number")
                    if serial_number:
                        device_statuses[serial_number] = "COMPLETED"
                elif isinstance(item, str) and item.startswith("ERROR ["):
                    # Extraer serial de "ERROR [serial]: ..."
                    try:
                        sn = item.split("[")[1].split("]")[0]
                        device_statuses[sn] = "FAILED"
                    except (IndexError, ValueError):
                        pass

    # Construir lista de devices con events
    all_serials = set(device_statuses.keys()) | set(events_by_device.keys())
    devices: list[DeviceWithEvents] = []
    for serial in sorted(all_serials):
        ds = device_statuses.get(serial, "PENDING")
        devices.append(
            DeviceWithEvents(
                serial_number=serial,
                status=DeviceExecutionStatus(ds),
                events=events_by_device.get(serial, []),
            )
        )

    # Si el workflow completó y no teniamos progress, calcularlo
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


def _temporal_status_to_device_status(
    temporal_status: str,
) -> DeviceExecutionStatus:
    """Mapea el status de Temporal al enum DeviceExecutionStatus."""
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
    """Normaliza un item de resultado de Temporal a dict/str serializable."""
    if item is None:
        return None
    if isinstance(item, (dict, str)):
        return item
    if is_dataclass(item):
        return asdict(item)

    serial_number = getattr(item, "serial_number", None)
    filename = getattr(item, "filename", None)
    status = getattr(item, "status", None)
    if serial_number is not None or filename is not None or status is not None:
        return {
            "serial_number": serial_number,
            "filename": filename,
            "status": status,
        }
    return None


def _normalize_workflow_result(result: object) -> list[dict | str] | None:
    """Normaliza el resultado del parent workflow a lista serializable."""
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
    """Normaliza el resultado del child workflow a dict compatible con schema."""
    normalized = _normalize_result_item(result)
    if isinstance(normalized, dict):
        return normalized
    return None
