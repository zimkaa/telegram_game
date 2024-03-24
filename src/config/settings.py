import logging

import pydantic
from pydantic import Field
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .project_info import get_name
from .project_info import get_version


pydantic.BaseSettings = BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    # development / test / production
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOGGER: logging.Logger = Field(default=logging.getLogger("SalesLogger"))

    @computed_field  # type: ignore[misc]
    @property
    def APP_VERSION(self) -> str:  # noqa: N802
        return get_version()

    @computed_field  # type: ignore[misc]
    @property
    def APP_NAME(self) -> str:  # noqa: N802
        return get_name()


settings = Settings()
