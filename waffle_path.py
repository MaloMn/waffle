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
from numpy.typing import ArrayLike
from collections.abc import Callable
from typing import Dict


def reconstruct_path(came_from: Dict[str], current: str):
    """
    Reconstruct the path from the came_from dictionary.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def heuristic(grid_a: str, grid_b: str) -> int:
    pass


def a_star(grid_a: ArrayLike, grid_b: ArrayLike, h: Callable) -> ArrayLike:
    pass


if __name__ == "__main__":
    pass
