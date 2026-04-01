from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from temporalio.client import Client

from api.dependencies.report_dependency import get_report_service
from api.dependencies.temporal import get_temporal_client
from api.schemas.reports import ReportDetailResponse, ReportSummaryResponse
from db.models.report import ReportFormatEnum
from db.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])

# Estados del workflow Temporal que indican finalización anormal:
# el workflow no llamó a mark_task_completed, por lo que pueden quedar
# dispositivos en estado no-terminal en la BD.
_FORCE_STATES = {"TERMINATED", "FAILED", "CANCELED", "TIMED_OUT"}


@router.post("/generate", response_model=ReportSummaryResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    task_id: int = Query(..., description="ID de la tarea"),
    report_format: ReportFormatEnum = Query(..., description="Formato del reporte"),
    force: bool = Query(False, description="Si True, marca dispositivos no-terminales como FAILED y genera el reporte igualmente"),
    service: ReportService = Depends(get_report_service),
    temporal_client: Client = Depends(get_temporal_client),
) -> ReportSummaryResponse:
    task = await service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró tarea con id='{task_id}'.",
        )
    workflow_id = task.workflow_id

    # Si el workflow terminó de forma anormal (TERMINATED, FAILED, CANCELED,
    # TIMED_OUT), las actividades de cierre no corrieron y puede haber
    # dispositivos en estado no-terminal en la BD. Forzamos automáticamente.
    effective_force = force
    if not effective_force:
        try:
            handle = temporal_client.get_workflow_handle(workflow_id)
            description = await handle.describe()
            wf_status = description.status.name if description.status else ""
            if wf_status in _FORCE_STATES:
                effective_force = True
        except Exception:
            pass  # Si no se puede consultar Temporal, se respeta el parámetro original

    report = await service.generate_for_task(task_id, report_format, force=effective_force, temporal_client=temporal_client)
    return ReportSummaryResponse(
        id=report.id,
        task_id=report.task_id,
        workflow_id=task.workflow_id,
        task_name=task.task_name,
        task_type=task.task_type,
        report_format=report.report_format,
        has_file=bool(report.report_path),
        created_at=report.created_at,
    )


@router.get("", response_model=list[ReportSummaryResponse])
async def list_reports(
    service: ReportService = Depends(get_report_service),
) -> list[ReportSummaryResponse]:
    return await service.list_all()


@router.get("/{report_id}", response_model=ReportDetailResponse)
async def get_report(
    report_id: int,
    service: ReportService = Depends(get_report_service),
) -> ReportDetailResponse:
    detail = await service.get_detail(report_id)
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reporte {report_id} no encontrado.")
    return detail


@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    service: ReportService = Depends(get_report_service),
) -> FileResponse:
    report = await service.get_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reporte {report_id} no encontrado.")
    try:
        file_path, media_type = await service.get_report_file(report_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return FileResponse(path=str(file_path), media_type=media_type, filename=file_path.name)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    service: ReportService = Depends(get_report_service),
):
    try:
        await service.delete(report_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
