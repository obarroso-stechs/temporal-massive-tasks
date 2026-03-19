from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.parameter_update_activities import (
        set_parameter_value,
    )
    from temporal.activities.common_activities import (
        verify_device_exists,
    )
    from temporal.models import ParameterUpdateResult, UpdateParameter


@workflow.defn
class ParameterUpdateChildWorkflow:
    """Workflow hijo: actualiza parametros en un solo dispositivo.

    Paso 1 -> verify_device_exists  (valida que el serialNumber existe en el ACS)
    Paso 2 -> set_parameter_value   (busca parametros actuales y setea los nuevos valores)
    """

    @workflow.run
    async def run(self, input: UpdateParameter) -> ParameterUpdateResult:
        serial_number = await workflow.execute_activity(
            verify_device_exists,
            input.serialNumber,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        result = await workflow.execute_activity(
            set_parameter_value,
            input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        return ParameterUpdateResult(
            serial_number=serial_number,
            status="COMPLETED",
            message=result,
        )
