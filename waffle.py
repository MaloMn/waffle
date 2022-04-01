import random
import copy
from utils import load_data, words_to_grid, check_grid, grid_path_generator, get_diff
from colors import color_text, GREEN, YELLOW, ENDC
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from numpy.typing import ArrayLike


class Waffle:

    """
    Represents a Waffle, meaning it contains the words to be found in the grid.
    It also handles shuffling the grid, and swapping letters.
    """

    def __init__(self):
        self.data:          List[str] = load_data()
        self.chosen_words:  List[str] = ['', '', '', '', '', '']
        self.true_grid:     ArrayLike = np.empty((5, 5), dtype=str)
        self.shuffled_grid: ArrayLike = np.empty((5, 5), dtype=str)
        # 0 if correctly placed, 1 if in same line/column, 2 else
        self.diff:          ArrayLike = np.empty((5, 5), dtype=int)

        # Making up a new grid
        self.new_waffle_grid()

    def build_waffle_grid(self, word_index: int) -> bool:
        """
        Building a waffle grid recursively with backtracking
        """
        # Ending condition
        if '' not in self.chosen_words:
            return True

        for word in self.data:
            # See if word fits
            option = self.chosen_words[:]
            option[word_index] = word
            if check_grid(option, word_index):
                # Word fits, try next word
                self.chosen_words[word_index] = word
                if self.build_waffle_grid(word_index + 1):
                    return True
                self.chosen_words[word_index] = ''

        # No word fits, backtrack
        return False

    def new_waffle_grid(self) -> None:
        """
        Uses recursive method build_waffle_grid to build a new grid.
        Also fills self.true_grid and self.shuffled_grid.
        :return: None
        """
        random.shuffle(self.data)
        for i in range(len(self.data)):
            self.chosen_words = ['', '', '', '', '', '']
            if self.build_waffle_grid(i):
                self.true_grid = words_to_grid(self.chosen_words)
                self.shuffle_grid()
                return

    def load_waffle(self, words: List[str]) -> None:
        self.chosen_words = words
        self.true_grid = words_to_grid(words)
        self.shuffle_grid()

    def shuffle_grid(self, nb: int = 10, detail: bool = True    ) -> None:
        """
        Make nb swaps between letters of the grid.
        :param nb: Number of swaps
        :param detail: enables printing of initial and shuffled grids
        :return: None
        """
        self.shuffled_grid = copy.deepcopy(self.true_grid)
        # Not every letters can be swapped
        possible_switch_indexes = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 4), (2, 0), (2, 1),
                                   (2, 3), (2, 4), (3, 0), (3, 2), (3, 4), (4, 1), (4, 2), (4, 3)]

        for _ in range(nb):
            # Randomly swap letters two by two, leaving corners and center letters untouched
            a, b = random.choices(possible_switch_indexes, k=2)
            self.shuffled_grid[a], self.shuffled_grid[b] = self.shuffled_grid[b], self.shuffled_grid[a]

        self.diff = get_diff(self.true_grid, self.shuffled_grid)

        if detail:
            print("Initial grid: ", self.true_grid)
            print("Shuffled grid: ", self.shuffled_grid)

    def __str__(self):
        print(self.diff)
        output = copy.deepcopy(self.shuffled_grid).tolist()

        # To handle words containing twice or more the same letter, a reference is built
        # and letters are removed from that reference when they are used
        ref = copy.deepcopy(self.true_grid)

        for x, y in grid_path_generator(5):
            letter = self.shuffled_grid[x, y]

            if self.diff[x, y] == 0:
                output[x][y] = GREEN + letter + ENDC
            elif self.diff[x, y] == 1:
                output[x][y] = YELLOW + letter + ENDC
            else:
                output[x][y] = letter

        return '\n'.join([' '.join(output[x]) for x in range(5)])


if __name__ == '__main__':
    waffle = Waffle()
    print(waffle)
