from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configurations.reports import REPORTS_OUTPUT_DIR
from db.models.report import Report, ReportFormatEnum
from db.models.task import DeviceTaskStatusEnum, TaskDeviceStatus
from db.repositories.report_repository import ReportRepository
from db.repositories.task_repository import TaskRepository
from db.repositories.task_device_status_repository import TaskDeviceStatusRepository
from db.schemas.report import ReportResponse
from reports.factory import ReportGeneratorFactory
from reports.models import DeviceReportRow, ReportData

logger = logging.getLogger(__name__)

_NON_TERMINAL = {
    DeviceTaskStatusEnum.SCHEDULED,
    DeviceTaskStatusEnum.PENDING,
    DeviceTaskStatusEnum.RUNNING,
}

_EXT_MAP = {
    ReportFormatEnum.PDF: "pdf",
    ReportFormatEnum.WORD: "docx",
    ReportFormatEnum.EXCEL: "xlsx",
    ReportFormatEnum.CSV: "csv",
}

_MEDIA_TYPE_MAP = {
    ReportFormatEnum.PDF: "application/pdf",
    ReportFormatEnum.WORD: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ReportFormatEnum.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ReportFormatEnum.CSV: "text/csv",
}


class ReportService:

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db
        self._repo = ReportRepository()
        self._task_repo = TaskRepository()
        self._status_repo = TaskDeviceStatusRepository()

    async def create(
        self,
        task_id: int,
        generate_report: bool,
        report_format: ReportFormatEnum | None,
    ) -> Report:
        return await self._repo.create(
            task_id=task_id,
            generate_report=generate_report,
            report_format=report_format,
            db=self._db,
        )

    async def get_task_by_id(self, task_id: int):
        return await self._task_repo.get_by_id(task_id, self._db)

    async def get_report_file(self, report_id: int) -> tuple[Path, str]:
        """Retorna (file_path, media_type) del reporte generado.

        Lanza ValueError si no existe registro o el archivo aún no fue generado.
        """
        report = await self._repo.get_by_id(report_id, self._db)
        if report is None:
            raise ValueError(f"No se encontró reporte con id={report_id}.")
        if not report.report_path:
            raise ValueError(f"El reporte {report_id} aún no fue generado.")

        file_path = Path(report.report_path)
        if not file_path.exists():
            raise ValueError(f"Archivo de reporte no encontrado en disco: {file_path}")

        media_type = _MEDIA_TYPE_MAP.get(report.report_format, "application/octet-stream")
        return file_path, media_type

    async def generate_for_workflow(
        self,
        workflow_id: str,
        report_format: ReportFormatEnum,
        force: bool = False,
        temporal_client=None,
    ) -> Report:
        """Genera (o devuelve) el reporte para un workflow dado.

        - 404 si el workflow_id no existe en la BD.
        - 422 si hay dispositivos en estado no-terminal (a menos que force=True).
        - force=True + temporal_client: sincroniza el estado real de cada dispositivo
          desde Temporal antes de generar el reporte (evita marcar como FAILED
          dispositivos que en realidad completaron exitosamente).
        - force=True sin temporal_client: fallback — marca todos los no-terminales como FAILED.
        - Idempotente: si ya existe un reporte con report_path, lo devuelve sin regenerar.
        """
        from datetime import UTC, datetime as dt

        task = await self._task_repo.get_by_workflow_id(workflow_id, self._db)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró tarea para workflow_id='{workflow_id}'.",
            )

        statuses = await self._status_repo.list_by_task(task.id, self._db)

        if any(s.status == DeviceTaskStatusEnum.CANCELED for s in statuses):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se puede generar un reporte para una tarea cancelada por el usuario.",
            )

        non_terminal_statuses = [s for s in statuses if s.status in _NON_TERMINAL]
        if non_terminal_statuses:
            if not force:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El workflow aún no finalizó. Dispositivos no-terminales: {[s.serial_number for s in non_terminal_statuses]}",
                )
            if temporal_client is not None:
                await self._sync_non_terminal_from_temporal(
                    task_id=task.id,
                    workflow_id=workflow_id,
                    non_terminal_statuses=non_terminal_statuses,
                    temporal_client=temporal_client,
                )
            else:
                await self._status_repo.bulk_fail_non_terminal_async(
                    task_id=task.id,
                    detail="La tarea fue interrumpida antes de procesar este dispositivo.",
                    end_at=dt.now(UTC),
                    db=self._db,
                )
            statuses = await self._status_repo.list_by_task(task.id, self._db)

        existing = await self._repo.get_by_task_and_format(task.id, report_format, self._db)
        if existing and existing.report_path:
            return existing

        report_data = await self._build_report_data(task, statuses)
        generator = ReportGeneratorFactory.create(report_format)
        content: bytes = await asyncio.to_thread(generator.generate, report_data)

        REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ext = _EXT_MAP[report_format]
        filename = f"report_task_{task.id}_{report_format.value.lower()}.{ext}"
        file_path = REPORTS_OUTPUT_DIR / filename
        file_path.write_bytes(content)

        if existing:
            await self._repo.set_report_path(task.id, report_format, str(file_path), self._db)
        else:
            await self._repo.create(
                task_id=task.id,
                generate_report=True,
                report_format=report_format,
                db=self._db,
            )
            await self._repo.set_report_path(task.id, report_format, str(file_path), self._db)

        logger.info("Reporte generado: %s", file_path)
        return await self._repo.get_by_task_and_format(task.id, report_format, self._db)

    async def generate_for_task(
        self,
        task_id: int,
        report_format: ReportFormatEnum,
        force: bool = False,
        temporal_client=None,
    ) -> Report:
        task = await self._task_repo.get_by_id(task_id, self._db)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró tarea con id='{task_id}'.",
            )

        return await self.generate_for_workflow(
            workflow_id=task.workflow_id,
            report_format=report_format,
            force=force,
            temporal_client=temporal_client,
        )

    async def list_all(self) -> list[dict]:
        """Retorna metadata de todos los reportes generados, ordenados por fecha descendente."""
        from db.models.task import Task
        reports = await self._repo.get_all(self._db)
        result = []
        for report in reports:
            task_result = await self._db.execute(select(Task).where(Task.id == report.task_id))
            task = task_result.scalar_one_or_none()
            result.append({
                "id": report.id,
                "task_id": report.task_id,
                "workflow_id": task.workflow_id if task else "",
                "task_name": task.task_name if task else "",
                "task_type": task.task_type if task else None,
                "report_format": report.report_format,
                "has_file": bool(report.report_path),
                "created_at": report.created_at,
            })
        return result

    async def get_by_id(self, report_id: int) -> ReportResponse | None:
        return await self._repo.get_by_id(report_id, self._db)

    async def delete(self, report_id: int) -> None:
        report = await self._repo.get_by_id(report_id, self._db)
        if report is None:
            raise ValueError(f"Reporte {report_id} no encontrado.")

        report_path = Path(report.report_path) if report.report_path else None
        await self._repo.delete(report_id, self._db)

        if report_path is not None:
            try:
                report_path.unlink(missing_ok=True)
            except OSError:
                logger.warning("No se pudo eliminar archivo de reporte: %s", report_path)

    async def get_detail(self, report_id: int) -> dict | None:
        """Retorna el cuerpo completo del reporte: metadata + lista de dispositivos."""
        from db.models.task import Task
        from db.models.device import Device
        report = await self._repo.get_by_id(report_id, self._db)
        if report is None:
            return None
        task_result = await self._db.execute(select(Task).where(Task.id == report.task_id))
        task = task_result.scalar_one_or_none()
        statuses = await self._status_repo.list_by_task(report.task_id, self._db)
        devices = []
        for s in statuses:
            dev_result = await self._db.execute(select(Device).where(Device.serial_number == s.serial_number))
            device = dev_result.scalar_one_or_none()
            devices.append({
                "serial_number": s.serial_number,
                "model": device.model if device else None,
                "manufacturer": device.manufacturer if device else None,
                "status": s.status,
                "detail": s.detail,
                "started_at": s.started_at,
                "end_at": s.end_at,
            })
        return {
            "id": report.id,
            "task_id": report.task_id,
            "workflow_id": task.workflow_id if task else "",
            "task_name": task.task_name if task else "",
            "task_type": task.task_type if task else None,
            "report_format": report.report_format,
            "has_file": bool(report.report_path),
            "created_at": report.created_at,
            "devices": devices,
        }

    async def _sync_non_terminal_from_temporal(
        self,
        task_id: int,
        workflow_id: str,
        non_terminal_statuses: list,
        temporal_client,
    ) -> None:
        """Consulta Temporal para obtener el estado real de cada dispositivo no-terminal.

        En lugar de marcar todos como FAILED, verifica el child workflow de cada
        dispositivo y actualiza la BD con el estado real: COMPLETED si terminó bien,
        FAILED con el mensaje de error real si falló, etc.
        """
        from datetime import UTC, datetime as dt

        from sqlalchemy import update as sa_update

        for s in non_terminal_statuses:
            sn = s.serial_number
            child_id = f"{workflow_id}-{sn}"

            new_status = DeviceTaskStatusEnum.FAILED
            detail = "La tarea fue interrumpida antes de procesar este dispositivo."

            try:
                handle = temporal_client.get_workflow_handle(child_id)
                desc = await handle.describe()
                wf_status = desc.status.name if desc.status else "UNKNOWN"

                if wf_status == "COMPLETED":
                    new_status = DeviceTaskStatusEnum.COMPLETED
                    try:
                        result = await handle.result()
                        if isinstance(result, dict):
                            detail = result.get("message") or result.get("status") or "Completado"
                        else:
                            detail = (
                                getattr(result, "message", None)
                                or getattr(result, "status", None)
                                or "Completado"
                            )
                    except Exception:
                        detail = "Completado"

                elif wf_status == "FAILED":
                    new_status = DeviceTaskStatusEnum.FAILED
                    try:
                        await handle.result()  # lanza WorkflowFailureError
                    except BaseException as exc:
                        cause = exc
                        while cause.__cause__ is not None:
                            cause = cause.__cause__
                        detail = str(cause)

                elif wf_status in ("TERMINATED", "CANCELED"):
                    new_status = DeviceTaskStatusEnum.FAILED
                    detail = f"El workflow del dispositivo fue {wf_status.lower()}."

                elif wf_status == "TIMED_OUT":
                    new_status = DeviceTaskStatusEnum.FAILED
                    detail = "El workflow del dispositivo expiró (timeout)."

            except Exception:
                pass  # Child no encontrado o error de red → FAILED con mensaje por defecto

            await self._db.execute(
                sa_update(TaskDeviceStatus)
                .where(
                    TaskDeviceStatus.task_id == task_id,
                    TaskDeviceStatus.serial_number == sn,
                )
                .values(status=new_status, detail=detail, end_at=dt.now(UTC))
            )

        await self._db.commit()

    async def _build_report_data(self, task, statuses) -> ReportData:
        from db.models.device import Device
        from db.models.device_group import DeviceGroup

        group_name = "Grupo no asignado"
        if task.group_id:
            result = await self._db.execute(
                select(DeviceGroup).where(DeviceGroup.id == task.group_id)
            )
            group = result.scalar_one_or_none()
            if group:
                group_name = group.name

        total = len(statuses)
        processed = sum(1 for s in statuses if s.status not in _NON_TERMINAL)
        failed = sum(1 for s in statuses if s.status == DeviceTaskStatusEnum.FAILED)

        rows: list[DeviceReportRow] = []
        for s in statuses:
            result = await self._db.execute(
                select(Device).where(Device.serial_number == s.serial_number)
            )
            device = result.scalar_one_or_none()
            rows.append(DeviceReportRow(
                serial_number=s.serial_number,
                model=device.model if device else None,
                manufacturer=device.manufacturer if device else None,
                task_status=s.status.value,
                detail=s.detail,
                scheduled_at=task.scheduled_at,
                started_at=s.started_at,
                end_at=s.end_at,
            ))

        return ReportData(
            task_name=task.task_name,
            group_name=group_name,
            total_devices=total,
            processed_devices=processed,
            failed_devices=failed,
            rows=rows,
        )
