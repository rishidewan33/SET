__author__="rishi"
__date__ ="$Jun 4, 2011 9:39:27 PM$"

if __name__ == "__main__":
    print "Hello World"

import itertools
from Tkinter import Label
from Tkinter import Button
from Tkinter import Toplevel

class Game:

    """
    This class contains game data which helps keeps track of the user status in the game.
    """
    _cardFields = ['color','shading','shape','number']

    def __init__(self):
        self.numSetsAcquired = 0
        self.setsAcquired = []

    def new_game(self):

        self.numSetsAcquired = 0
        self.setsAcquired = []
        self.visited = []

    def addSetMade(self, ls):
        self.setsAcquired.append(ls)
        self.numSetsAcquired += 1

    def getSetsAcquired(self):
        return self.setsAcquired

    def getNumSetsAcquired(self):
        return self.numSetsAcquired

    def setExists(self, ls):
        ls.sort()
        if ls in self.setsAcquired:
            return True
        else:
            return False

    """Checks the field for possible sets"""

    def checkFieldForSets(self, Field):
        self.visited = []
        possiblesets = 0
        comb = itertools.combinations(xrange(12), 3)
        for it in comb:
            i,j,k = it[0],it[1],it[2]
            c1 = Field.getCardAt(i // 4, i % 4)
            c2 = Field.getCardAt(j // 4, j % 4)
            c3 = Field.getCardAt(k // 4, k % 4)
            if self.checkSet(c1, c2, c3) == None:
                self.visited.append([i, j, k])
                possiblesets += 1
        return possiblesets

    def checkSet(self, c1, c2, c3): #Non-Printing version of isSet used for checking

        violators = None
        iter1 = [c1.__dict__[i] for i in Game._cardFields]
        iter2 = [c2.__dict__[i] for i in Game._cardFields]
        iter3 = [c3.__dict__[i] for i in Game._cardFields]
        for i, j, k in zip(iter1,iter2,iter3):
            violators = self.isSetHelper([i, j, k])
            if(violators != None):
                return violators
        return violators #violators = None

    def isSet(self, c1, c2, c3, root):

        violators = self.checkSet(c1, c2, c3)
        if violators != None: #If the chosen cards don't form a set, then we must display a popup indicating so and why.
            failed = Toplevel(root)
            failed.title('Not a set')
            failed.geometry('300x50-550+300')
            failed.focus_set()
            Label(failed, text='This is not a set because\n2 are ' + violators[0] + ' and 1 is ' + violators[1] + '.').pack()
            Button(failed, text="OK", command=failed.destroy).pack()
            failed.bind("<Return>", lambda e:failed.destroy())
            root.wait_window(failed)
            return False
        return True

    def isSetHelper(self,col):

        if col[0] == col[1] and col[0] != col[2]:
            return (col[0], col[2])

        if col[1] == col[2] and col[1] != col[0]:
            return (col[1], col[0])

        if col[0] == col[2] and col[0] != col[1]:
            return (col[0], col[1])