from dataclasses import dataclass, field


@dataclass
class GetParameterValuesInput:
    """Input unitario: un equipo del cual leer parametros."""

    serialNumber: str
    paths: list[str]

    def __post_init__(self) -> None:
        if not self.serialNumber or not self.serialNumber.strip():
            raise ValueError("serialNumber no puede estar vacio")
        if not self.paths:
            raise ValueError("paths no puede estar vacio")


@dataclass
class GetParameterValuesBatchInput:
    """Input del workflow padre.

    ``processed_count`` permite al continue-as-new acumular el progreso
    a traves de multiples ejecuciones encadenadas.
    """

    items: list[GetParameterValuesInput]
    processed_count: int = 0
    device_statuses: dict[str, str] = field(default_factory=dict)


@dataclass
class GetParameterValuesResult:
    """Resultado de una lectura de parametros individual."""

    serial_number: str
    status: str
    message: str = ""
