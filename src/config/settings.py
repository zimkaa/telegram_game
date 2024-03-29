import logging
import logging.config
from pathlib import Path
from typing import Final

import yaml  # type: ignore[import]
from pydantic import Field
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .project_info import get_name
from .project_info import get_version


LOGGER_FOLDER_NAME: Final[str] = "logger"
LOGGER_CONFIG_FOLDER_NAME: Final[str] = "logging_config"

ROOT_PATH_LOGGER_FOLDER = Path(LOGGER_FOLDER_NAME)
PATH_LOGGER_FOLDER = ROOT_PATH_LOGGER_FOLDER / LOGGER_CONFIG_FOLDER_NAME


def setup_logging(config_file: str) -> None:
    config_file = PATH_LOGGER_FOLDER / config_file  # type: ignore[assignment]
    with Path(config_file).open() as f_in:
        config = yaml.safe_load(f_in)

    logging.config.dictConfig(config)


# pydantic.BaseSettings = BaseSettings  # noqa: ERA001


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    # development / test / production
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOGGER: logging.Logger = Field(default=logging.getLogger("GameLogger"))
    LOGGER_CONFIG_FILE: str = Field(default="custom_config.yaml")

    MINIMUM_PLAYERS: int = Field(default=4, ge=4, le=16)

    @computed_field  # type: ignore[misc]
    @property
    def APP_VERSION(self) -> str:  # noqa: N802
        return get_version()

    @computed_field  # type: ignore[misc]
    @property
    def APP_NAME(self) -> str:  # noqa: N802
        return get_name()


settings = Settings()
setup_logging(settings.LOGGER_CONFIG_FILE)
