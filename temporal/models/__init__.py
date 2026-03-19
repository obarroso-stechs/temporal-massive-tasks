from .firmware import (
    FirmwareDownloadInput,
    FirmwareUpdateBatchInput,
    FirmwareUpdateResult,
    UpdateFirmware,
)
from .parameter_update import (
    ParameterUpdateBatchInput,
    ParameterUpdateResult,
    UpdateParameter,
)

__all__ = [
    "UpdateFirmware",
    "FirmwareUpdateBatchInput",
    "FirmwareUpdateResult",
    "FirmwareDownloadInput",
    "UpdateParameter",
    "ParameterUpdateBatchInput",
    "ParameterUpdateResult",
]
