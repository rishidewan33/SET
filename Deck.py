__author__="rishi"
__date__ ="$Jun 3, 2011 2:09:50 AM$"

"""making the Deck for the Sets game (Which is just a list of 81 Card Objects)"""

from Card import Card
import random

class Deck:

    def __init__(self):

        self.dk = []
        color = ['Red', 'Purple', 'Green']
        shape = ['Squiggle', 'Diamond', 'Oval']
        number = [1, 2, 3]
        shading = ['Solid', 'Stripped', 'Open']
        imgnum = 1
        for i in shading:
            for j in shape:
                for k in color:
                    for l in number:
                        self.dk.append(Card(i, j, k, l, imgnum))
                        imgnum += 1
        random.shuffle(self.dk) #shuffle the deck

    def shuffleDeck(self):
        random.shuffle(self.dk)