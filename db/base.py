"""Database infrastructure: engines, sessions, transaction context manager and @atomic decorator."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from contextlib import contextmanager
from functools import wraps
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

from configurations.database import DATABASE_URL, SYNC_DATABASE_URL

logger = logging.getLogger(__name__)

# ── Engines ───────────────────────────────────────────────────────────────────

_async_engine = create_async_engine(DATABASE_URL, echo=False)
_sync_engine = create_engine(SYNC_DATABASE_URL, echo=False, pool_pre_ping=True)

# ── Session factories ──────────────────────────────────────────────────────────

# Async session for FastAPI routes
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=_async_engine,
    expire_on_commit=False,
    autoflush=False,
)

# Sync scoped session for Temporal activities (thread-local, one per thread in ThreadPoolExecutor)
_sync_session_factory = sessionmaker(bind=_sync_engine, autocommit=False, autoflush=False, expire_on_commit=False)


# ── ORM Base ──────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── DbBase: holds the scoped session registry ─────────────────────────────────

class DbBase:
    """Namespace that holds the scoped sync session registry.

    Use get_sync_session() to obtain the current thread's Session instance.
    The @atomic decorator manages the transaction lifecycle and injects the
    session into decorated repository methods via the `session` keyword arg.
    """

    _scoped: scoped_session[Session] = scoped_session(_sync_session_factory)


def get_sync_session() -> Session:
    """Return the current thread-local Session (creates one if needed)."""
    return DbBase._scoped()


# ── Transaction context manager ───────────────────────────────────────────────

@contextmanager
def transaction() -> Generator[Session, None, None]:
    """Open a transaction on the current thread-local session.

    Yields the Session, commits on success, rolls back and re-raises on
    exception, and always removes the session from the scoped registry.
    """
    session = DbBase._scoped()
    try:
        yield session
        DbBase._scoped.commit()
    except Exception:
        DbBase._scoped.rollback()
        raise
    finally:
        DbBase._scoped.remove()


def async_atomic(function: Callable[..., Awaitable[Any]]):
    """Wrap an async repository method with transaction semantics.

    Expected argument: an AsyncSession provided as `db` kwarg or positional arg.
    If there is no active transaction, this decorator opens one and ensures
    commit/rollback semantics. If there is an outer transaction, it defers
    commit/rollback to that owner.
    """

    @wraps(function)
    async def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        if db is None:
            for arg in args:
                if isinstance(arg, AsyncSession):
                    db = arg
                    break

        if db is None:
            raise ValueError(f"{function.__name__} requires an AsyncSession argument named 'db'")

        try:
            if db.in_transaction():
                return await function(*args, **kwargs)

            async with db.begin():
                return await function(*args, **kwargs)
        except Exception as e:
            logger.exception("Rollback transaction because of exception %s", e)
            raise

    return wrapper
