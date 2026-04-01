from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.parameter_set_activities import (
        set_parameter_value_parameter_set,
    )
    from temporal.activities.common_activities import (
        verify_device_exists,
    )
    from temporal.models import ParameterSetResult, UpdateParameterSet


@workflow.defn
class ParameterSetChildWorkflow:
    """Workflow hijo: setea parametros en un solo dispositivo.

    Paso 1 -> verify_device_exists (valida que el serialNumber existe en el ACS)
    Paso 2 -> set_parameter_value_parameter_set (setea los parametros enviados)
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
    async def run(self, input: UpdateParameterSet) -> ParameterSetResult:
        serial_number = await workflow.execute_activity(
            verify_device_exists,
            input.serialNumber,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        # Pause point between activities
        await workflow.wait_condition(lambda: not self._paused)

        result = await workflow.execute_activity(
            set_parameter_value_parameter_set,
            input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(maximum_attempts=5),
        )

        return ParameterSetResult(
            serial_number=serial_number,
            status="COMPLETED",
            message=result,
        )
