from __future__ import annotations

from db.models.report import ReportFormatEnum
from reports.base_generator import BaseReportGenerator
from reports.generators.csv_generator import CsvReportGenerator
from reports.generators.excel_generator import ExcelReportGenerator
from reports.generators.pdf_generator import PdfReportGenerator
from reports.generators.word_generator import WordReportGenerator

_REGISTRY: dict[ReportFormatEnum, type[BaseReportGenerator]] = {
    ReportFormatEnum.PDF: PdfReportGenerator,
    ReportFormatEnum.WORD: WordReportGenerator,
    ReportFormatEnum.EXCEL: ExcelReportGenerator,
    ReportFormatEnum.CSV: CsvReportGenerator,
}


class ReportGeneratorFactory:

    @staticmethod
    def create(report_format: ReportFormatEnum) -> BaseReportGenerator:
        generator_cls = _REGISTRY.get(report_format)
        if generator_cls is None:
            raise ValueError(f"Unsupported report format: {report_format}")
        return generator_cls()
