from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
import uvicorn

# Allow running this file directly from /api with: python main.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dependencies import create_temporal_client
from routers.firmware import router as firmware_router
from routers.parameter_update import router as parameter_update_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Temporal Python SDK Client does not require explicit close;
    # connections are released by garbage collection.
    app.state.temporal_client = await create_temporal_client()
    yield


app = FastAPI(
    title="Temporal Firmware API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(firmware_router)
app.include_router(parameter_update_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=23200, reload=False)
