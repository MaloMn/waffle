from waffle import Waffle
import numpy as np
from numpy.typing import ArrayLike
from typing import List, Set, Tuple, Any, Dict
from utils import load_data, check_grid, words_to_grid


class WaffleSolver:

    def __init__(self, waffle: Waffle):
        self.waffle = waffle
        self.location_constraints: List[List[Set[str]]] = words_constraints(self.waffle)
        self.freq_constraints: Dict[str, int] = get_frequency(self.waffle.shuffled_grid)
        self.solution: List[str] = []

    def solve(self) -> None:
        """
        Returns a solution to the waffle puzzle.
        This solution is a possibility, and might not be the right one.
        This solution satisfies constraints set by the game.
        :return: List of words forming the solution.
        """
        self.solution = ['' for i in range(6)]
        if self.rec_find_solution(0):
            return

    def rec_find_solution(self, word_index: int) -> bool:
        """
        Recursive method to solve the waffle puzzle.
        :return: boolean
        """
        # Ending condition
        if word_index > 5:
            return True

        for word in get_words_match(self.location_constraints[word_index]):
            # See if words fits
            option = self.solution[:]
            option[word_index] = word
            if check_grid(option, word_index) and check_freq_constraint(
                    self.freq_constraints, get_frequency(words_to_grid(option))):
                self.solution[word_index] = word
                if self.rec_find_solution(word_index + 1):
                    return True
                self.solution[word_index] = ''

        # No word fits, backtrack!
        return False


def words_constraints(waffle: Waffle, details: bool = False) -> List[List[Set[str]]]:
    constraints: List[List[Set[str]]] = [[set() for i in range(5)] for i in range(5)]

    print(waffle.shuffled_grid)
    print(waffle.diff)

    green = np.where(waffle.diff == 0)
    orange = np.where(waffle.diff == 1)
    black = np.where(waffle.diff == 2)

    if details:
        print("Diff matrix:")
        print(waffle.diff)
        print("\nGreen:", list(zip(*green)))
        print("Orange:", list(zip(*orange)))
        print("Black:", list(zip(*black)))

    # Add black letters to other lines/columns
    for pos in list(zip(*black)):
        letter = waffle.shuffled_grid[pos]

        # 1. Gather all positions
        positions = {(x, y) for x in range(5) for y in range(5)}

        # Remove lines / columns positions
        positions.difference(set(get_line_column(pos)))

        # Now that positions have been curated, we add the letter to the constraints
        for x, y in positions:
            constraints[x][y].add(letter)

    if details:
        print("\nAdded black letters:")
        print(constraints)

    # Add orange letters on their respective lines and/or columns
    for pos in list(zip(*orange)):
        letter = waffle.shuffled_grid[pos]

        for i, j in get_line_column(pos):
            if (i, j) != pos:
                constraints[i][j].add(letter)
            elif letter in constraints[i][j]:
                constraints[i][j].remove(letter)

    if details:
        print("\nAdded orange letters:")
        print(constraints)

    # Set letters that are right
    for x, y in list(zip(*green)):
        letter = waffle.shuffled_grid[x, y]
        if letter == ' ':
            constraints[x][y] = set()
        else:
            constraints[x][y] = set(letter)

    if details:
        print("\nAdded green letters:")
        print(constraints)

    return grid_constraints_to_constraints(constraints)


def get_frequency(waffle_grid: ArrayLike, details: bool = False) -> Dict[str, int]:
    """
    Returns a dictionary with the frequency of each letter in the grid.
    :param waffle_grid:
    :param details:
    :return:
    """
    frequency: Dict[str, int] = {letter: 0 for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
    letters = ''.join([''.join(w) for w in waffle_grid])

    for letter in letters:
        if letter in frequency.keys():
            frequency[letter] += 1

    return {k: v for k, v in frequency.items() if v > 0}


def get_line_column(position: Tuple[int, int]):
    x, y = position

    output: List[Tuple[int, int]] = []

    # Located on a full line
    if x % 2 == 0:
        output += [(x, i) for i in range(5)]

    # Located on a full column
    if y % 2 == 0:
        output += [(i, y) for i in range(5)]

    return output


def grid_constraints_to_constraints(grid: List[List[Any]]) -> List[List[Any]]:
    """
    Converts a waffle grid to a list of words.
    :param grid:
    :return:
    """
    return [[grid[x][2] for x in range(5)], [grid[2][y] for y in range(5)],
            [grid[0][y] for y in range(5)], [grid[x][4] for x in range(5)],
            [grid[4][y] for y in range(5)], [grid[x][0] for x in range(5)]]


def grid_to_words(grid: List[List[Any]]) -> List[Any]:
    """
    Converts a waffle grid to a list of words.
    :param grid:
    :return:
    """
    output = grid_constraints_to_constraints(grid)
    return [''.join(w) for w in output]


def get_words_match(constraint: List[Set[str]]) -> List[str]:
    """
    Returns the words that match the given constraint.
    :param constraint:
    :return:
    """
    return [word for word in load_data() if word[0] in constraint[0] and
            word[1] in constraint[1] and word[2] in constraint[2] and
            word[3] in constraint[3] and word[4] in constraint[4]]


def check_freq_constraint(true, observed) -> bool:
    """
    Checks if the frequency constraint is satisfied.
    :param true:
    :param observed:
    :return:
    """
    return all([observed[letter] <= true[letter] for letter in observed])


if __name__ == "__main__":
    waffle = Waffle()
    waffle.load_shuffled_waffle(['aatue', 'eltbv', 'roaal', 'lovin', 'tiein', 'raent'],
                                np.array([[0, 2, 1, 0, 0], [2, 0, 2, 0, 2], [1, 2, 0, 1, 2],
                                          [2, 0, 2, 0, 1], [0, 2, 2, 2, 0]]))

    solver = WaffleSolver(waffle)
    solver.solve()

    print(solver.solution)
