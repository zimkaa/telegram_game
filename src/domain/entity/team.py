from datetime import datetime

from pydantic import Field
from pydantic import field_validator

from src.config import settings
from src.domain.entity.base import BaseEntity
from src.domain.entity.user import User

# from src.domain.utils.color import TeamColor  # noqa: ERA001
from src.domain.utils.role import Role
from src.domain.value_object.score import Score


class Team(BaseEntity):
    players: list[User]
    # color: TeamColor  # noqa: ERA001
    role: Role = Role.PLAYER
    score: Score | None = Field(default=None)
    created_at: datetime | None = Field(default=None)

    @field_validator("players", mode="before")
    @classmethod
    def check_card_number_omitted(cls: type["Team"], data: list[User]) -> list[User]:
        if len(data) < settings.MINIMUM_PLAYERS:
            msg = f"The number of players must be at least {settings.MINIMUM_PLAYERS}."
            raise ValueError(msg)
        return data
