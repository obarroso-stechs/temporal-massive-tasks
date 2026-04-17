from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi_client_async import AsyncNbiClient, NbiConfig
from temporal.models import GetParameterValuesInput


@activity.defn
async def get_parameter_values(input: GetParameterValuesInput) -> str:
    async with AsyncNbiClient(NbiConfig()) as client:
        response = await client.devices.get_parameter(
            serial_number=input.serialNumber,
            params_list=input.paths,
        )

    items = response.get("items") or []
    if not items:
        raise ApplicationError(
            f"No se encontraron parametros para el device {input.serialNumber} "
            f"con los paths solicitados: {input.paths}",
            non_retryable=True,
        )

    lines = [f"{item['name']} = {item['value']}" for item in items]
    return "\n".join(lines)
