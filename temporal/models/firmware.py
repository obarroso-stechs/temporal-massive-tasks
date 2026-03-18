from dataclasses import dataclass, field


@dataclass
class UpdateFirmware:
    """Input unitario: un equipo al cual actualizar firmware."""

    filename: str
    serialNumber: str

    def __post_init__(self) -> None:
        missing = [
            name
            for name, value in (
                ("filename", self.filename),
                ("serialNumber", self.serialNumber),
            )
            if not value or not value.strip()
        ]
        if missing:
            raise ValueError(
                f"Los siguientes campos no pueden estar vacíos: {', '.join(missing)}"
            )


@dataclass
class FirmwareUpdateBatchInput:
    """Input del workflow padre.

    ``processed_count`` permite al continue-as-new acumular el progreso
    a través de múltiples ejecuciones encadenadas.
    ``device_statuses`` lleva el estado de cada equipo entre continue-as-new.
    """

    items: list[UpdateFirmware]
    processed_count: int = 0
    device_statuses: dict = field(default_factory=dict)


@dataclass
class FirmwareUpdateResult:
    """Resultado de un firmware update individual."""

    serial_number: str
    filename: str
    status: str


# ── Activity inputs ──────────────────────────────────────────────


@dataclass
class FirmwareDownloadInput:
    """Input para la activity que dispara la descarga de firmware."""

    serial_number: str
    filename: str
    file_type: str = field(default="1 Firmware Upgrade Image")
