from src.domain.entity.user import User
from src.scenarios.create_team import create_teams


def test_create(players: list[User]) -> None:
    teams = create_teams(players)
    assert len(teams[0].players) - len(teams[1].players) in (0, 1, -1)
