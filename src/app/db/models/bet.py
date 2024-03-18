"""Модель ставки."""

from __future__ import annotations

import logging
from typing import Sequence

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app import schemas
from app.db import const
from app.db import models


class Bet(models.Base):
    """Класс модели ставки."""

    __tablename__ = "bet"

    bet_id: Mapped[const.DBTypes.integer] = mapped_column(primary_key=True)
    event_id: Mapped[const.DBTypes.integer] = mapped_column(nullable=False)
    amount: Mapped[const.DBTypes.numeric] = mapped_column(nullable=False)
    state: Mapped[const.DBTypes.smallint] = mapped_column(
        default=schemas.BetState.NOT_PLAYED
    )

    @staticmethod
    async def create(
        db_session: AsyncSession,
        bet: schemas.BetCreate,
    ) -> int | None:
        """Создает ставку.

        Args:
            db_session: Объект сессии БД.
            bet: Объект создаваемой ставки.

        Returns:
            ID созданной ставки.
        """
        try:
            stmt = (
                insert(Bet)
                .values(
                    event_id=bet.event_id,
                    amount=bet.amount,
                )
                .returning(Bet.bet_id)
            )
            result = await db_session.execute(stmt)
            await db_session.commit()
        except SQLAlchemyError:
            await db_session.rollback()
            raise

        return result.scalars().first()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> Sequence[Bet]:
        """Возвращает список всех ставок.

        Args:
            db_session: Объект сессии БД.

        Returns:
            Список ставок.
        """
        try:
            stmt = select(Bet)
            result = await db_session.execute(stmt)
        except SQLAlchemyError:
            await db_session.rollback()
            raise

        return result.scalars().all()

    @staticmethod
    async def update_state(
        event_id: int, state: schemas.BetState, db_session: AsyncSession
    ) -> None:
        """Обновлеят статус ставки по ID события.

        Args:
            event_id: ID события.
            state: Статус события.
            db_session: Объект сессии БД.

        Returns:
            Список обновленных ставок.
        """
        try:
            stmt = update(Bet).where(Bet.event_id == event_id).values(state=state)
            await db_session.execute(stmt)
            await db_session.commit()
        except SQLAlchemyError as exc:
            await db_session.rollback()
            logging.error(
                f"Failed to update bets for event {event_id} with state {state}: {exc}"
            )
