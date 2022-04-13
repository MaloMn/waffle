from waffle import Waffle
import numpy as np
from numpy.typing import ArrayLike
from typing import List, Set


class WaffleSolver:

    def __init__(self, waffle: Waffle):
        self.waffle = waffle
        self.constraints = None

    def solve(self):
        self.constraints = words_constraints(self.waffle, details=True)


def words_constraints(waffle: Waffle, details: bool = False) -> List[List[Set[str]]]:
    constraints: List[List[Set[str]]] = [[set() for i in range(5)] for i in range(5)]

    green = np.where(waffle.diff == 2)
    orange = np.where(waffle.diff == 1)
    black = np.where(waffle.diff == 0)

    # Add orange letters on their respective lines and/or columns
    for x, y in list(zip(*orange)):
        letter = waffle.shuffled_grid[x, y]

        if letter == ' ':
            continue

        # Add letter on its column
        if x % 2 == 0:
            for i in range(5):
                if i != y:
                    constraints[i][y].add(letter)

        # Add letter on its line
        if y % 2 == 0:
            for i in range(5):
                if i != x:
                    constraints[x][i].add(letter)

    # Add black letters to other lines/columns
    for x, y in list(zip(*black)):
        # 1. Gather all positions
        positions = [(x, y) for x in range(5) for y in range(5)]
        # Remove column positions
        if x % 2 == 0:
            for i in range(5):
                if (x, i) not in positions:
                    positions.remove((x, i))

        # Remove line positions
        if y % 2 == 0:
            for i in range(5):
                if (i, y) not in positions:
                    positions.remove((i, y))

        # Now that positions have been curated, we add the letter to the constraints
        for i, j in positions:
            constraints[i][j].add(letter)

    # Set letters that are right
    for x, y in list(zip(*green)):
        constraints[x][y] = set(letter)

    if details:
        print(constraints)

    return constraints


if __name__ == "__main__":
    waffle = Waffle(words=['impel', 'input', 'weigh', 'hutch', 'filth', 'whiff'],
                    shuffle=['eipit', 'iepmn', 'wtech', 'hlnuh', 'fhtgh', 'wuiff'])
    print(waffle)

    solver = WaffleSolver(waffle)
    solver.solve()
