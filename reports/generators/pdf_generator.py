from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from reports.base_generator import BaseReportGenerator
from reports.models import ReportData

_HEADER_COLUMNS = [
    "modelo", "marca", "status task", "detalle",
    "scheduled_at", "started_at", "end_at",
]

_DATE_FMT = "%Y-%m-%d %H:%M"


def _fmt(value: datetime | None) -> str:
    return value.strftime(_DATE_FMT) if value else "-"


class PdfReportGenerator(BaseReportGenerator):

    def generate(self, data: ReportData) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=6,
        )
        meta_style = styles["Normal"]

        story = []

        # ── Title ──
        story.append(Paragraph("MASSIVE TASK PROGRAM", title_style))
        story.append(Spacer(1, 0.3 * cm))

        # ── Metadata ──
        meta_lines = [
            f"<b>nombre tarea:</b> {data.task_name}",
            f"<b>total devices:</b> {data.total_devices}",
            f"<b>processed devices:</b> {data.processed_devices}",
            f"<b>failed devices:</b> {data.failed_devices}",
            f"<b>group name:</b> {data.group_name}",
        ]
        for line in meta_lines:
            story.append(Paragraph(line, meta_style))
        story.append(Spacer(1, 0.5 * cm))

        # ── Table ──
        # Header row: empty cell for serial_number label column + column headers
        header_row = [""] + _HEADER_COLUMNS
        table_data = [header_row]

        for row in data.rows:
            table_data.append([
                row.serial_number,
                row.model or "-",
                row.manufacturer or "-",
                row.task_status,
                row.detail or "-",
                _fmt(row.scheduled_at),
                _fmt(row.started_at),
                _fmt(row.end_at),
            ])

        col_widths = [4 * cm, 3 * cm, 3 * cm, 3 * cm, 5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ECF0F1")]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BDC3C7")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))

        story.append(table)
        doc.build(story)
        return buffer.getvalue()
