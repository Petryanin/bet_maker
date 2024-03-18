"""Схемы, связанные со ставками."""

import decimal
import enum
from typing import Annotated

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class BetState(enum.IntEnum):
    """Перечисление статусов ставок."""

    NOT_PLAYED = enum.auto()
    WIN = enum.auto()
    LOSE = enum.auto()


class BetCreate(BaseModel):
    """Cхема создания ставки."""

    event_id: Annotated[int, Field(gt=0)]
    amount: Annotated[decimal.Decimal, Field(gt=0, decimal_places=2)]


class BetCreateSuccess(BaseModel):
    """Cхема успешного создания ставки."""

    bet_id: int
    message: str


class BetShow(BaseModel):
    """Публичная схема ставки."""

    model_config = ConfigDict(from_attributes=True)

    bet_id: int
    event_id: int
    state: BetState
    amount: decimal.Decimal
