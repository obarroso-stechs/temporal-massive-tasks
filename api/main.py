from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.base import Base, _async_engine
from api.dependencies.temporal import create_temporal_client
from routers.devices import router as devices_router
from routers.device_groups import router as device_groups_router
from routers.firmware import router as firmware_router
from routers.parameter_update import router as parameter_update_router
from routers.parameter_set import router as parameter_set_router
from routers.reports import router as reports_router
from routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with _async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.temporal_client = await create_temporal_client()
    yield


app = FastAPI(
    title="Temporal Firmware API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(firmware_router)
app.include_router(parameter_update_router)
app.include_router(parameter_set_router)
app.include_router(devices_router)
app.include_router(device_groups_router)
app.include_router(reports_router)
app.include_router(tasks_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=23200, reload=True)
