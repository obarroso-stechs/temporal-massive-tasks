from dataclasses import dataclass, field


ParameterValue = str | bool | int | float


@dataclass
class UpdateParameterSet:
    """Input unitario: un equipo al cual setear parametros."""

    serialNumber: str
    parameters: dict[str, ParameterValue]

    def __post_init__(self) -> None:
        if not self.serialNumber or not self.serialNumber.strip():
            raise ValueError("serialNumber no puede estar vacio")
        if not self.parameters:
            raise ValueError("parameters no puede estar vacio")


@dataclass
class ParameterSetBatchInput:
    """Input del workflow padre.

    ``processed_count`` permite al continue-as-new acumular el progreso
    a traves de multiples ejecuciones encadenadas.
    """

    items: list[UpdateParameterSet]
    processed_count: int = 0
    device_statuses: dict[str, str] = field(default_factory=dict)


@dataclass
class ParameterSetResult:
    """Resultado de un parameter set individual."""

    serial_number: str
    status: str
    message: str = ""
