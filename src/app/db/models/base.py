"""Базовая модель."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.db import const


class Base(DeclarativeBase):
    """Базовый класс, используемый для декларативного определения моделей."""

    metadata = MetaData(naming_convention=const.POSTGRES_INDEXES_NAMING_CONVENTION)
    type_annotation_map = const.TYPE_ANNOTATION_MAP
