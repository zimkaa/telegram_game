from src.config.words import GAME_WORDS
from src.config.words import MAX_GAME_WORDS
from src.domain.entity.user import User
from src.scenarios.team.create_team import create_teams


def test_create(players: list[User]) -> None:
    assert len(GAME_WORDS) == MAX_GAME_WORDS
    teams = create_teams(players)
    assert len(teams[0].players) - len(teams[1].players) in (0, 1, -1)
    assert len(GAME_WORDS) == MAX_GAME_WORDS
