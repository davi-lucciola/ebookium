from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.community.postgres import PostgresContainer

from app import create_app
from app.config import settings
from app.infra.db import get_db
from app.infra.db.models import BaseEntity
from tests.integration.mocks import test_user

__all__ = ['test_user']


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    yield


app = create_app(
    title=settings.title,
    lifespan=test_lifespan,
)


@pytest.fixture(scope='session')
def postgres_url() -> str:
    with PostgresContainer('postgres:16-alpine') as postgres:
        yield postgres.get_connection_url(driver='psycopg')


@pytest.fixture
async def test_db(postgres_url: str):
    test_engine = create_async_engine(postgres_url)

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)

    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession):
    async def override_test_db():
        return test_db

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = override_test_db
        yield client

    app.dependency_overrides.clear()
