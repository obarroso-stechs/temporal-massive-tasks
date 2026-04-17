from __future__ import annotations

from abc import ABC, abstractmethod

from reports.models import ReportData


class BaseReportGenerator(ABC):
    """Contract that all report generators must fulfil."""

    @abstractmethod
    def generate(self, data: ReportData) -> bytes:
        """Return the report as raw bytes ready to write to disk or stream."""
        ...
