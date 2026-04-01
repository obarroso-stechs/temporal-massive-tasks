from dataclasses import dataclass

from temporalio import activity
from temporalio.exceptions import ApplicationError

from nbi_client_async import AsyncNbiClient, NbiConfig
from temporal.models import UpdateParameter


@dataclass
class ParameterToSet:
    path: str
    value: str | bool
    type: str


@dataclass
class SetParametersBody:
    paramsList: list[ParameterToSet]
    connectionRequest: bool = True

possible_parameters_to_set = ["Device.WiFi.SSID", "InternetGatewayDevice.LANDevice"]


@activity.defn
async def set_parameter_value(input: UpdateParameter) -> str:
    """ 
    Recibe una lista de serial numbers. Este servira para hacer la busqueda de los parametros a setear
    Estos seran SSID y su respectivo enable
    1. Buscar los parametros via API con projection [parameterName] y filtrando por serial_number y parameterName (con los nombres de los parametros a setear)
    2. Una vez recibida la respuesta, iterar sobre cada serial number y setear el nuevo valor del parametro via API usando set_parameter_sync.
    """

    parameters = await _get_parameter_names_to_set(serial_number=input.serialNumber)
    
    print(f"Parameters to set for device {input.serialNumber}: {parameters}")
    
    configured_parameters = _reformat_parameters(parameters, serial_number=input.serialNumber)

    print(f"Reformatted parameters for device {input.serialNumber}: {configured_parameters}")

    async with AsyncNbiClient(NbiConfig()) as client:
        await client.devices.set_parameter(
            serial_number=input.serialNumber,
            body=configured_parameters,
        )
    params_summary = ", ".join(
        f"{p.path}={p.value}" for p in configured_parameters.paramsList
    )
    return f"Parámetros actualizados: {params_summary}"

def _reformat_parameters(parameters: list[dict], serial_number: str) -> SetParametersBody:
    params_list = []
    for param in parameters:
        name = param["name"]
        is_wifi = name.startswith("Device.WiFi.SSID.")
        is_wlan = "WLANConfiguration" in name

        if is_wifi and name.endswith(".SSID") or is_wlan and name.endswith(".SSID"):
            instance_index = int(name.split(".")[-2])
            params_list.append(ParameterToSet(
                path=name,
                value=f"Stechs-{serial_number[:-instance_index]}-temporal-{instance_index}",
                type="string",
            ))
        elif is_wifi and name.endswith(".Enable") or is_wlan and name.endswith(".Enable"):
            params_list.append(ParameterToSet(
                path=name,
                value=bool(param["value"]),
                type="boolean",
            ))
    return SetParametersBody(paramsList=params_list)

async def _get_parameter_names_to_set(serial_number: str) -> list[dict]:
    # En este ejemplo, vamos a setear el SSID y su enable, por lo que retornamos esos nombres de parametros.
    # En un caso real, esto podria ser mas dinamico, por ejemplo recibiendo como input una lista de parametros a setear.
    async with AsyncNbiClient(NbiConfig()) as client:
        for parameter_name in possible_parameters_to_set:
            parameters = await client.devices.get_parameter(
                serial_number=serial_number,
                params_list=parameter_name,
            )
            items = parameters.get("items") or []
            if items:
                return items

    raise ApplicationError(
        f"No se encontraron parametros para el device {serial_number} "
        f"con ninguno de los prefijos configurados: {possible_parameters_to_set}"
    )