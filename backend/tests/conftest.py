"""Test fixtures: an app per test, driven in-process through httpx with its lifespan running,
a real database for the tests that ask for one (db_session, db_client)."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx
import pytest
from alembic import command
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db import get_session
from app.main import create_app
from app.settings import Settings
from tests import db


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=None, app_env="test")


# A production database URL that is not the local default (the production guard refuses that).
PRODUCTION_DB = "postgresql+psycopg://app:secret@db.internal:5432/app"


@pytest.fixture
def production_values() -> dict[str, Any]:
    """The settings a production start needs because this project's parts have no safe default
    for them. Splat into Settings(app_env="production", **production_values)."""
    return {"database_url": PRODUCTION_DB}


@pytest.fixture
def expected_readiness_checks() -> set[str]:
    """The readiness checks a fresh app registers (storage adds one only when a bucket is set)."""
    return {"database"}


@pytest.fixture
def database_settings(database_url: str) -> dict[str, Any]:
    """Settings that point an app at the test database (empty in a project with no database)."""
    return {"database_url": SecretStr(database_url)}


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(app) as manager:
        transport = httpx.ASGITransport(app=manager.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture(scope="session")
def database_url() -> Iterator[str]:
    """A migrated database for the whole test session (see tests/db.py)."""
    for url in db.database_url():
        command.upgrade(db.alembic_config(url), "heads")
        yield url


@pytest.fixture
async def db_session(database_url: str) -> AsyncIterator[AsyncSession]:
    """A session whose work, commits included, is rolled back when the test ends."""
    engine = create_async_engine(database_url, poolclass=NullPool)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False
        )
        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
    await engine.dispose()


@pytest.fixture
async def db_client(
    app: FastAPI, db_session: AsyncSession, database_url: str
) -> AsyncIterator[httpx.AsyncClient]:
    """Like client, with the whole app on the test database: requests use db_session, and code
    that opens sessions from app.state.sessionmaker joins the same rolled-back transaction."""

    async def session_override() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = session_override
    # The lifespan builds the engine from these settings: the test database, never a local one.
    app.state.settings = app.state.settings.model_copy(
        update={"database_url": SecretStr(database_url)}
    )
    async with LifespanManager(app) as manager:
        app.state.sessionmaker = async_sessionmaker(
            bind=db_session.bind, join_transaction_mode="create_savepoint", expire_on_commit=False
        )
        transport = httpx.ASGITransport(app=manager.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
