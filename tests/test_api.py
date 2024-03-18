"""Модульные тесты API."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


async def test_docs(ac: AsyncClient):
    """Документация."""
    response = await ac.get("/docs")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ("event_id", "amount", "expected_http_status"),
    (
        (1, 1, HTTPStatus.CREATED),
        ("1", "1.23", HTTPStatus.CREATED),
        (1, 0, HTTPStatus.UNPROCESSABLE_ENTITY),
        (1, 1.234, HTTPStatus.UNPROCESSABLE_ENTITY),
        (1, -1, HTTPStatus.UNPROCESSABLE_ENTITY),
    ),
)
async def test_create_bet(
    event_id, amount, expected_http_status, ac: AsyncClient
) -> None:
    """Создание ставки."""
    bet = {
        "event_id": event_id,
        "amount": amount,
    }
    response = await ac.post("/bets", json=bet)

    assert response.status_code == expected_http_status


async def test_get_all_bets(ac: AsyncClient) -> None:
    """Получение всех ставок."""
    response = await ac.get("/bets")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ("state", "expected_http_status"),
    (
        ("WIN", HTTPStatus.OK),
        ("LOSE", HTTPStatus.OK),
        ("DEFEAT", HTTPStatus.UNPROCESSABLE_ENTITY),
    ),
)
async def test_update_event(state, expected_http_status, ac: AsyncClient) -> None:
    """Обновление статуса события."""
    event_id = 1
    event = {"state": state}
    response = await ac.put(f"/events/{event_id}", json=event)

    assert response.status_code == expected_http_status
