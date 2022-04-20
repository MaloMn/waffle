"""
Once the words of the waffle have been determined,
a path towards this solution in a minimal number
of moves is needed.

I decide to use a version of the A* algorithm to tackle this problem.
Main source: https://en.wikipedia.org/wiki/A*_search_algorithm

Grid will be represented as strings representing the state of the grid:

    A B C D E
    F   G   H
    I J K L M   => "ABCDEFGHIJKLMNOPQRSTU"
    N   O   P
    Q R S T U

"""
from typing import Dict, Set, List, Generator, Optional, Tuple
from colors import GREEN, YELLOW, ENDC
from utils import get_diff
from numpy.typing import ArrayLike
import numpy as np
from statistics import mean


# Conversion functions below
def grid_from_grid_string(grid: str) -> ArrayLike:
    return np.array([list(grid[:5]),
                     [grid[5], ' ', grid[6], ' ', grid[7]],
                     list(grid[8:13]),
                     [grid[13], ' ', grid[14], ' ', grid[15]],
                     list(grid[16:])])


def grid_string_from_grid(diff: ArrayLike) -> str:
    diff[1, 1] = -1
    diff[1, 3] = -1
    diff[3, 1] = -1
    diff[3, 3] = -1

    return ''.join([''.join([str(a) for a in row if a != -1]) for row in diff])


def get_string_diff(letters: str) -> str:
    """
    Wrapper for get_diff, using string representations of grids.
    """
    true_grid: ArrayLike = grid_from_grid_string(SimplifiedWaffle.goal)
    shuffled_grid: ArrayLike = grid_from_grid_string(letters)

    # print(letters)
    # print(true_grid)
    # print(shuffled_grid)

    diff: ArrayLike = get_diff(true_grid, shuffled_grid)

    return grid_string_from_grid(diff)


class SimplifiedWaffle:
    """
    A simplified version of the waffle,
    with only the letters and their "color".
    """

    goal = ""

    def __init__(self, letters: str, diff: str = "0" * 21, goal: Optional[str] = None):
        """
        :param letters: Letters of the waffle.
        :param diff: Diff of the waffle.
        :param goal: Goal of the waffle.
        """
        self.letters = letters.upper()
        if SimplifiedWaffle.goal == "":
            SimplifiedWaffle.goal = goal.upper()
            self.diff = diff
        else:
            # Determine diff from letters & goal
            self.diff = get_string_diff(self.letters)

    def __hash__(self):
        """
        :return: Hash of the waffle.
        """
        return hash(self.letters + self.diff + self.goal)

    def __str__(self):

        output = ""

        for i, letter in enumerate(self.letters):
            if self.diff[i] == "2":
                output += letter
            elif self.diff[i] == "1":
                output += YELLOW + letter + ENDC
            else:
                output += GREEN + letter + ENDC

        output += " (" + GREEN + str(self.diff.count("0")) + ENDC + ", " + \
            YELLOW + str(self.diff.count("1")) + ENDC + ", " + str(self.diff.count("2")) + ")"

        return output


def reconstruct_path(came_from: Dict[int, int], current: int,
                     links: Dict[int, SimplifiedWaffle]) -> List[SimplifiedWaffle]:
    """
    Reconstruct the path from the came_from dictionary.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return [links[w] for w in total_path if w is not None][::-1]


def heuristic(waffle: SimplifiedWaffle) -> int:
    """
    Calculate the heuristic between two simplified waffles.
    Method: Number of left letters / 2
    This assumes that every move is perfect => Always underestimates real cost.
    """
    return int((len(waffle.letters) - waffle.diff.count('0')) / 2)


def is_perfect_move(previous: SimplifiedWaffle, waffle: SimplifiedWaffle) -> bool:
    """
    Check if the move is perfect.
    """
    return waffle.diff.count('0') == 2 + previous.diff.count('0')


def neighbours(waffle: SimplifiedWaffle) -> Generator[SimplifiedWaffle, None, None]:
    """
    Return all the neighbours of a waffle (meaning only switching 2 letters).
    """
    switchable: List[Tuple[int, str]] = [(i, letter) for i, letter in enumerate(waffle.letters) if waffle.diff[i] != '0']

    for idi, (i, letter_i) in enumerate(switchable):
        for idj, (j, letter_j) in enumerate(switchable[idi + 1:]):
            if waffle.letters[i] != waffle.letters[j]:
                yield SimplifiedWaffle(waffle.letters[:i] + waffle.letters[j] + waffle.letters[i+1:j] +
                                       waffle.letters[i] + waffle.letters[j+1:],
                                       waffle.diff[:i] + waffle.diff[j] + waffle.diff[i+1:j] +
                                       waffle.diff[i] + waffle.diff[j+1:], waffle.goal)


def a_star(start: SimplifiedWaffle, goal: SimplifiedWaffle) -> List[SimplifiedWaffle]:
    links: Dict[int, SimplifiedWaffle] = {hash(start): start}
    open_set: Set[int] = {hash(start)}
    came_from: Dict[int, Optional[int]] = {hash(start): None}
    cost_so_far: Dict[int, int] = {hash(start): 0}
    f_score: Dict[int, int] = {hash(start): heuristic(start)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        open_set.remove(current)

        if current == hash(goal):
            return reconstruct_path(came_from, current, links)

        for neighbour in neighbours(links[current]):
            tentative_g_score = cost_so_far[current] + 1
            if hash(neighbour) not in cost_so_far or tentative_g_score < cost_so_far[hash(neighbour)]:
                came_from[hash(neighbour)] = current
                cost_so_far[hash(neighbour)] = tentative_g_score
                f_score[hash(neighbour)] = tentative_g_score + heuristic(neighbour)
                open_set.add(hash(neighbour))
                links[hash(neighbour)] = neighbour

                if is_perfect_move(links[current], neighbour):
                    open_set = {hash(neighbour)}
                    break

    return []


def compare_waffles(waffle_a, waffle_b):
    output = ""
    for a, b in zip(waffle_a.letters, waffle_b.letters):
        if a == b:
            output += "-"
        else:
            output += a

    return output


if __name__ == "__main__":
    start = SimplifiedWaffle("BESOLIEENIKOAREADWROR", diff="022102212202100202220", goal="BROILOAOASKEWREEDINER")
    #start = SimplifiedWaffle("CHASECGVINANELRNKENPT", diff="000001000000022001120", goal="CHASERGVINANECPNKNELT")
    goal = SimplifiedWaffle("BROILOAOASKEWREEDINER")

    result = a_star(start, goal)

    print("Solution found in {} moves.\n".format(len(result) - 1))

    for a, b in zip(result[:len(result) - 1], result[1:]):
        print(a, compare_waffles(a, b))
    print(result[-1])
