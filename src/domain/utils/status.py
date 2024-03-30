from enum import StrEnum
from enum import auto


class GameStatus(StrEnum):
    PREPARING = auto()
    STARTED = auto()
    PAUSED = auto()
    ENDED = auto()
