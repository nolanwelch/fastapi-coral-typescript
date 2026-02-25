from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine_test) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
