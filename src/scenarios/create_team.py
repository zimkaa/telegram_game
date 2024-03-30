from random import shuffle

from src.domain.entity.team import Team
from src.domain.entity.user import User


def create_teams(players: list[User]) -> tuple[Team, Team]:
    shuffle(players)
    middle_index = len(players) // 2
    team1 = players[0:middle_index]
    players[middle_index:]
    return (Team(players=team1), Team(players=team1))
