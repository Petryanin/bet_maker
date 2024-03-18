"""Константы для работы с БД."""

import decimal
from typing import Annotated

import sqlalchemy
from sqlalchemy.engine.url import URL

from app.core.config import app_config


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=app_config.postgres_user,
    password=app_config.postgres_password,
    host=app_config.postgres_host,
    port=app_config.postgres_port,
    database=app_config.postgres_name,
)


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class DBTypes:
    """Переопределенные Python-типы данных для использования в рамках ORM."""

    text = Annotated[str, "text"]
    varchar_50 = Annotated[str, 50]
    varchar_255 = Annotated[str, 255]

    smallint = Annotated[int, 16]
    integer = Annotated[int, 32]
    bigint = Annotated[int, 64]

    numeric = decimal.Decimal


TYPE_ANNOTATION_MAP = {
    DBTypes.text: sqlalchemy.TEXT,
    DBTypes.varchar_50: sqlalchemy.VARCHAR(50),
    DBTypes.varchar_255: sqlalchemy.VARCHAR(255),
    DBTypes.smallint: sqlalchemy.SMALLINT,
    DBTypes.integer: sqlalchemy.INTEGER,
    DBTypes.bigint: sqlalchemy.BIGINT,
    DBTypes.numeric: sqlalchemy.NUMERIC,
}
