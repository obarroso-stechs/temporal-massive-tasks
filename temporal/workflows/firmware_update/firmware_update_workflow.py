import asyncio
from datetime import timedelta
from typing import List, Union

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from pathlib import Path # noqa: F401
    from configurations.temporal import TEMPORAL_TASK_QUEUE
    from temporal.models import (
        FirmwareUpdateBatchInput,
        FirmwareUpdateResult,
        UpdateFirmware,
    )
    from temporal.workflows.firmware_update.firmware_update_child_workflow import FirmwareUpdateChildWorkflow
    from temporal.activities.reporting_activities import (
        mark_task_started,
        mark_task_completed,
        mark_task_canceled,
        upsert_device_status,
    )

# Cuántos child workflows lanzar en paralelo por batch.
# Cada child genera ~5 eventos en el padre (init, started, completed).
# Con BATCH_SIZE=50 y continue-as-new, nos mantenemos lejos del límite de 50K eventos.
BATCH_SIZE = 50


def _sanitize_error_detail(exc: BaseException) -> str:
    """Extrae el mensaje más específico de una cadena de excepciones de Temporal."""
    cause = exc
    while cause.__cause__ is not None:
        cause = cause.__cause__
    return str(cause)


@workflow.defn
class FirmwareUpdateBatchWorkflow:
    """Workflow padre: procesa miles de firmware updates en batches.

    Recibe una lista de UpdateFirmware, la particiona en batches de
    BATCH_SIZE, lanza cada batch en paralelo con asyncio.gather, y
    usa continue-as-new cuando Temporal lo sugiere para mantener
    el Event History acotado.

    Expone queries para consultar el progreso y el estado de cada equipo.
    """

    def __init__(self) -> None:
        self._total: int = 0
        self._processed: int = 0
        self._failed: int = 0
        self._device_statuses: dict[str, str] = {}
        self._paused: bool = False

    @workflow.signal
    def pause_batch(self) -> None:
        self._paused = True

    @workflow.signal
    def resume_batch(self) -> None:
        self._paused = False

    @workflow.query
    def get_progress(self) -> dict:
        return {
            "total": self._total,
            "processed": self._processed,
            "pending": self._total - self._processed,
            "failed": self._failed,
            "is_paused": self._paused,
        }

    @workflow.query
    def get_device_statuses(self) -> dict:
        return dict(self._device_statuses)

    @workflow.run
    async def run(
        self, input: FirmwareUpdateBatchInput
    ) -> List[Union[FirmwareUpdateResult, str]]:
        # Restaurar estados de continue-as-new previo
        self._device_statuses = dict(input.device_statuses)

        # Marcar items pendientes como PENDING
        for item in input.items:
            if item.serialNumber not in self._device_statuses:
                self._device_statuses[item.serialNumber] = "PENDING"

        self._total = len(self._device_statuses)
        self._processed = input.processed_count
        self._failed = sum(
            1 for s in self._device_statuses.values() if s == "FAILED"
        )

        # Mark started only on first execution (not after continue-as-new)
        if input.processed_count == 0:
            await workflow.execute_activity(
                mark_task_started,
                workflow.info().workflow_id,
                start_to_close_timeout=timedelta(seconds=10),
            )

        results: List[Union[FirmwareUpdateResult, str]] = []
        remaining = list(input.items)

        while remaining:
            # Pause point between batches
            if self._paused:
                await workflow.wait_condition(lambda: not self._paused)

            batch = remaining[:BATCH_SIZE]
            remaining = remaining[BATCH_SIZE:]

            # Marcar equipos del batch como RUNNING
            for item in batch:
                self._device_statuses[item.serialNumber] = "RUNNING"

            batch_results = await self._execute_batch(batch)
            results.extend(batch_results)

            # Checkpoint: si Temporal sugiere continue-as-new, reiniciar
            # con los items que quedan y el progreso acumulado.
            if remaining and workflow.info().is_continue_as_new_suggested():
                workflow.logger.info(
                    f"Continue-as-new: {self._processed} procesados, "
                    f"{len(remaining)} pendientes"
                )
                workflow.continue_as_new(
                    FirmwareUpdateBatchInput(
                        items=remaining,
                        processed_count=self._processed,
                        device_statuses=self._device_statuses,
                    )
                )

        await workflow.execute_activity(
            mark_task_completed,
            workflow.info().workflow_id,
            start_to_close_timeout=timedelta(seconds=10),
        )
        workflow.logger.info(
            f"Batch completo: {self._processed} equipos procesados"
        )
        return results

    async def _execute_batch(
        self,
        batch: List[UpdateFirmware],
    ) -> List[Union[FirmwareUpdateResult, str]]:
        """Lanza N child workflows en paralelo y actualiza estado por completion."""
        parent_id = workflow.info().workflow_id

        async def run_one(
            idx: int,
            item: UpdateFirmware,
        ) -> tuple[int, Union[FirmwareUpdateResult, BaseException]]:
            try:
                result = await workflow.execute_child_workflow(
                    FirmwareUpdateChildWorkflow.run,
                    item,
                    id=f"{parent_id}-{item.serialNumber}",
                    task_queue=TEMPORAL_TASK_QUEUE,
                    retry_policy=RetryPolicy(maximum_attempts=5),
                )
                return idx, result
            except BaseException as exc:
                return idx, exc

        tasks = [
            asyncio.create_task(run_one(idx, item))
            for idx, item in enumerate(batch)
        ]

        raw_results: list[Union[FirmwareUpdateResult, str, None]] = [None] * len(batch)

        for done in asyncio.as_completed(tasks):
            idx, completed_result = await done
            item = batch[idx]

            if isinstance(completed_result, BaseException):
                workflow.logger.warning(
                    f"Child workflow falló para {item.serialNumber}: {completed_result}"
                )
                raw_results[idx] = f"ERROR [{item.serialNumber}]: {completed_result}"
                self._device_statuses[item.serialNumber] = "FAILED"
                self._failed += 1
                await workflow.execute_activity(
                    upsert_device_status,
                    args=[workflow.info().workflow_id, item.serialNumber, "FAILED", _sanitize_error_detail(completed_result)],
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=RetryPolicy(maximum_attempts=5),
                )
            else:
                raw_results[idx] = completed_result
                self._device_statuses[item.serialNumber] = "COMPLETED"
                await workflow.execute_activity(
                    upsert_device_status,
                    args=[workflow.info().workflow_id, item.serialNumber, "COMPLETED", f"Firmware actualizado: {completed_result.filename}"],
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=RetryPolicy(maximum_attempts=5),
                )

            self._processed += 1

        results: List[Union[FirmwareUpdateResult, str]] = []
        for result in raw_results:
            if result is not None:
                results.append(result)

        return results
