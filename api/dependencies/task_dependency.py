from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import AsyncSessionLocal
from db.dependencies import get_db
from db.services.task_service import TaskService


async def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)


@asynccontextmanager
async def get_task_service_scope() -> AsyncIterator[TaskService]:
    """Yield a TaskService with managed async session/transaction lifecycle.

    Uses AsyncSessionLocal directly to avoid the async-for + return pattern
    that triggers GeneratorExit on the generator, causing SQLAlchemy to
    rollback instead of commit.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield TaskService(session)
