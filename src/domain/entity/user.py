from datetime import datetime

from pydantic import Field

from src.domain.entity.base import BaseEntity
from src.domain.utils.role import Role
from src.domain.value_object.score import Score


class User(BaseEntity):
    telegram_id: int
    username: str
    role: Role = Role.PLAYER
    score: Score | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
