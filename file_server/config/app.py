from pathlib import Path
from typing import Literal, final

from pydantic import Field
from pydantic_settings import BaseSettings


@final
class AppSettings(BaseSettings):
    """
    Основные настройки приложения.

    Attributes:
        app_name (str): Имя приложения.
        environment (Literal["local", "dev", "development", "prod"]): Среда приложения.
        log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR"]): Уровень ведения журнала.
        debug (bool): Флаг режима отладки.
    """

    app_name: str = "FileServer"
    environment: Literal["local", "dev", "development", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    debug: bool = Field(False, alias="DEBUG")

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"