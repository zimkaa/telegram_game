from dataclasses import dataclass
from random import choice
from random import sample

from src.config.constants import MAX_FIRST_TEAM_CARDS
from src.config.constants import MAX_NEUTRAL_CARDS
from src.config.constants import MAX_SECOND_TEAM_CARDS


@dataclass(init=False)
class RoundCard:
    stop_word: str
    all_words: list[str]
    first_team_words: list[str]
    second_team_words: list[str]
    another_words: list[str]
    _words_copy: list[str]

    def create_game_set(self, words: list[str]) -> None:
        self.all_words = words
        self._copy_words()
        self._set_words_category()

    def _set_words_category(self) -> None:
        self._set_stop_word()
        self._set_first_team_words()
        self._set_second_team_words()
        self._set_another_words()

    def _copy_words(self) -> None:
        assert self.all_words is not None
        self._words_copy = self.all_words.copy()

    def _set_stop_word(self) -> None:
        self.stop_word = choice(self._words_copy)  # noqa: S311
        self._remove_elements([self.stop_word])
        assert self.stop_word is not None

    def _remove_elements(self, words: list[str]) -> None:
        for word in words:
            self._words_copy.remove(word)

    def _set_first_team_words(self) -> None:
        self.first_team_words = sample(self._words_copy, k=MAX_FIRST_TEAM_CARDS)
        self._remove_elements(self.first_team_words)
        assert self.first_team_words is not None

    def _set_second_team_words(self) -> None:
        self.second_team_words = sample(self._words_copy, k=MAX_SECOND_TEAM_CARDS)
        self._remove_elements(self.second_team_words)
        assert self.second_team_words is not None

    def _set_another_words(self) -> None:
        self.another_words = self._words_copy
        assert self._words_copy is not None
        assert len(self._words_copy) == MAX_NEUTRAL_CARDS
