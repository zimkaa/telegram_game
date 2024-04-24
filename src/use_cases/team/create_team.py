from random import shuffle

from src.domain.entity.team import Team
from src.domain.entity.user import User
from src.domain.value_object.score import Score


def create_teams(players: list[User]) -> tuple[Team, Team]:
    shuffle(players)
    middle_index = len(players) // 2
    team1 = players[:middle_index]
    team2 = players[middle_index:]
    return (Team(players=team1, score=Score()), Team(players=team2, score=Score()))
