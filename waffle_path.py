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
from collections.abc import Callable
from typing import Dict, Set, List, Generator


class SimplifiedWaffle:
    """
    A simplified version of the waffle,
    with only the letters and their "color".
    """

    def __init__(self, letters: str, diff: str, goal: str):
        """
        :param letters: Letters of the waffle.
        :param diff: Diff of the waffle.
        :param goal: Goal of the waffle.
        """
        self.letters = letters
        self.diff = diff
        self.goal = goal

    def __hash__(self):
        """
        :return: Hash of the waffle.
        """
        return hash(self.letters + self.diff + self.goal)


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


def neighbours(waffle: SimplifiedWaffle) -> Generator[SimplifiedWaffle]:
    """
    Return all the neighbours of a waffle (meaning only switching 2 letters).
    """
    switchable: Dict[int, str] = {i: letter for i, letter in enumerate(waffle.letters) if waffle.diff[i] != '0'}

    for i in switchable:
        for j in switchable:
            if waffle.letters[i] != waffle.letters[j]:
                yield SimplifiedWaffle(waffle.letters[:i] + waffle.letters[j] + waffle.letters[i+1:j] +
                                       waffle.letters[i] + waffle.letters[j+1:],
                                       waffle.diff[:i] + waffle.diff[j] + waffle.diff[i+1:j] +
                                       waffle.diff[i] + waffle.diff[j+1:], waffle.goal)


def a_star(start: SimplifiedWaffle, goal: SimplifiedWaffle, h: Callable) -> List[SimplifiedWaffle]:
    links: Dict[int, SimplifiedWaffle] = {hash(start): start}
    open_set: Set[int] = {hash(start)}
    came_from: Dict[int, int] = {}
    g_score: Dict[int, int] = {hash(start): 0}
    f_score: Dict[int, int] = {hash(start): h(start)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])

        if current == hash(goal):
            return reconstruct_path(came_from, current, links)
        open_set.remove(current)

        for neighbour in neighbours(links[current]):
            tentative_g_score = g_score[current] + 1
            if hash(neighbour) not in g_score or tentative_g_score < g_score[hash(neighbour)]:
                came_from[hash(neighbour)] = current
                g_score[hash(neighbour)] = tentative_g_score
                f_score[hash(neighbour)] = tentative_g_score + h(neighbour)
                open_set.add(hash(neighbour))

    return []


if __name__ == "__main__":
    

    # a_star(SimplifiedWaffle("ABCDEFGHIJKLMNOPQRSTU", "", "ABCDEFGHIJKLMNOPQRSTU"),
    #        SimplifiedWaffle("ABCDEFGHIJKLMNOPQRSTU", "", "ABCDEFGHIJKLMNOPQRSTU"),
    #        heuristic)
