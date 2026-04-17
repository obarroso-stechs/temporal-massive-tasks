from __future__ import annotations

import csv
import io
from datetime import datetime

from reports.base_generator import BaseReportGenerator
from reports.models import ReportData

_DATE_FMT = "%Y-%m-%d %H:%M"


def _fmt(value: datetime | None) -> str:
    return value.strftime(_DATE_FMT) if value else ""


class CsvReportGenerator(BaseReportGenerator):

    def generate(self, data: ReportData) -> bytes:
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        # ── Metadata block ──
        writer.writerow(["MASSIVE TASK PROGRAM"])
        writer.writerow(["nombre tarea:", data.task_name])
        writer.writerow(["total devices:", data.total_devices])
        writer.writerow(["processed devices:", data.processed_devices])
        writer.writerow(["failed devices:", data.failed_devices])
        writer.writerow(["group name:", data.group_name])
        writer.writerow([])

        # ── Table ──
        writer.writerow([
            "serial number", "modelo", "marca", "status task",
            "detalle", "scheduled_at", "started_at", "end_at",
        ])
        for row in data.rows:
            writer.writerow([
                row.serial_number,
                row.model or "",
                row.manufacturer or "",
                row.task_status,
                row.detail or "",
                _fmt(row.scheduled_at),
                _fmt(row.started_at),
                _fmt(row.end_at),
            ])

        return buffer.getvalue().encode("utf-8")
