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
            # TODO Re-use the function to determine diff from letters & goal
            self.diff = diff

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
                     link: Dict[int, SimplifiedWaffle]) -> List[SimplifiedWaffle]:
    """
    Reconstruct the path from the came_from dictionary.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return [link[w] for w in total_path]


def heuristic(waffle: SimplifiedWaffle) -> int:
    """
    Calculate the heuristic between two simplified waffles.
    Method: Number of left letters / 2
    This assumes that every move is perfect => Always underestimates real cost.
    """
    return int((len(waffle.letters) - waffle.diff.count('0')) / 2)


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
    came_from: Dict[int, int] = {}
    g_score: Dict[int, int] = {hash(start): 0}
    f_score: Dict[int, int] = {hash(start): heuristic(start)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])

        if current == hash(goal):
            return reconstruct_path(came_from, current, links)
        open_set.remove(current)

        print(links[current], "has {} neighbours".format(len(list(neighbours(links[current])))))

        print("\n => ".join([n.__str__() for n in list(neighbours(links[current]))]))

        for neighbour in neighbours(links[current]):
            tentative_g_score = g_score[current] + 1
            if hash(neighbour) in g_score and tentative_g_score < g_score[hash(neighbour)]:
                came_from[hash(neighbour)] = current
                g_score[hash(neighbour)] = tentative_g_score
                f_score[hash(neighbour)] = tentative_g_score + heuristic(neighbour)
                open_set.add(hash(neighbour))

    return []


# Conversion functions below
def grid_from_grid_string(grid: str) -> ArrayLike:
    pass


def grid_string_from_grid(diff: ArrayLike) -> str:
    pass


def get_string_diff(waffle: SimplifiedWaffle) -> str:
    """
    Wrapper for get_diff, using string representations of grids.
    """

    true_grid: ArrayLike = grid_from_grid_string(SimplifiedWaffle.goal)
    shuffled_grid: ArrayLike = grid_from_grid_string(waffle.letters)
    diff: ArrayLike = get_diff(true_grid, shuffled_grid)

    return grid_string_from_grid(diff)


if __name__ == "__main__":
    start = SimplifiedWaffle("CNNSECVGNEAPLERAKINHT", diff="022001221102222202120", goal="ABCDEFGHIJKLMNOPQRSTU")
    goal = SimplifiedWaffle("CHASERGVINANECPNKNELT")

    print(start)

    print(a_star(start, goal))
