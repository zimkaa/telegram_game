from src.config.constants import MAX_FIRST_TEAM_CARDS
from src.config.constants import MAX_NEUTRAL_CARDS
from src.config.constants import MAX_SECOND_TEAM_CARDS
from src.scenarios.card.team_words import RoundCard


def test_cards_set(game_words: list[str]) -> None:
    my_round = RoundCard()
    my_round.create_game_set(game_words)
    assert my_round.all_words == game_words
    assert len(my_round.first_team_words) == MAX_FIRST_TEAM_CARDS
    assert len(my_round.second_team_words) == MAX_SECOND_TEAM_CARDS
    assert len(my_round.another_words) == MAX_NEUTRAL_CARDS
    assert isinstance(my_round.stop_word, str)
    assert my_round.stop_word not in my_round.first_team_words
    assert my_round.stop_word not in my_round.second_team_words
    assert set(my_round.first_team_words) != set(my_round.second_team_words)
