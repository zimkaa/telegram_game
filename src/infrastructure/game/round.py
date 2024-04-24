from random import choice

from src.domain.entity.team import Team
from src.domain.value_object.score import Score
from src.infrastructure.card.team_words import RoundCard
from src.use_cases.game.round import BaseGameRound


class GameRound(BaseGameRound):
    _is_game_over: bool

    def __init__(self, teams: tuple[Team, Team], cards: RoundCard) -> None:
        self.is_game_over = False
        self._first_move = teams[0]
        self._second_move = teams[1]
        self._cards = cards

    def team_move(self) -> None:
        pass

    def process_round(
        self,
        team: Team,
        team_choice: str | None = None,
    ) -> None:
        if team_choice is None:
            team_choice = choice(self._cards.all_words)  # noqa: S311

        if team_choice == self._cards.stop_word:
            self._is_game_over = True
            return

        words = self._cards.first_team_words if team == self._first_move else self._cards.second_team_words

        if team == self._first_move:
            words = self._cards.first_team_words
            if team_choice in words:
                self._first_move.score = Score(value=self._first_move.score.value + 1)
                return
        else:
            words = self._cards.second_team_words
            if team_choice in words:
                self._second_move.score = Score(value=self._second_move.score.value + 1)
                return

        self._change_of_stroke = True
