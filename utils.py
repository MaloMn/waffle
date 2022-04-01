from typing import List, Generator
import numpy as np
from numpy.typing import ArrayLike


def load_data() -> List[str]:
    """
    Loads every 5-letters words from words.txt
    :return: List containing 5-letters words
    """
    with open("words.txt") as f:
        return [w.upper() for w in f.read().splitlines()]


def check_grid(choices: List[str], index: int) -> bool:
    """
    Checks that a given list of words forms a valid grid.
    :param choices: (potentially not full) list of words
    :param index: Number of words in choices
    :return: boolean
    """

    # TODO Find index based on the number of '' in the array
    # Check that a word does not appear more than once
    for word in choices:
        if word != '' and choices.count(word) > 1:
            return False

    output = True

    if index >= 1:
        output &= choices[1][2] == choices[0][2]
    if index >= 2:
        output &= choices[2][2] == choices[0][0]
    if index >= 3:
        output &= choices[3][2] == choices[1][4] and choices[3][0] == choices[2][4]
    if index >= 4:
        output &= choices[4][2] == choices[0][4] and choices[4][4] == choices[3][4]
    if index >= 5:
        output &= choices[5][0] == choices[2][0] and choices[5][2] == choices[1][0] and choices[5][4] == choices[4][0]

    return output


def words_to_grid(words: List[str]) -> ArrayLike:
    """
    Convert list of words to the grid of letters formong the waffle.
    :param words: List of words
    :return: Grid of letters
    """
    return np.array([list(words[2]), [words[5][1], ' ', words[0][1], ' ', words[3][1]], list(words[1]),
                     [words[5][3], ' ', words[0][3], ' ', words[3][3]], list(words[4])])


def grid_path_generator(n: int) -> Generator[int, None, None]:
    for i in range(n):
        for j in range(n):
            yield i, j
