"""
A Waffle Game solver
"""

import random
from colors import *
import copy


def load_data():
    with open("words.txt") as f:
        return [w.upper() for w in f.read().splitlines()]


def check_grid(choices, index):
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


def words_to_grid(words):
    return [list(words[2]), [words[5][1], ' ', words[0][1], ' ', words[3][1]], list(words[1]),
            [words[5][3], ' ', words[0][3], ' ', words[3][3]], list(words[4])]


class WaffleGame:
    def __init__(self):
        self.waffle = Waffle()
        print(self.waffle)
        self.moves = 15

    def switch(self, x, y):
        self.waffle.switch(x, y)
        print(self.waffle)
        self.moves -= 1
        if self.moves <= 0:
            print("You lose!")
            exit()


class Waffle:

    def __init__(self):
        self.words = load_data()
        self.chosen_words = ['', '', '', '', '', '']
        self.true_grid = []
        self.shuffled_grid = []

        if self.new_waffle_grid():
            self.true_grid = words_to_grid(self.chosen_words)

        self.shuffle_grid()

    def build_waffle_grid(self, word_index):
        """
        Building a waffle grid recursively with backtracking
        """
        # Ending condition
        if '' not in self.chosen_words:
            return True

        for word in self.words:
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

    def new_waffle_grid(self):
        random.shuffle(self.words)
        for i in range(len(self.words)):
            self.chosen_words = ['', '', '', '', '', '']
            if self.build_waffle_grid(i):
                return True

    def load_waffle(self, words):
        self.chosen_words = words
        self.true_grid = words_to_grid(words)
        self.shuffled_grid = self.true_grid[:]

    def shuffle_grid(self, nb=15):
        self.shuffled_grid = copy.deepcopy(self.true_grid)
        possible_switch_indexes = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 4), (2, 0), (2, 1), (2, 3), (2, 4),
                                   (3, 0), (3, 2), (3, 4), (4, 1), (4, 2), (4, 3)]
        for i in range(nb):
            # Switch randomly letters two by two, leaving corners and center letters untouched
            a = random.choice(possible_switch_indexes)
            b = random.choice(possible_switch_indexes)
            self.shuffled_grid[a[0]][a[1]], self.shuffled_grid[b[0]][b[1]] = self.shuffled_grid[b[0]][b[1]], \
                                                                             self.shuffled_grid[a[0]][a[1]]
        print("Initial grid: ", self.true_grid)
        print("Shuffled grid: ", self.shuffled_grid)

    def __str__(self):
        letters = copy.deepcopy(self.shuffled_grid)
        for x in range(5):
            for y in range(5):
                letter = letters[x][y]
                if self.true_grid[x][y] == letter:
                    letters[x][y] = color_text(GREEN, letter)
                elif x % 2 == 1 and y % 2 == 0:
                    # Located in lines 1 and 3
                    if letter in [self.true_grid[b][y] for b in range(4)]:
                        letters[x][y] = color_text(YELLOW, letter)
                elif x % 2 == 0 and y % 2 == 1:
                    # Located in columns 1 and 3
                    if letter in self.true_grid[x]:
                        letters[x][y] = color_text(YELLOW, letter)

                    # TODO Find condition to check if letter is in orange
                    # Has to take into account that two similar letters
                    # are both orange if word contains twice this letter

        return '\n'.join([' '.join(letters[x]) for x in range(5)])


class WaffleSolver:
    def __init__(self, waffle):
        self.waffle = waffle

    def minimum_moves(self):
        pass

    def solve(self):
        pass


if __name__ == "__main__":
    w = WaffleGame()
