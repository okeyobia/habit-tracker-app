

import os
os.environ["TESTING"] = "1"
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app import models, database

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def async_client():
    # Setup test database and override dependency
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession
    )
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session
    app.dependency_overrides[database.get_db] = override_get_db
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(base_url="http://test", transport=transport) as ac:
            yield ac
    await engine.dispose()

import pytest

@pytest.mark.asyncio
async def test_register_and_login(async_client):
    # Register
    response = await async_client.post("/auth/register", json={"email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    # Login
    response = await async_client.post("/auth/login", data={"username": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
