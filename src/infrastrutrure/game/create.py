from src.domain.entity.game import GameEntity
from src.domain.entity.team import Team
from src.domain.entity.user import User
from src.domain.utils.status import GameStatus
from src.use_cases.game.create import BaseGame
from src.use_cases.team.create_team import create_teams


def create_game(players: list[User]) -> GameEntity:
    teams = create_teams(players)
    return GameEntity(teams=teams)


class Game(BaseGame):
    players: list[User]

    def set_players(self, players: list[User]) -> None:
        self.players = players

    def create_game(self) -> None:
        self.teams = self._create_game()

    def _create_game(self) -> tuple[Team, Team]:
        return create_teams(self.players)

    def start(self) -> None:
        self.status = GameStatus.STARTED

    def _distribute_words_to_teams(self) -> None:
        pass
