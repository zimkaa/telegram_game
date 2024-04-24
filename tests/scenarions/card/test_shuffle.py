from src.config.constants import MAX_GAME_CARDS
from src.use_cases.card.shuffle import get_shuffled_words


def test_shuffle() -> None:
    words = get_shuffled_words()
    assert words
    assert len(words) == MAX_GAME_CARDS
    assert len(words) == len(set(words))


def test_second() -> None:
    assert True
