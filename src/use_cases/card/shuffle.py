from random import sample

from src.config.words import GAME_WORDS


def get_shuffled_words() -> list[str]:
    return sample(GAME_WORDS, k=25)
