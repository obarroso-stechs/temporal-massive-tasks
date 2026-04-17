from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.get_parameter_values_activities import (
        get_parameter_values,
    )
    from temporal.activities.common_activities import (
        verify_device_exists,
    )
    from temporal.models import GetParameterValuesResult, GetParameterValuesInput


@workflow.defn
class GetParameterValuesChildWorkflow:
    """Workflow hijo: lee parametros de un solo dispositivo.

    Paso 1 -> verify_device_exists (valida que el serialNumber existe en el ACS)
    Paso 2 -> get_parameter_values (lee los valores de los paths solicitados)
    """

    def __init__(self) -> None:
        self._paused = False

    @workflow.signal
    def pause(self) -> None:
        self._paused = True

    @workflow.signal
    def resume(self) -> None:
        self._paused = False

    @workflow.run
    async def run(self, input: GetParameterValuesInput) -> GetParameterValuesResult:
        serial_number = await workflow.execute_activity(
            verify_device_exists,
            input.serialNumber,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        await workflow.wait_condition(lambda: not self._paused)

        result = await workflow.execute_activity(
            get_parameter_values,
            input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        return GetParameterValuesResult(
            serial_number=serial_number,
            status="COMPLETED",
            message=result,
        )
