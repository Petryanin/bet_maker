"""Конфигурация для модульных тестов."""

import asyncio  # noqa
from collections.abc import AsyncGenerator
from collections.abc import Generator

import httpx
import pytest

from app.core import dependencies
from app.db.models.bet import Bet
from app.main import app


async def mock_db_session() -> AsyncGenerator[int, None]:
    """Мок получения сессии БД."""
    yield 1


@pytest.fixture(autouse=True, scope="session")
def override_dependencies() -> Generator[None, None, None]:
    """Фикстура переопределения зависимостей."""
    app.dependency_overrides[dependencies.get_db_session] = mock_db_session

    yield

    app.dependency_overrides = {}


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Фикстура получения сессии клиента."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),  # pyright: ignore
        base_url="http://127.0.0.1:8080",
    ) as session:
        yield session


async def mock_bet_create(*args, **kwarsg) -> int:
    """Мок записи ставки в БД."""
    return 1


async def mock_bet_get_all(*args, **kwarsg) -> list:
    """Мок получения всех ставок из БД."""
    return []


async def mock_bet_update_state(*args, **kwarsg) -> None:
    """Мок получения всех ставок из БД."""


@pytest.fixture(autouse=True)
def patch(monkeypatch: pytest.MonkeyPatch):
    """Фикстура для патчинга методов."""

    monkeypatch.setattr(Bet, "create", mock_bet_create)
    monkeypatch.setattr(Bet, "get_all", mock_bet_get_all)
    monkeypatch.setattr(Bet, "update_state", mock_bet_update_state)
