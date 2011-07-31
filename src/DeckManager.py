__author__ = 'Rishi'

from Card import Card
import random, itertools

class DeckManager:

    def __init__(self):

        self.beginnerDeck = BeginnerDeck()
        self.normalDeck = NormalDeck()
        self.currentDeck = self.normalDeck

    def collectCardsFromField(self,field):
        
            while len(field):
                for i in field.pop():
                    self.currentDeck.addCard(i)
            self.shuffleDeck()

    def switchDecks(self):
        if id(self.currentDeck) == id(self.beginnerDeck):
            self.currentDeck = self.normalDeck
        else:
            self.currentDeck = self.beginnerDeck

    def pop(self):
        return self.currentDeck.takeTopCard()

    ##Take cards from the top of the deck and place them in the (backend) field.
    # @param self The object pointer
    def placeCardsOnField(self,field):

        for i in range(len(field)):
            for j in range(len(field[0])):
                field[i][j] = self.currentDeck.takeTopCard()

    def shuffleDeck(self):

        self.currentDeck.shuffle()

class Deck(object):

    def __init__(self):

        self.deck = []
        if self.__class__ == Deck:
            raise NotImplementedError("Deck is abstract")

    def takeTopCard(self):

        return self.deck.pop()

    def addCard(self, card):

        assert type(card) == Card
        self.deck.append(card)

    def shuffle(self):

        random.shuffle(self.deck)

class NormalDeck(Deck):

    def __init__(self):

        Deck.__init__(self)
        iter = itertools.product(xrange(3), repeat=4) #Generates the novice/advanced level's deck.
        for i in iter:
            self.deck.append(Card(i[0],i[1],i[2],i[3]))
        random.shuffle(self.deck)

class BeginnerDeck(Deck):

    def __init__(self):

        Deck.__init__(self)
        iter = itertools.product(xrange(3), repeat=3) #Generates the beginner level's deck.
        for i in iter:
            self.deck.append(Card(0,i[0],i[1],i[2]))
        random.shuffle(self.deck)
