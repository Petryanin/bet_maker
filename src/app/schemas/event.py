"""Схемы, связанные с событиями."""

import enum

from pydantic import BaseModel


class EventState(enum.StrEnum):
    """Перечисление статусов событий."""

    WIN = "WIN"
    LOSE = "LOSE"


class EventUpdate(BaseModel):
    """Схема обновления события."""

    state: EventState


class EventUpdateResponse(BaseModel):
    """Схема ответа на обновление события."""

    event_id: int
    message: str
