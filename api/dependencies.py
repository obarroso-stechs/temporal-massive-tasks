from temporalio.client import Client
from fastapi import Request

from temporal.constants import TEMPORAL_NAMESPACE, TEMPORAL_TARGET_HOST


async def create_temporal_client() -> Client:
    return await Client.connect(
        TEMPORAL_TARGET_HOST,
        namespace=TEMPORAL_NAMESPACE,
    )


def get_temporal_client(request: Request) -> Client:
    return request.app.state.temporal_client
