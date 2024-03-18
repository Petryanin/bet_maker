"""Модуль конфигурации сервиса."""

from typing import Any

import yaml
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Класс для хранения настроек приложения.

    Использует Pydantic для валидации и парсинга настроек из файла конфигурации.
    """

    # logging
    logging_config_path: str

    # database
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_port: int
    postgres_host: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_logging_config(config_path: str) -> dict[str, Any]:
    """Инициализирует конфигурацию логгера приложения.

    Args:
        config_path: Путь к файлу конфигурации.

    Returns:
        Словарь с конфигурацией логгера.
    """
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    return config


app_config = Settings()  # pyright: ignore
logging_config = get_logging_config(app_config.logging_config_path)
