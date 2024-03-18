"""Обработчики запросов, связанных со ставками."""

import logging
from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.dependencies import get_db_session
from app.db.models.bet import Bet


router = APIRouter()


@router.get("")
async def get_bets(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[schemas.BetShow]:
    """Возвращает список ставок.

    Args:
        db_session: Объект сессии БД.

    Returns:
        Список ставок.
    """
    try:
        bets = await Bet.get_all(db_session)
    except Exception as exc:
        message = "Failed to get all bets"
        logging.error(f"{message}: {exc}")
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, detail=message) from exc

    return [schemas.BetShow.model_validate(bet) for bet in bets]


@router.post("", status_code=HTTPStatus.CREATED)
async def create_bet(
    bet: schemas.BetCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> schemas.BetCreateSuccess:
    """Создает ставку.

    Args:
        bet: Объект ставки.
        db_session: Объект сессии БД.

    Returns:
        Ответ об успешности создания.
    """
    try:
        bet_id = await Bet.create(db_session, bet)
        if not isinstance(bet_id, int):
            raise Exception(f"{bet_id=}")
    except Exception as exc:
        message = "Failed to create a bet"
        logging.error(f"{message}: {exc}")
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, detail=message) from exc

    return schemas.BetCreateSuccess(bet_id=bet_id, message="Bet created successfully")
