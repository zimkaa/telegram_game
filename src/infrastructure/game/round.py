from src.domain.entity.team import Team
from src.use_cases.game.round import BaseGameRound


class GameRound(BaseGameRound):
    def __init__(self, teams: tuple[Team, Team]) -> None:
        self.is_game_over = False
        self._first_move = teams[0]
        self._second_move = teams[1]

    def team_move(self) -> None:
        pass
