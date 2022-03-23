"""
A Waffle Game solver
"""

import random
from colors import *


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


class WaffleGame:
    def __init__(self):
        self.words = load_data()
        self.waffle = ['', '', '', '', '', '']

    def build_waffle_grid(self, word_index):
        """
        Building a waffle grid recursively with backtracking
        """
        # Ending condition
        if '' not in self.waffle:
            return True

        for word in self.words:
            # See if word fits
            option = self.waffle[:]
            option[word_index] = word
            if check_grid(option, word_index):
                # Word fits, try next word
                self.waffle[word_index] = word
                if self.build_waffle_grid(word_index + 1):
                    return True
                self.waffle[word_index] = ''

        # No word fits, backtrack
        return False

    def new_waffle_grid(self):
        while True:
            self.waffle = ['', '', '', '', '', '']
            random.shuffle(self.words)
            if self.build_waffle_grid(0):
                self.print_true_waffle()
                break
            else:
                print("No solution found")

    def print_true_waffle(self):
        print("{}\n{}   {}   {}\n{}\n{}   {}   {}\n{}".format(' '.join(list(self.waffle[2])), self.waffle[5][1],
                                                              self.waffle[0][1], self.waffle[3][1],
                                                              ' '.join(list(self.waffle[1])), self.waffle[5][3],
                                                              self.waffle[0][3], self.waffle[3][3],
                                                              ' '.join(list(self.waffle[4]))))


if __name__ == "__main__":
    w = WaffleGame()
    w.new_waffle_grid()
    print(w.waffle)
