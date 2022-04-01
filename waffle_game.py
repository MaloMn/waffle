from waffle import Waffle


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
