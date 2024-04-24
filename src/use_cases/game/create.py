from abc import ABC
from abc import abstractmethod

from src.domain.entity.game import GameEntity
from src.domain.entity.user import User


class BaseGame(ABC, GameEntity):
    players: list[User]

    @abstractmethod
    def set_players(self, players: list[User]) -> None:
        pass

    @abstractmethod
    def create_game(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass
