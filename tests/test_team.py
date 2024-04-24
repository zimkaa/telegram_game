import pytest

from src.domain.entity.team import Team
from src.domain.entity.user import User
from src.domain.value_object.score import Score


def test_create() -> None:
    team = Team(
        players=[
            User(telegram_id=1, username="Ben"),
            User(telegram_id=2, username="Ant"),
            User(telegram_id=3, username="Den"),
            User(telegram_id=4, username="Gin"),
            User(telegram_id=5, username="Lin"),
        ],
        score=Score(),
    )
    assert team


def test_create_error() -> None:
    TeamClass = Team  # noqa: N806
    with pytest.raises(ValueError, match=f"validation error for {TeamClass.__name__}"):
        TeamClass(
            players=[
                User(telegram_id=1, username="Ben"),
                User(telegram_id=2, username="Ant"),
                User(telegram_id=3, username="Den"),
            ],
            score=Score(),
        )
