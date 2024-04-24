from datetime import datetime

from pydantic import Field

from .base import BaseValueObject


class Score(BaseValueObject):
    value: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
