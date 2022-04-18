"""
Once the words of the waffle have been determined,
a path towards this solution in a minimal number
of moves is needed.

I decide to use a version of the A* algorithm to tackle this problem.
Main source: https://en.wikipedia.org/wiki/A*_search_algorithm
"""
from numpy.typing import ArrayLike


def reconstruct_path(came_from, current):
    """
    Reconstruct the path from the came_from dictionary.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def heuristic(grid_a: ArrayLike, grid_b: ArrayLike) -> int:
    pass

