import asyncio
from typing import List, Union

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from temporal.constants import TEMPORAL_TASK_QUEUE
    from temporal.models import (
        FirmwareUpdateBatchInput,
        FirmwareUpdateResult,
        UpdateFirmware,
    )
    from temporal.workflows.child_workflow import FirmwareUpdateChildWorkflow

# Cuántos child workflows lanzar en paralelo por batch.
# Cada child genera ~5 eventos en el padre (init, started, completed).
# Con BATCH_SIZE=50 y continue-as-new, nos mantenemos lejos del límite de 50K eventos.
BATCH_SIZE = 50


@workflow.defn
class FirmwareUpdateBatchWorkflow:
    """Workflow padre: procesa miles de firmware updates en batches.

    Recibe una lista de UpdateFirmware, la particiona en batches de
    BATCH_SIZE, lanza cada batch en paralelo con asyncio.gather, y
    usa continue-as-new cuando Temporal lo sugiere para mantener
    el Event History acotado.
    """

    @workflow.run
    async def run(
        self, input: FirmwareUpdateBatchInput
    ) -> List[Union[FirmwareUpdateResult, str]]:
        results: List[Union[FirmwareUpdateResult, str]] = []
        remaining = list(input.items)
        total_processed = input.processed_count

        while remaining:
            batch = remaining[:BATCH_SIZE]
            remaining = remaining[BATCH_SIZE:]

            batch_results = await self._execute_batch(batch, total_processed)
            results.extend(batch_results)
            total_processed += len(batch)

            # Checkpoint: si Temporal sugiere continue-as-new, reiniciar
            # con los items que quedan y el progreso acumulado.
            if remaining and workflow.info().is_continue_as_new_suggested():
                workflow.logger.info(
                    f"Continue-as-new: {total_processed} procesados, "
                    f"{len(remaining)} pendientes"
                )
                workflow.continue_as_new(
                    FirmwareUpdateBatchInput(
                        items=remaining,
                        processed_count=total_processed,
                    )
                )

        workflow.logger.info(
            f"Batch completo: {total_processed} equipos procesados"
        )
        return results

    async def _execute_batch(
        self,
        batch: List[UpdateFirmware],
        offset: int,
    ) -> List[Union[FirmwareUpdateResult, str]]:
        """Lanza N child workflows en paralelo y espera a que terminen todos."""
        parent_id = workflow.info().workflow_id

        raw_results = await asyncio.gather(
            *[
                workflow.execute_child_workflow(
                    FirmwareUpdateChildWorkflow.run,
                    item,
                    id=f"{parent_id}-child-{offset + idx}",
                    task_queue=TEMPORAL_TASK_QUEUE,
                )
                for idx, item in enumerate(batch)
            ],
            return_exceptions=True,
        )
        print("Raw results:", raw_results)
        results: List[Union[FirmwareUpdateResult, str]] = []
        for idx, result in enumerate(raw_results):
            if isinstance(result, BaseException):
                item = batch[idx]
                workflow.logger.warning(
                    f"Child workflow falló para {item.serialNumber}: {result}"
                )
                results.append(
                    f"ERROR [{item.serialNumber}]: {result}"
                )
            else:
                results.append(result)

        return results
