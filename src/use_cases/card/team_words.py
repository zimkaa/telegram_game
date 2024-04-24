from abc import ABC
from abc import abstractmethod


class BaseRoundCard(ABC):
    @abstractmethod
    def create_game_set(self, words: list[str]) -> None:
        pass
