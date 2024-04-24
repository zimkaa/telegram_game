from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from pydantic import Field

from src.domain.entity.base import BaseEntity
from src.domain.entity.team import Team

# from src.domain.utils.color import TeamColor  # noqa: ERA001
from src.domain.utils.status import GameStatus
from src.domain.value_object.score import Score


class GameEntity(BaseEntity):
    id: UUID4 = Field(default_factory=uuid4)
    teams: tuple[Team, Team] | None = Field(default=None)
    # color: TeamColor  # noqa: ERA001
    start_at: datetime | None = Field(default=None)
    end_at: datetime | None = Field(default=None)
    status: GameStatus = Field(default=GameStatus.PREPARING)

    score: Score | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
