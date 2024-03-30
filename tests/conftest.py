import pytest

from src.domain.entity.game import Game
from src.domain.entity.team import Team
from src.domain.entity.user import User


@pytest.fixture()
def static_user() -> User:
    return User(telegram_id=1, username="Ben")


@pytest.fixture()
def random_user() -> User:
    return User(telegram_id=3, username="ANT")


@pytest.fixture()
def players(static_user: User) -> list[User]:
    return [static_user for _ in range(25)]


@pytest.fixture()
def static_team(static_user: User) -> Team:
    return Team(
        players=[
            static_user,
            static_user,
            static_user,
            static_user,
        ],
    )


@pytest.fixture()
def random_team(static_user: User, random_user: User) -> Team:
    return Team(
        players=[
            static_user,
            random_user,
            random_user,
            random_user,
        ],
    )


@pytest.fixture()
def static_teams(static_team: Team, random_team: Team) -> tuple[Team, Team]:
    return (static_team, random_team)


@pytest.fixture()
def game(static_teams: tuple[Team, Team]) -> Game:
    return Game(teams=static_teams)
