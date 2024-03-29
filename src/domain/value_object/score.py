from datetime import datetime

from .base import BaseValueObject


class Score(BaseValueObject):
    value: int
    created_at: datetime
