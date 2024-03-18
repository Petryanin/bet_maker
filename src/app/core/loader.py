"""Модуль инициализации объектов конфигурации сервиса."""

import logging.config

from fastapi import FastAPI

from app.api import API_PREFIX
from app.api import api_v1_router
from app.core import config
from app.middlewares.logging import LoggingMiddleware


def init_all(app: FastAPI) -> None:
    """Инит всех частей сервиса."""
    logging.config.dictConfig(config.logging_config)
    logging.info("Initializing the app...")

    try:
        init_routers(app)
        init_middlewares(app)
    except Exception:
        logging.error("There was an error initializing the app!")
        raise

    logging.info("Initialization success!")


def init_routers(app: FastAPI) -> None:
    """Инит роутеров, определенных в `app.api`."""
    app.include_router(api_v1_router, prefix=API_PREFIX)


def init_middlewares(app: FastAPI) -> None:
    """Инит промежуточного ПО."""
    app.add_middleware(LoggingMiddleware)
