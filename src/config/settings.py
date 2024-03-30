from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .project_info import get_name
from .project_info import get_version


# pydantic.BaseSettings = BaseSettings  # noqa: ERA001

app_version = get_version()
app_name = get_name()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    DEBUG: bool = Field(default=False)
    LOGGER_LEVEL: str = Field(default="DEBUG" if DEBUG else "INFO")
    LOGGER_CONFIG_FILE: str = Field(default="custom_config.yaml")

    MINIMUM_PLAYERS: int = Field(default=4, ge=4, le=16)

    APP_VERSION: str = Field(default=app_version)
    APP_NAME: str = Field(default=app_name)


settings = Settings()
