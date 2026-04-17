"""Utilidades para parsear el Event History de Temporal a dicts serializables."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from temporalio.api.enums.v1 import EventType
from temporalio.client import WorkflowHistory


def enrich_events_with_pending_activities(
    events: list[dict[str, Any]],
    raw_description: Any,
) -> list[dict[str, Any]]:
    """Enriquece eventos ACTIVITY_TASK_SCHEDULED con info de pending activities.

    Cuando una activity esta retryando, el last_failure vive en
    pending_activities del describe(), no en el event history.
    Esta funcion inyecta esa info como `activity_result` dentro del
    details del evento ACTIVITY_TASK_SCHEDULED correspondiente.
    """
    # Construir mapa activity_id -> pending info
    pending_map: dict[str, Any] = {}
    for info in raw_description.pending_activities:
        activity_result: dict[str, Any] | None = None
        if info.HasField("last_failure"):
            activity_result = {
                "status": "RETRYING",
                "attempt": info.attempt,
                "maximum_attempts": info.maximum_attempts,
                "state": _format_pending_state(info.state),
                "next_attempt_schedule_time": (
                    _format_timestamp(info.next_attempt_schedule_time)
                    if info.HasField("next_attempt_schedule_time")
                    else None
                ),
                "failure": _build_failure(info.last_failure),
            }
        pending_map[info.activity_id] = activity_result

    # Enriquecer eventos ACTIVITY_TASK_SCHEDULED
    for event in events:
        if event["event_type"] == "ACTIVITY_TASK_SCHEDULED":
            activity_id = event["details"].get("activity_id")
            if activity_id and activity_id in pending_map:
                event["details"]["activity_result"] = pending_map[activity_id]

    # Tambien enriquecer ACTIVITY_TASK_COMPLETED con su resultado
    # (ya esta en details["result"] via _extract_event_details)

    return events


def _format_pending_state(state: int) -> str:
    """PENDING_ACTIVITY_STATE_SCHEDULED -> SCHEDULED."""
    from temporalio.api.enums.v1 import PendingActivityState
    try:
        name = PendingActivityState.Name(state)
        return name.removeprefix("PENDING_ACTIVITY_STATE_")
    except ValueError:
        return f"UNKNOWN_{state}"


_INTERNAL_EVENT_TYPES = {
    EventType.EVENT_TYPE_WORKFLOW_TASK_SCHEDULED,
    EventType.EVENT_TYPE_WORKFLOW_TASK_STARTED,
    EventType.EVENT_TYPE_WORKFLOW_TASK_COMPLETED,
    EventType.EVENT_TYPE_WORKFLOW_TASK_FAILED,
    EventType.EVENT_TYPE_WORKFLOW_TASK_TIMED_OUT,
}

# Mapeo de nombres técnicos de activities a etiquetas amigables para el usuario.
_ACTIVITY_FRIENDLY_NAMES: dict[str, str] = {
    "verify_device_exists": "Verificar dispositivo",
    "trigger_firmware_download": "Descargar firmware",
    "mark_task_started": "Iniciar tarea",
    "mark_task_completed": "Completar tarea",
    "mark_task_canceled": "Cancelar tarea",
    "upsert_device_status": "Actualizar estado",
    "set_device_parameter": "Aplicar parámetro",
    "get_device_parameters": "Obtener parámetros",
}


def parse_workflow_events(history: WorkflowHistory) -> list[dict[str, Any]]:
    """Convierte todos los eventos de un WorkflowHistory a una lista plana.

    Filtra eventos internos de Temporal (WORKFLOW_TASK_*) que no son
    relevantes para el usuario final.
    Usado para Caso 1: event history completo de un child workflow.
    """
    return [
        _event_to_dict(event) for event in history.events
        if event.event_type not in _INTERNAL_EVENT_TYPES
    ]


def group_child_events_by_device(
    history: WorkflowHistory,
    parent_workflow_id: str,
) -> dict[str, list[dict[str, Any]]]:
    """Agrupa eventos child-related del parent history por serial_number.

    Usado para Caso 2 y 3: events del parent agrupados por device.

    Filtra solo eventos relacionados a child workflows, extrae el
    serial_number del child_workflow_id (patron: {parent_id}-{serial}),
    y agrupa los eventos bajo cada serial_number.
    """
    child_event_types = {
        EventType.EVENT_TYPE_START_CHILD_WORKFLOW_EXECUTION_INITIATED,
        EventType.EVENT_TYPE_START_CHILD_WORKFLOW_EXECUTION_FAILED,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_STARTED,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_COMPLETED,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_FAILED,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_CANCELED,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TIMED_OUT,
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TERMINATED,
    }

    prefix = f"{parent_workflow_id}-"
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for event in history.events:
        if event.event_type not in child_event_types:
            continue

        child_wf_id = _extract_child_workflow_id(event)
        if not child_wf_id:
            continue

        # Derivar serial_number del child workflow id
        if child_wf_id.startswith(prefix):
            serial_number = child_wf_id[len(prefix):]
        else:
            serial_number = child_wf_id

        grouped[serial_number].append(_event_to_dict(event))

    return dict(grouped)


# ── Helpers internos ─────────────────────────────────────────────


def _event_to_dict(event: Any) -> dict[str, Any]:
    """Convierte un HistoryEvent protobuf a un dict serializable."""
    return {
        "event_id": event.event_id,
        "timestamp": _format_timestamp(event.event_time),
        "event_type": _format_event_type(event.event_type),
        "details": _extract_event_details(event),
    }


def _format_event_type(event_type: int) -> str:
    """EVENT_TYPE_WORKFLOW_EXECUTION_STARTED -> WORKFLOW_EXECUTION_STARTED."""
    try:
        name = EventType.Name(event_type)
        return name.removeprefix("EVENT_TYPE_")
    except ValueError:
        return f"UNKNOWN_{event_type}"


def _format_timestamp(ts: Any) -> str | None:
    """Convierte un protobuf Timestamp a ISO 8601 string."""
    if ts is None:
        return None
    try:
        dt = ts.ToDatetime(tzinfo=timezone.utc)
        return dt.isoformat()
    except Exception:
        try:
            # Fallback: construir desde seconds/nanos
            dt = datetime.fromtimestamp(
                ts.seconds + ts.nanos / 1e9, tz=timezone.utc
            )
            return dt.isoformat()
        except Exception:
            return None


def _extract_child_workflow_id(event: Any) -> str | None:
    """Extrae el child workflow ID de un evento child-related."""
    et = event.event_type

    if et == EventType.EVENT_TYPE_START_CHILD_WORKFLOW_EXECUTION_INITIATED:
        attrs = event.start_child_workflow_execution_initiated_event_attributes
        return attrs.workflow_id if attrs else None

    if et == EventType.EVENT_TYPE_START_CHILD_WORKFLOW_EXECUTION_FAILED:
        attrs = event.start_child_workflow_execution_failed_event_attributes
        return attrs.workflow_id if attrs else None

    # Todos los demas child events tienen workflow_execution.workflow_id
    attrs_map = {
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_STARTED: "child_workflow_execution_started_event_attributes",
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_COMPLETED: "child_workflow_execution_completed_event_attributes",
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_FAILED: "child_workflow_execution_failed_event_attributes",
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_CANCELED: "child_workflow_execution_canceled_event_attributes",
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TIMED_OUT: "child_workflow_execution_timed_out_event_attributes",
        EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TERMINATED: "child_workflow_execution_terminated_event_attributes",
    }

    attr_name = attrs_map.get(et)
    if attr_name:
        attrs = getattr(event, attr_name, None)
        if attrs and attrs.workflow_execution:
            return attrs.workflow_execution.workflow_id

    return None


def _extract_event_details(event: Any) -> dict[str, Any]:
    """Extrae los detalles relevantes de un evento segun su tipo."""
    et = event.event_type
    details: dict[str, Any] = {}

    # ── Workflow lifecycle ────────────────────────────────────
    if et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_STARTED:
        pass  # Sin detalles técnicos expuestos al usuario

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_COMPLETED:
        pass  # Sin detalles — el resultado ya se muestra en el último ACTIVITY_TASK_COMPLETED

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_FAILED:
        attrs = event.workflow_execution_failed_event_attributes
        if attrs:
            details.update(_failure_to_dict(attrs.failure))

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_TIMED_OUT:
        pass  # Sin detalles técnicos

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_SIGNALED:
        attrs = event.workflow_execution_signaled_event_attributes
        if attrs:
            details["signal_name"] = attrs.signal_name or None

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_CANCELED:
        pass  # No details relevantes

    elif et == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_CONTINUED_AS_NEW:
        pass  # Sin detalles técnicos expuestos

    # ── Activity tasks ────────────────────────────────────────
    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED:
        attrs = event.activity_task_scheduled_event_attributes
        if attrs and attrs.activity_type:
            raw_name = attrs.activity_type.name or ""
            details["activity"] = _ACTIVITY_FRIENDLY_NAMES.get(raw_name, raw_name)

    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_STARTED:
        attrs = event.activity_task_started_event_attributes
        if attrs and attrs.attempt and attrs.attempt > 1:
            details["intento"] = attrs.attempt

    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED:
        attrs = event.activity_task_completed_event_attributes
        if attrs and attrs.result and attrs.result.payloads:
            details["result"] = _payloads_to_str(attrs.result)

    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED:
        attrs = event.activity_task_failed_event_attributes
        if attrs:
            details.update(_failure_to_dict(attrs.failure))

    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_TIMED_OUT:
        attrs = event.activity_task_timed_out_event_attributes
        if attrs:
            details.update(_failure_to_dict(attrs.failure))

    elif et == EventType.EVENT_TYPE_ACTIVITY_TASK_CANCELED:
        pass  # No details relevantes extra

    # ── Child workflow events ─────────────────────────────────
    elif et == EventType.EVENT_TYPE_START_CHILD_WORKFLOW_EXECUTION_INITIATED:
        pass  # Sin detalles técnicos

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_STARTED:
        pass  # Sin detalles técnicos

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_COMPLETED:
        attrs = event.child_workflow_execution_completed_event_attributes
        if attrs and attrs.result and attrs.result.payloads:
            details["result"] = _payloads_to_str(attrs.result)

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_FAILED:
        attrs = event.child_workflow_execution_failed_event_attributes
        if attrs:
            details.update(_failure_to_dict(attrs.failure))

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_CANCELED:
        pass  # Sin detalles técnicos

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TIMED_OUT:
        pass  # Sin detalles técnicos

    elif et == EventType.EVENT_TYPE_CHILD_WORKFLOW_EXECUTION_TERMINATED:
        pass  # Sin detalles técnicos

    return details


def _failure_to_dict(failure: Any) -> dict[str, Any]:
    """Extrae informacion de un Failure protobuf (top-level para details del evento)."""
    if not failure:
        return {}
    failure_detail = _build_failure(failure)
    return {"failure": failure_detail} if failure_detail else {}


def _build_failure(failure: Any) -> dict[str, Any] | None:
    """Construye un dict recursivo completo de un Failure protobuf.

    Replica la estructura que muestra la UI de Temporal:
      message, stackTrace, cause (recursivo), applicationFailureInfo, serverFailureInfo, etc.
    """
    if not failure:
        return None

    result: dict[str, Any] = {}

    if failure.message:
        result["message"] = failure.message
    if failure.source:
        result["source"] = failure.source
    # applicationFailureInfo
    if hasattr(failure, "HasField") and failure.HasField("application_failure_info"):
        app_info = failure.application_failure_info
        info_dict: dict[str, Any] = {}
        if app_info.type:
            info_dict["type"] = app_info.type
        if app_info.non_retryable:
            info_dict["nonRetryable"] = True
        if info_dict:
            result["applicationFailureInfo"] = info_dict

    # serverFailureInfo
    if hasattr(failure, "HasField") and failure.HasField("server_failure_info"):
        srv_info = failure.server_failure_info
        srv_dict: dict[str, Any] = {}
        if srv_info.non_retryable:
            srv_dict["nonRetryable"] = True
        result["serverFailureInfo"] = srv_dict

    # timeoutFailureInfo
    if hasattr(failure, "HasField") and failure.HasField("timeout_failure_info"):
        timeout_info = failure.timeout_failure_info
        result["timeoutFailureInfo"] = {"timeoutType": str(timeout_info.timeout_type)}

    # cause (recursivo) — usar HasField porque protobuf devuelve un
    # Failure vacío (truthy) en vez de None cuando no hay cause
    if hasattr(failure, "HasField") and failure.HasField("cause"):
        cause_dict = _build_failure(failure.cause)
        if cause_dict:
            result["cause"] = cause_dict

    return result or None


def infer_paused_from_history(history: WorkflowHistory) -> bool:
    """Determina si el workflow está pausado leyendo el historial de señales.

    Recorre los eventos de señal (WORKFLOW_EXECUTION_SIGNALED) en orden
    cronológico y retorna True si la última señal de control fue pause_batch,
    False si fue resume_batch o no hay señales de control.

    Útil como fallback cuando el query get_progress no está disponible
    (e.g. workflow en start_delay, aún no procesado por el worker).
    """
    last_control_signal: str | None = None
    for event in history.events:
        if event.event_type == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_SIGNALED:
            attrs = event.workflow_execution_signaled_event_attributes
            if attrs and attrs.signal_name in ("pause_batch", "resume_batch"):
                last_control_signal = attrs.signal_name
    return last_control_signal == "pause_batch"


def _payloads_to_str(payloads: Any) -> str | None:
    """Convierte Payloads protobuf a string representativo."""
    if not payloads or not payloads.payloads:
        return None
    try:
        # Tomar el primer payload y decodificar como UTF-8
        data = payloads.payloads[0].data
        return data.decode("utf-8") if data else None
    except Exception:
        return f"<{len(payloads.payloads)} payload(s)>"
