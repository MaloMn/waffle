from typing import List, Generator
import numpy as np
from numpy.typing import ArrayLike
import copy


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
    for word in choices[:index + 1]:
        if choices.count(word) > 1:
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
    Convert list of words to the grid of letters forming the waffle.
    :param words: List of words
    :return: Grid of letters
    """
    output = np.array([[' '] * 5] * 5)

    # First word
    for i in range(5):
        if i < len(words[0]):
            output[i, 2] = words[0][i]

    # Second word
    for i in [0, 1, 3, 4]:
        if i < len(words[1]):
            output[2, i] = words[1][i]

    # Third word
    for i in [0, 1, 3, 4]:
        if i < len(words[2]):
            output[0, i] = words[2][i]

    # Fourth word
    for i in [1, 3, 4]:
        if i < len(words[3]):
            output[i, 4] = words[3][i]

    # Fifth word
    for i in [0, 1, 3]:
        if i < len(words[4]):
            output[4, i] = words[4][i]

    # Sixth word
    for i in [1, 3]:
        if i < len(words[5]):
            output[i, 0] = words[5][i]

    return output


def grid_path_generator(n: int) -> Generator[int, None, None]:
    for i in range(n):
        for j in range(n):
            yield i, j


def get_diff(true_grid: ArrayLike, shuffled_grid: ArrayLike) -> ArrayLike:
    diff = np.full((5, 5), 2)

    # To handle words containing twice or more the same letter, a reference is built
    # and letters are removed from that reference when they are used
    ref = copy.deepcopy(true_grid)

    # Remove from ref correctly placed letters
    for x, y in grid_path_generator(5):
        if shuffled_grid[x, y] == true_grid[x, y]:
            ref[x, y] = ''
            diff[x, y] = 0

    for x, y in grid_path_generator(5):
        letter = shuffled_grid[x, y]

        if letter == ' ' or letter == true_grid[x, y]:
            continue

        if x % 2 == 1 and y % 2 == 0 :
            # Located in lines 1 and 3
            if letter in ref[:, y]:
                diff[x, y] = 1
                idx = np.where(ref[:, y] == letter)
                ref[idx, y] = ''

        elif x % 2 == 0 and y % 2 == 1:
            # Located in columns 1 and 3
            if letter in ref[x, :]:
                diff[x, y] = 1
                idx = np.where(ref[:, x] == letter)
                ref[x, idx] = ''

        elif letter in ref[x, :] or letter in ref[:, y]:
            diff[x, y] = 1

            idx = np.where(ref == letter)
            idx = [i for i in list(zip(*idx)) if i[0] == x or i[1] == y][0]
            ref[idx] = ''

    return diff


def grid_string_to_words(grid: str) -> List[str]:
    """
    Converts a grid string to a list of words
    :param grid: grid string
    :return: list of words
    """
    grid = grid.upper()
    return [grid[2:19:4], grid[8:13], grid[:5], ''.join([grid[i] for i in [4, 7, 12, 15, 20]]), grid[16:],
            ''.join([grid[i] for i in [0, 5, 8, 13, 16]])]


def words_to_grid_string(words: List[str]) -> str:
    """
    Converts a list of words to a grid string
    :param words: list of words
    :return: grid string
    """
    return ''.join([words[2], words[5][1], words[0][1], words[3][1],
                    words[1], words[5][3], words[0][3], words[3][3],
                    words[4]])


if __name__ == "__main__":
    print(grid_string_to_words('roaalaaoeltbvnuitiein'))
