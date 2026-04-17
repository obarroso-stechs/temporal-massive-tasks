"""FastAPI async DB dependency."""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session with an open transaction for the duration of the request."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
