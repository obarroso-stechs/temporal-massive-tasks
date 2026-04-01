from dataclasses import dataclass, field


@dataclass
class UpdateParameter:
    """Input unitario: un equipo al cual actualizar parametros."""

    serialNumber: str

    def __post_init__(self) -> None:
        if not self.serialNumber or not self.serialNumber.strip():
            raise ValueError("serialNumber no puede estar vacio")


@dataclass
class ParameterUpdateBatchInput:
    """Input del workflow padre.

    ``processed_count`` permite al continue-as-new acumular el progreso
    a traves de multiples ejecuciones encadenadas.
    """

    items: list[UpdateParameter]
    processed_count: int = 0
    device_statuses: dict[str, str] = field(default_factory=dict)


@dataclass
class ParameterUpdateResult:
    """Resultado de un parameter update individual."""

    serial_number: str
    status: str
    message: str = ""
