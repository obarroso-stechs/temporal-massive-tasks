from __future__ import annotations

import ast
import json
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from temporalio.client import Client
from temporalio.service import RPCError

from dependencies import get_temporal_client
from schemas import (
    BatchProgress,
    DeviceExecutionStatus,
    DeviceStatusItem,
    DeviceStatusResponse,
    ParameterBatchRequest,
    ParameterBatchScheduledRequest,
    ParameterBatchStartResponse,
    WorkflowStatusResponse,
)
from service import _start_parameter_batch, compute_start_delay
from temporal.models import UpdateParameter
from temporal.workflows.parameter_update.parameter_update_workflow import ParameterUpdateBatchWorkflow
from utils import (
    extract_client_detail_from_event_details,
    extract_retrying_detail,
    group_child_events_by_device,
    parse_workflow_events,
)

router = APIRouter(prefix="/parameter-update", tags=["parameter-update"])

SUCCESS_DETAIL = "Parameter update executed successfully"


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
    "/batch/{workflow_id}/device/{serial_number}/status",
    response_model=DeviceStatusResponse,
)
async def get_device_status(
    workflow_id: str,
    serial_number: str,
    temporal_client: Client = Depends(get_temporal_client),
) -> DeviceStatusResponse:
    """Consulta el estado de un equipo individual dentro de un batch."""
    child_workflow_id = f"{workflow_id}-{serial_number}"
    child_handle = temporal_client.get_workflow_handle(child_workflow_id)

    try:
        description = await child_handle.describe()
    except RPCError:
        # Child workflow no existe: verificar si está PENDING en el parent
        parent_handle = temporal_client.get_workflow_handle(workflow_id)
        try:
            device_statuses = await parent_handle.query(
                ParameterUpdateBatchWorkflow.get_device_statuses
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
                detail=None,
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{serial_number}' not found in workflow '{workflow_id}'",
        )

    wf_status = description.status.name if description.status else "UNKNOWN"
    device_status = _temporal_status_to_device_status(wf_status)

    detail = None
    if wf_status == "RUNNING":
        retrying_detail = extract_retrying_detail(description.raw_description)
        if retrying_detail:
            device_status = DeviceExecutionStatus.RETRYING
            detail = retrying_detail
    elif wf_status == "COMPLETED":
        try:
            result = _normalize_device_result(await child_handle.result())
            detail = result.get("status") if result else None
        except Exception:
            detail = None
        detail = _normalize_client_detail(detail)
        if not detail:
            detail = SUCCESS_DETAIL
    elif wf_status in ("FAILED", "TIMED_OUT", "TERMINATED", "CANCELED"):
        try:
            history = await child_handle.fetch_history()
            events = parse_workflow_events(history)
            detail = _extract_detail_from_events(events)
        except Exception:
            detail = "Internal server error"
        if not detail:
            detail = "Internal server error"

    return DeviceStatusResponse(
        workflow_id=child_workflow_id,
        serial_number=serial_number,
        status=device_status,
        detail=detail,
    )


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

    completed_result = None
    if wf_status == "COMPLETED":
        try:
            completed_result = _normalize_workflow_result(await handle.result())
        except Exception:
            pass

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

    result_details: dict[str, str] = {}
    if completed_result:
        for item in completed_result:
            if isinstance(item, dict) and "serial_number" in item:
                sn = item.get("serial_number")
                if sn:
                    detail_value = item.get("message") or item.get("status")
                    result_details[sn] = (
                        detail_value if isinstance(detail_value, str) and detail_value else "success"
                    )
            elif isinstance(item, str) and item.startswith("ERROR ["):
                try:
                    sn = item.split("[")[1].split("]")[0]
                    detail = item.split(": ", 1)[1] if ": " in item else item
                    result_details[sn] = detail
                except (IndexError, ValueError):
                    pass

    devices: list[DeviceStatusItem] = []
    for serial in sorted(all_serials):
        ds = device_statuses.get(serial, "PENDING")
        terminal_status = _terminal_status_from_events(events_by_device.get(serial, []))
        if terminal_status is not None:
            ds = terminal_status.value

        event_detail = _extract_detail_from_events(events_by_device.get(serial, []))
        result_detail = result_details.get(serial)

        if ds in {
            DeviceExecutionStatus.FAILED.value,
            DeviceExecutionStatus.TIMED_OUT.value,
            DeviceExecutionStatus.TERMINATED.value,
            DeviceExecutionStatus.CANCELED.value,
        }:
            detail = event_detail or result_detail
        else:
            detail = result_detail or event_detail

        detail = _normalize_client_detail(detail)

        if ds == DeviceExecutionStatus.COMPLETED.value and not detail:
            detail = SUCCESS_DETAIL

        devices.append(
            DeviceStatusItem(
                serial_number=serial,
                status=DeviceExecutionStatus(ds),
                detail=detail,
            )
        )

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
        return {
            "serial_number": serial_number,
            "status": status_val,
            "message": message,
        }
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


def _terminal_status_from_events(events: list[dict]) -> DeviceExecutionStatus | None:
    terminal_mapping = {
        "CHILD_WORKFLOW_EXECUTION_COMPLETED": DeviceExecutionStatus.COMPLETED,
        "CHILD_WORKFLOW_EXECUTION_FAILED": DeviceExecutionStatus.FAILED,
        "CHILD_WORKFLOW_EXECUTION_TIMED_OUT": DeviceExecutionStatus.TIMED_OUT,
        "CHILD_WORKFLOW_EXECUTION_TERMINATED": DeviceExecutionStatus.TERMINATED,
        "CHILD_WORKFLOW_EXECUTION_CANCELED": DeviceExecutionStatus.CANCELED,
    }
    for event in reversed(events):
        event_type = event.get("event_type")
        if event_type in terminal_mapping:
            return terminal_mapping[event_type]
    return None


def _extract_detail_from_events(events: list[dict]) -> str | None:
    for event in reversed(events):
        details = event.get("details")
        if not isinstance(details, dict):
            continue
        detail = extract_client_detail_from_event_details(details)
        if detail:
            return detail
    return None


def _normalize_client_detail(detail: str | None) -> str | None:
    if not detail:
        return None

    text = detail.strip()
    if not text:
        return None

    if text == "Child Workflow execution failed":
        return None

    parsed = _try_parse_mapping(text)
    if parsed:
        result_value = str(parsed.get("result", "")).strip().lower()
        if result_value == "success":
            return SUCCESS_DETAIL
        for key in ("errorStrDetail", "errorStr", "message", "detail"):
            value = parsed.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return text


def _try_parse_mapping(raw: str) -> dict | None:
    try:
        maybe_obj = ast.literal_eval(raw)
        if isinstance(maybe_obj, dict):
            return maybe_obj
    except (SyntaxError, ValueError):
        pass
    if raw.startswith("{") and raw.endswith("}") and "\"result\"" in raw:
        try:
            maybe_obj = json.loads(raw)
            if isinstance(maybe_obj, dict):
                return maybe_obj
        except (json.JSONDecodeError, TypeError):
            return None
    return None
