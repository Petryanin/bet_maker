"""Основной модуль."""

import logging

import uvicorn
from fastapi import FastAPI

from app.core import config
from app.core import loader


app = FastAPI(
    title="Bet Maker",
    description="Service for making bets",
    version="0.1.0",
)
loader.init_all(app)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        log_config=config.logging_config,
        log_level=logging.DEBUG,
        reload=True,
    )
