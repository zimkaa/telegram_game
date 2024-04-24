from abc import ABC
from abc import abstractmethod


class BaseGameRound(ABC):
    _is_game_over: bool

    @abstractmethod
    def team_move(self) -> None:
        pass
