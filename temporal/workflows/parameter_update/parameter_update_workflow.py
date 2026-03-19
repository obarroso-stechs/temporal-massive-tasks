import asyncio
from typing import List, Union

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.constants import TEMPORAL_TASK_QUEUE
    from temporal.models import (
        ParameterUpdateBatchInput,
        ParameterUpdateResult,
        UpdateParameter,
    )
    from temporal.workflows.parameter_update.parameter_update_child_workflow import (
        ParameterUpdateChildWorkflow,
    )

BATCH_SIZE = 50


@workflow.defn
class ParameterUpdateBatchWorkflow:
    """Workflow padre: procesa miles de parameter updates en batches.

    Recibe una lista de UpdateParameter, la particiona en batches de
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

    @workflow.query
    def get_progress(self) -> dict:
        return {
            "total": self._total,
            "processed": self._processed,
            "pending": self._total - self._processed,
            "failed": self._failed,
        }

    @workflow.query
    def get_device_statuses(self) -> dict:
        return dict(self._device_statuses)

    @workflow.run
    async def run(
        self, input: ParameterUpdateBatchInput
    ) -> List[Union[ParameterUpdateResult, str]]:
        self._device_statuses = dict(input.device_statuses)

        for item in input.items:
            if item.serialNumber not in self._device_statuses:
                self._device_statuses[item.serialNumber] = "PENDING"

        self._total = len(self._device_statuses)
        self._processed = input.processed_count
        self._failed = sum(
            1 for s in self._device_statuses.values() if s == "FAILED"
        )

        results: List[Union[ParameterUpdateResult, str]] = []
        remaining = list(input.items)

        while remaining:
            batch = remaining[:BATCH_SIZE]
            remaining = remaining[BATCH_SIZE:]

            for item in batch:
                self._device_statuses[item.serialNumber] = "RUNNING"

            batch_results = await self._execute_batch(batch)
            results.extend(batch_results)

            if remaining and workflow.info().is_continue_as_new_suggested():
                workflow.logger.info(
                    f"Continue-as-new: {self._processed} procesados, "
                    f"{len(remaining)} pendientes"
                )
                workflow.continue_as_new(
                    ParameterUpdateBatchInput(
                        items=remaining,
                        processed_count=self._processed,
                        device_statuses=self._device_statuses,
                    )
                )

        workflow.logger.info(
            f"Batch completo: {self._processed} equipos procesados"
        )
        return results

    async def _execute_batch(
        self,
        batch: List[UpdateParameter],
    ) -> List[Union[ParameterUpdateResult, str]]:
        """Lanza N child workflows en paralelo y actualiza estado por completion."""
        parent_id = workflow.info().workflow_id

        async def run_one(
            idx: int,
            item: UpdateParameter,
        ) -> tuple[int, Union[ParameterUpdateResult, BaseException]]:
            try:
                result = await workflow.execute_child_workflow(
                    ParameterUpdateChildWorkflow.run,
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

        raw_results: list[Union[ParameterUpdateResult, str, None]] = [None] * len(batch)

        for done in asyncio.as_completed(tasks):
            idx, completed_result = await done
            item = batch[idx]

            if isinstance(completed_result, BaseException):
                workflow.logger.warning(
                    f"Child workflow fallo para {item.serialNumber}: {completed_result}"
                )
                raw_results[idx] = f"ERROR [{item.serialNumber}]: {completed_result}"
                self._device_statuses[item.serialNumber] = "FAILED"
                self._failed += 1
            else:
                raw_results[idx] = completed_result
                self._device_statuses[item.serialNumber] = "COMPLETED"

            self._processed += 1

        results: List[Union[ParameterUpdateResult, str]] = []
        for result in raw_results:
            if result is not None:
                results.append(result)

        return results
