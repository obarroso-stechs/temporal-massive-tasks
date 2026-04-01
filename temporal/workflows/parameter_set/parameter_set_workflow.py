import asyncio
from datetime import timedelta
from typing import List, Union

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from configurations.temporal import TEMPORAL_TASK_QUEUE
    from temporal.models import (
        ParameterSetBatchInput,
        ParameterSetResult,
        UpdateParameterSet,
    )
    from temporal.workflows.parameter_set.parameter_set_child_workflow import (
        ParameterSetChildWorkflow,
    )
    from temporal.activities.reporting_activities import (
        mark_task_started,
        mark_task_completed,
        upsert_device_status,
    )

BATCH_SIZE = 50


def _sanitize_error_detail(exc: BaseException) -> str:
    """Extrae el mensaje mas especifico de una cadena de excepciones de Temporal."""
    cause = exc
    while cause.__cause__ is not None:
        cause = cause.__cause__
    return str(cause)


@workflow.defn
class ParameterSetBatchWorkflow:
    """Workflow padre: procesa miles de parameter sets en batches."""

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
        self, input: ParameterSetBatchInput
    ) -> List[Union[ParameterSetResult, str]]:
        self._device_statuses = dict(input.device_statuses)

        for item in input.items:
            if item.serialNumber not in self._device_statuses:
                self._device_statuses[item.serialNumber] = "PENDING"

        self._total = len(self._device_statuses)
        self._processed = input.processed_count
        self._failed = sum(
            1 for s in self._device_statuses.values() if s == "FAILED"
        )

        if input.processed_count == 0:
            await workflow.execute_activity(
                mark_task_started,
                workflow.info().workflow_id,
                start_to_close_timeout=timedelta(seconds=10),
            )

        results: List[Union[ParameterSetResult, str]] = []
        remaining = list(input.items)

        while remaining:
            if self._paused:
                await workflow.wait_condition(lambda: not self._paused)

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
                    ParameterSetBatchInput(
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
        batch: List[UpdateParameterSet],
    ) -> List[Union[ParameterSetResult, str]]:
        """Lanza N child workflows en paralelo y actualiza estado por completion."""
        parent_id = workflow.info().workflow_id

        async def run_one(
            idx: int,
            item: UpdateParameterSet,
        ) -> tuple[int, Union[ParameterSetResult, BaseException]]:
            try:
                result = await workflow.execute_child_workflow(
                    ParameterSetChildWorkflow.run,
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

        raw_results: list[Union[ParameterSetResult, str, None]] = [None] * len(batch)

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
                    args=[workflow.info().workflow_id, item.serialNumber, "COMPLETED", completed_result.message],
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=RetryPolicy(maximum_attempts=5),
                )

            self._processed += 1

        results: List[Union[ParameterSetResult, str]] = []
        for result in raw_results:
            if result is not None:
                results.append(result)

        return results
