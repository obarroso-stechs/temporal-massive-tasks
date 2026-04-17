from dataclasses import dataclass

from temporalio import activity

from nbi_client_async import AsyncNbiClient, NbiConfig
from temporal.models import UpdateParameterSet


@dataclass
class ParameterToSet:
    path: str
    value: str | bool | int | float
    type: str


@dataclass
class SetParametersBody:
    paramsList: list[ParameterToSet]
    connectionRequest: bool = True


def _infer_parameter_type(value: str | bool | int | float) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "double"
    return "string"


@activity.defn
async def set_parameter_value_parameter_set(input: UpdateParameterSet) -> str:
    """Setea en ACS los parametros recibidos en formato {path: value}."""
    params = [
        ParameterToSet(
            path=path,
            value=value,
            type=_infer_parameter_type(value),
        )
        for path, value in input.parameters.items()
    ]

    body = SetParametersBody(paramsList=params)

    async with AsyncNbiClient(NbiConfig()) as client:
        await client.devices.set_parameter(
            serial_number=input.serialNumber,
            body=body,
        )

    params_summary = ", ".join(f"{path}={value}" for path, value in input.parameters.items())
    return f"Parametros seteados: {params_summary}"
