"""V1."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    bet as api_bet,
)
from app.api.v1.endpoints import (
    event as api_event,
)


api_router = APIRouter()

api_router.include_router(api_bet.router, prefix="/bets", tags=["bets"])
api_router.include_router(api_event.router, prefix="/events", tags=["events"])
