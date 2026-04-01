"""Shared workflow status logic for firmware and parameter-update routers.

Both batch types expose the same status endpoints — the only difference is
which parent workflow class is queried for live progress/device-statuses.
WorkflowStatusService is parameterised with that class at construction time.
"""

from __future__ import annotations

import asyncio
from dataclasses import asdict, is_dataclass
from typing import Any, Type

from fastapi import HTTPException, status
from temporalio.client import Client
from temporalio.service import RPCError

from api.schemas.workflow import (
    BatchGroupStatusRequest,
    BatchGroupStatusResponse,
    BatchGroupSummary,
    BatchProgress,
    DeviceExecutionStatus,
    DeviceStatusResponse,
    DeviceWithEvents,
    WorkflowStatusResponse,
)
from utils import enrich_events_with_pending_activities, group_child_events_by_device, infer_paused_from_history, parse_workflow_events

_STATUS_MAP: dict[str, DeviceExecutionStatus] = {
    "RUNNING": DeviceExecutionStatus.RUNNING,
    "COMPLETED": DeviceExecutionStatus.COMPLETED,
    "FAILED": DeviceExecutionStatus.FAILED,
    "TIMED_OUT": DeviceExecutionStatus.TIMED_OUT,
    "TERMINATED": DeviceExecutionStatus.TERMINATED,
    "CANCELED": DeviceExecutionStatus.CANCELED,
}


class WorkflowStatusService:
    """Query Temporal for batch and device-level status.

    Args:
        batch_workflow_class: The @workflow.defn class used for the parent
            batch (FirmwareUpdateBatchWorkflow or ParameterUpdateBatchWorkflow).
            Its ``get_progress`` and ``get_device_statuses`` query handlers
            are called when the workflow is RUNNING.
    """

    def __init__(self, batch_workflow_class: Any) -> None:
        self._batch_workflow_class = batch_workflow_class

    # ── Public API ────────────────────────────────────────────────────────────

    async def get_batch_status(
        self,
        workflow_id: str,
        temporal_client: Client,
        task_service: Any = None,
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
        is_paused = False
        device_statuses: dict[str, str] = {}
        if wf_status == "RUNNING":
            try:
                raw = await handle.query(self._batch_workflow_class.get_progress)
                is_paused = bool(raw.pop("is_paused", False))
                progress = BatchProgress(**raw)
            except Exception:
                pass
            try:
                device_statuses = await handle.query(
                    self._batch_workflow_class.get_device_statuses
                )
            except Exception:
                pass

        history = await handle.fetch_history()
        events_by_device = group_child_events_by_device(history, workflow_id)

        # Fallback: si el query falló (workflow en start_delay, worker no lo procesó aún),
        # inferir estado de pausa desde las señales del historial.
        if wf_status == "RUNNING" and not is_paused:
            is_paused = infer_paused_from_history(history)

        if wf_status == "COMPLETED":
            try:
                completed_result = self._normalize_workflow_result(await handle.result())
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

        # Fallback: workflow programado aún en delay — Temporal no tiene devices aún,
        # pero la DB ya tiene los registros creados al momento del scheduling.
        if not all_serials and task_service is not None:
            raw = await task_service.get_batch_status_raw(workflow_id)
            if raw:
                for d in raw["devices"]:
                    db_val = d.status.value
                    device_statuses[d.serial_number] = "PENDING" if db_val == "SCHEDULED" else db_val
                all_serials = set(device_statuses.keys())

        device_details = await asyncio.gather(
            *[
                self.get_device_status(
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

        if wf_status != "RUNNING" and progress is None and devices:
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
            is_paused=is_paused,
        )

    async def get_device_status(
        self,
        workflow_id: str,
        serial_number: str,
        temporal_client: Client,
        *,
        known_status: DeviceExecutionStatus | None = None,
        fallback_events: list[dict] | None = None,
        raise_if_missing: bool = True,
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
                        self._batch_workflow_class.get_device_statuses
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
                    message=self._extract_message_from_events(fallback_events or []),
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
                message=self._extract_message_from_events(fallback_events or []),
                events=fallback_events or [],
            )

        wf_status = description.status.name if description.status else "UNKNOWN"
        device_status = _STATUS_MAP.get(wf_status, DeviceExecutionStatus.PENDING)

        history = await child_handle.fetch_history()
        events = parse_workflow_events(history)
        events = enrich_events_with_pending_activities(events, description.raw_description)

        message = self._extract_message_from_events(events)
        if wf_status == "COMPLETED":
            try:
                normalized = self._normalize_device_result(await child_handle.result())
                result_message = self._extract_device_message(normalized)
                if result_message:
                    message = result_message
            except Exception:
                pass

        return DeviceStatusResponse(
            workflow_id=child_workflow_id,
            serial_number=serial_number,
            status=device_status,
            message=message,
            events=events,
        )

    async def get_batch_status_from_db(self, workflow_id: str, task_service: Any) -> WorkflowStatusResponse:
        """Fallback: build WorkflowStatusResponse from DB when Temporal is unavailable."""
        raw = await task_service.get_batch_status_raw(workflow_id)
        if raw is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow '{workflow_id}' not found",
            )
        task = raw["task"]
        devices = raw["devices"]
        counts = raw["counts"]

        _db_status_map: dict[str, DeviceExecutionStatus] = {
            "PENDING": DeviceExecutionStatus("PENDING"),
            "SCHEDULED": DeviceExecutionStatus("PENDING"),
            "RUNNING": DeviceExecutionStatus("RUNNING"),
            "COMPLETED": DeviceExecutionStatus("COMPLETED"),
            "FAILED": DeviceExecutionStatus("FAILED"),
            "CANCELED": DeviceExecutionStatus("CANCELED"),
            "TIMED_OUT": DeviceExecutionStatus("TIMED_OUT"),
        }

        device_list = [
            DeviceWithEvents(
                workflow_id=f"{workflow_id}-{d.serial_number}",
                serial_number=d.serial_number,
                status=_db_status_map.get(d.status.value, DeviceExecutionStatus("PENDING")),
                message=d.detail,
                events=[],
            )
            for d in devices
        ]

        if task.end_at is not None:
            canceled_count = sum(1 for d in devices if d.status.value == "CANCELED")
            failed_count = counts["failed"]
            if canceled_count > 0 and failed_count == 0:
                wf_status = "CANCELED"
            elif failed_count > 0:
                wf_status = "FAILED"
            else:
                wf_status = "COMPLETED"
        elif task.started_at is not None:
            wf_status = "RUNNING"
        else:
            wf_status = "PENDING"

        progress = BatchProgress(
            total=counts["total"],
            processed=counts["processed"],
            pending=counts["total"] - counts["processed"],
            failed=counts["failed"],
        )

        return WorkflowStatusResponse(
            workflow_id=workflow_id,
            status=wf_status,
            progress=progress,
            devices=device_list,
        )

    async def get_device_status_from_db(
        self, workflow_id: str, serial_number: str, task_service: Any
    ) -> DeviceStatusResponse:
        """Fallback: build DeviceStatusResponse from DB when Temporal is unavailable."""
        raw = await task_service.get_batch_status_raw(workflow_id)
        if raw is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow '{workflow_id}' not found",
            )
        devices = raw["devices"]
        device = next((d for d in devices if d.serial_number == serial_number), None)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device '{serial_number}' not found in workflow '{workflow_id}'",
            )
        _db_status_map: dict[str, DeviceExecutionStatus] = {
            "PENDING": DeviceExecutionStatus("PENDING"),
            "SCHEDULED": DeviceExecutionStatus("PENDING"),
            "RUNNING": DeviceExecutionStatus("RUNNING"),
            "COMPLETED": DeviceExecutionStatus("COMPLETED"),
            "FAILED": DeviceExecutionStatus("FAILED"),
            "CANCELED": DeviceExecutionStatus("CANCELED"),
            "TIMED_OUT": DeviceExecutionStatus("TIMED_OUT"),
        }
        return DeviceStatusResponse(
            workflow_id=f"{workflow_id}-{serial_number}",
            serial_number=serial_number,
            status=_db_status_map.get(device.status.value, DeviceExecutionStatus("PENDING")),
            message=device.detail,
            events=[],
        )

    async def get_group_status(
        self,
        payload: BatchGroupStatusRequest,
        temporal_client: Client,
    ) -> BatchGroupStatusResponse:
        batches: list[WorkflowStatusResponse] = []

        for wf_id in payload.workflow_ids:
            try:
                batches.append(await self.get_batch_status(wf_id, temporal_client))
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

    # ── Overrideable hook ─────────────────────────────────────────────────────

    def _extract_device_message(self, normalized_result: dict | None) -> str | None:
        """Extract a human-readable message from a child workflow result dict.

        Subclasses can override this to customise per-type message extraction.
        Default: reads the ``message`` key.
        """
        if not normalized_result:
            return None
        raw = normalized_result.get("message")
        return raw if isinstance(raw, str) and raw else None

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _normalize_result_item(self, item: object) -> dict | str | None:
        if item is None:
            return None
        if isinstance(item, (dict, str)):
            return item
        if is_dataclass(item):
            return asdict(item)
        serial_number = getattr(item, "serial_number", None)
        status_val = getattr(item, "status", None)
        message = getattr(item, "message", None)
        filename = getattr(item, "filename", None)
        if serial_number is not None or status_val is not None:
            return {
                "serial_number": serial_number,
                "status": status_val,
                "message": message,
                "filename": filename,
            }
        return None

    def _normalize_workflow_result(self, result: object) -> list[dict | str] | None:
        if result is None:
            return None
        if not isinstance(result, list):
            normalized = self._normalize_result_item(result)
            return [normalized] if normalized is not None else None
        return [n for item in result if (n := self._normalize_result_item(item)) is not None]

    def _normalize_device_result(self, result: object) -> dict | None:
        normalized = self._normalize_result_item(result)
        return normalized if isinstance(normalized, dict) else None

    def _extract_message_from_events(self, events: list[dict]) -> str | None:
        import json

        for event in reversed(events):
            details = event.get("details", {})
            failure = details.get("failure")
            if isinstance(failure, dict):
                msg = self._extract_failure_message(failure)
                if msg:
                    return msg
            raw_result = details.get("result")
            if isinstance(raw_result, str) and raw_result:
                try:
                    parsed = json.loads(raw_result)
                    if isinstance(parsed, dict):
                        s = parsed.get("status")
                        if isinstance(s, str) and s:
                            return s
                except Exception:
                    pass
                return raw_result
        return None

    def _extract_failure_message(self, failure: dict) -> str | None:
        cause = failure.get("cause")
        if isinstance(cause, dict):
            msg = self._extract_failure_message(cause)
            if msg:
                return msg
        message = failure.get("message")
        return message if isinstance(message, str) and message else None


class FirmwareWorkflowStatusService(WorkflowStatusService):
    """Firmware-specific: extracts message from filename/serial fields."""

    def _extract_device_message(self, normalized_result: dict | None) -> str | None:
        if not normalized_result:
            return None
        status_val = normalized_result.get("status")
        if isinstance(status_val, str) and status_val:
            return status_val
        filename = normalized_result.get("filename")
        serial = normalized_result.get("serial_number")
        if isinstance(filename, str) and filename:
            if isinstance(serial, str) and serial:
                return f"Firmware updated for {serial} with {filename}"
            return f"Firmware updated with {filename}"
        return None
