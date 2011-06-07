import Difficulty
__author__="rishi"
__date__ ="$Jun 3, 2011 1:22:13 AM$"

class Difficulty:

    UNTIMED = 4
    EASY = 3
    MEDIUM = 2
    HARD = 1

    def __init__(self):

        self.difficulty = self.UNTIMED

    def setDifficulty(self,diff):

        try:
            if diff < Difficulty.HARD or diff > Difficulty.UNTIMED:
                raise Exception
            self.difficulty = diff
        except:
            pass
    def __str__(self):
        return str(self.difficulty)