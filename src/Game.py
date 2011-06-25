__author__="rishi"
__date__ ="$Jun 7, 2011 11:15:55 PM$"

from Field import Field
from Card import Card

import itertools
import random

## Game object which performs most of the game's operations.
#
class Game(object):

    ## Game constructor
    # @param self The object pointer
    ## @var numSetsMade
    # The total number of sets the user has made so far.
    ## @var setsListTotal
    # A list of Sets the Game object maintains when it scans the field during game initialization.
    # This data field is primarily used to test the correctness of the sets from the field.
    ## @var setsMadeSoFar
    # A list that keeps track of the sets the user has made so far.
    ## @var numSetsTotal
    # The absolute total number of sets that are on the field to be found.
    ## @var cardChoices
    # A list that keeps track of the current set choices the users has made.
    # Once the user has made 3 card choices (i.e. len(cardChoices) == 3), the Game Object verifies the Set.
    ## @var BeginnersDeck
    # A Deck object which contains cards of only solid shadings (27 cards in this deck). This deck is used only in the Beginner Level
    ## @var NormalDeck
    # A Deck object which contains all possible features (81 cards in this deck). This deck is used only in the Novice and Advanced Level.
    # This deck is used by default.
    ## @var UseDeck
    # References one of the 2 decks above based on the mode the user chooses to play in.
    ## @var beginnerFlag
    # Flag that determines whether the game should be in beginner mode. gamediff cannot be 1 or 2 if beginnerFlag is True.
    ## @var gamediff
    # Difficulty of the Game itself (a.k.a. the number of cards), Beginner/Novice uses 9 cards on the field, Advanced uses 12.
    # Default difficulty is Novice. (0 = Beginner and beginnerFlag = True, 0 = Novice and beginnerFlag = False, 2 = Advanced)
    ## @var timediff
    # Determines the difficulty of timed mode.
    # Easy by default when timed mode is turned on (0 = Easy, 1 = Medium, 2 = Hard).
    # Higher difficulties means less time to find sets. Game is in untimed mode by default
    ## @var Field
    # An instance of a Field object that the Game object uses to scan for sets,
    # reference field indices for card choices, etc.
    
    def __init__(self):

        self.numSetsMade = 0
        self.numSetsTotal = 0
        self.setsListTotal = []
        self.setsMadeSoFar = []
        self.cardChoices = []
        self.BeginnersDeck = []
        self.NormalDeck = []
        self.UseDeck = self.NormalDeck
        self.beginnerFlag = False
        self.timedModeFlag = False
        self.gamediff = 0
        self.timeddiff = 0
        self.numHints = 0
        self.Field = Field(3,3+self.gamediff)

        iter = itertools.product(xrange(3), repeat=4) #Generates the novice/advanced level's deck.
        for i in iter:
            self.NormalDeck.append(Card(i[0],i[1],i[2],i[3]))
        random.shuffle(self.NormalDeck)

        iter = itertools.product(xrange(3), repeat=3) #Generates the beginner level's deck.
        for i in iter:
            self.BeginnersDeck.append(Card(i[0],i[1],i[2],0))
        random.shuffle(self.BeginnersDeck)

        self.placeCardsOnField()
        if self.scanSetsOnField() != 4 + (2 * self.gamediff):
            self.resetGame()
        self.numHints = int(not self.timedModeFlag) * (self.numSetsTotal//2) + int(self.timedModeFlag) * (self.numSetsTotal//2)

    ## resets all data for the Game, this method was created because it was
    #  preferable than having overhead with creating a brand new instance and garbage collection
    def resetGame(self):

        self.numSetsMade = 0
        self.numSetsTotal = 0
        del self.setsListTotal[:]
        del self.setsMadeSoFar[:]
        del self.cardChoices[:]

        assert len(self.setsListTotal) == 0
        assert len(self.setsMadeSoFar) == 0
        assert len(self.cardChoices) == 0

        if len(self.NormalDeck) < 81: #Case 1: The cards in the field instance were from the normal deck and are being returned to the deck.
            while len(self.Field) != 0:
                for i in self.Field.pop():
                    self.NormalDeck.append(i)
            assert len(self.NormalDeck) == 81
            random.shuffle(self.NormalDeck)
        elif len(self.BeginnersDeck) < 27: #Case 2: The cards in the field instance were from the beginner's deck and are being returned to the deck.
            while len(self.Field) != 0:
                for i in self.Field.pop():
                    self.BeginnersDeck.append(i)
            assert len(self.BeginnersDeck) == 27
            random.shuffle(self.BeginnersDeck)
        else: #Default case: There shouldn't be default case...
            assert False #Program should definitely not reach this statement
            
        self.Field.reset(3,3+self.gamediff) #reset the existing field instance rather than create a new instance (a new instance doesn't work for some reason)
        self.placeCardsOnField()
        if self.scanSetsOnField() != 4 + (2*self.gamediff):
            self.resetGame()
        
    ##Take cards from the top of the deck and place them in the (backend) field.
    #
    def placeCardsOnField(self):

        for i in range(len(self.Field.cardField)):
            for j in range(len(self.Field.cardField[0])):
                self.Field.cardField[i][j] = self.UseDeck.pop()

    ##Checks over the (backend) Field array to check all possible sets
    #
    def scanSetsOnField(self):

        rows = len(self.Field)
        cols = len(self.Field[0])
        comb = itertools.combinations(xrange(rows*cols), 3)
        for it in comb:
            i,j,k = it[0],it[1],it[2]
            c1 = self.Field[i//cols][i%cols]
            c2 = self.Field[j//cols][j%cols]
            c3 = self.Field[k//cols][k%cols]
            if self.verifySet([c1, c2, c3]) == None:
                self.setsListTotal.append([i, j, k])
        self.numSetsTotal = len(self.setsListTotal)
        return self.numSetsTotal

    ##Given a list of EXACTLY 3 Card Objects, this method checks the attributes of the cards to
    # see if the cards form a given set. If so, return 'None', if not return the 2 attributes that violate the SET rule.

    def verifySet(self,ls):

        assert len(ls) == 3
        assert type(ls[0]) == Card
        assert type(ls[1]) == Card
        assert type(ls[2]) == Card
        
        violators = None
        d1 = ls[0].__dict__
        d2 = ls[1].__dict__
        d3 = ls[2].__dict__
        for attr in Card.attrdict:
            i,j,k = d1[attr],d2[attr],d3[attr]
            violators = self._verifyHelper([i, j, k])
            if(violators != None):
                assert len(violators) == 2
                return Card.attrdict[attr][violators[0]], Card.attrdict[attr][violators[1]]
                #if the cards picked aren't a set then we return from the function.
                #We return the string attributes that violate the SET rule.

    ## A simple helper method for the verifySet function that actually checks the attributes
    #  @return A 2-length tuple of string attributes that violated the set rule, or None otherwise.
    def _verifyHelper(self,attributes):

        assert len(attributes) == 3
        if attributes[0] == attributes[1] and attributes[0] != attributes[2]:
            return (attributes[0], attributes[2])

        if attributes[1] == attributes[2] and attributes[1] != attributes[0]:
            return (attributes[1], attributes[0])

        if attributes[0] == attributes[2] and attributes[0] != attributes[1]:
            return (attributes[0], attributes[1])

    ## Primary method used for testing the validity of the current card choices.
    #  It returns one of the following: A tuple of strings indicating the attributes
    #  that violated the set rule, or an integer indicating other wise.
    #  @return (1 == Repeated Set, 2 == Successful Set, (str,str) == choices don't form a set)
    def validateSet(self):

        assert len(self.cardChoices)
        choices = [i for i in self.cardChoices] #Create a copy of the choice list
        if choices in self.setsMadeSoFar:
            return 1
        result = self.verifySet([self.Field[i//self.Field.cols()][i%self.Field.cols()] for i in self.cardChoices])
        if not result:
            self.setsMadeSoFar.append(choices)
            self.numSetsMade+=1
            assert self.numSetsMade == len(self.setsMadeSoFar)
            return 2
        else:
            return result

    ## Primary method for processing cardChoices. The length of the choice list must be less than 3 upon calling
    #  this function. If the choices passed in the function already exists in the choice list, it is removed.
    #  If the choices list hasn't reached 3 yet, returns 0. Otherwise, we call the validateSet() method and return
    #  the method's return value.
    #  @return (0 == Pending (choice list hasn't reached length 3 yet), and the return values from validateSet() are also used, 3 == choices to be removed from set.)
    def addCardChoice(self,i):

        assert len(self.cardChoices) < 3
        if i in self.cardChoices:
            self.cardChoices.remove(i)
            return 3
        else:
            self.cardChoices.append(i)
            if len(self.cardChoices) == 3:
                try:
                    self.cardChoices.sort()
                    return self.validateSet() #returns None if Set is valid, A tuple of card attributes otherwise.
                finally:
                    del self.cardChoices[:]
        return 0

    ##Sets the game difficulty of the current game.
    # Returns True if the difficulty change was successful, False if it wasn't.
    def changeGameDifficulty(self,i,f):
        if (self.gamediff == i and self.beginnerFlag == f):
            return False
        assert i >= -1 and i < 2

        self.gamediff = i
        self.beginnerFlag = f
        self.UseDeck = self.BeginnersDeck if f else self.NormalDeck
        return True

    def numSetsRemaining(self):

        return self.numSetsTotal-self.numSetsMade