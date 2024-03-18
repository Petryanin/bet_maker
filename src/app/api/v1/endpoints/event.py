"""Обработчики запросов, связанных с событиями."""

from typing import Annotated

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.dependencies import get_db_session
from app.db.models.bet import Bet


router = APIRouter()


@router.put("/{event_id}")
async def update_event(
    event_id: Annotated[int, Path(gt=0)],
    body: schemas.EventUpdate,
    background_tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db_session),
) -> schemas.EventUpdateResponse:
    """Обновляет событие, попутно обновляя связанные с ним ставки.

    Args:
        event_id: ID события.
        body: Тело запроса со статусом события.
        background_tasks: Объект для запуска фоновых задач.
        db_session: Объект сессии БД.

    Returns:
        Ответ об об успешности обновления.
    """
    bet_state = getattr(schemas.BetState, body.state)

    background_tasks.add_task(
        Bet.update_state,
        event_id=event_id,
        state=bet_state,
        db_session=db_session,
    )

    return schemas.EventUpdateResponse(
        event_id=event_id, message="Event updated successfully"
    )
