__author__="rishi"
__date__ ="$Jun 7, 2011 11:15:55 PM$"

from Field import Field
from Card import Card
from Difficulty import Difficulty
from DeckManager import DeckManager
from HintErrorCode import HintErrorCode

import itertools

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
    # Once the user has made 3 card choices (i.e. len(_cardChoices) == 3), the Game Object verifies the Set.
    ## @var deckManager
    # Object which manages the use of the Beginner sized deck and the Normal size deck in gameplay.
    ## @var timerModeFlag
    # Boolean that determines whether the game should be run in timed mode.
    ## @var gamediff
    # Difficulty of the Game itself (a.k.a. the number of cards), Beginner/Novice uses 9 cards on the field, Advanced uses 12.
    # Default difficulty is Novice. (0 = Beginner and _beginnerFlag = True, 0 = Novice and _beginnerFlag = False, 2 = Advanced)
    ## @var timediff
    # Determines the difficulty of timed mode.
    # Easy by default when timed mode is turned on (0 = Easy, 1 = Medium, 2 = Hard).
    # Higher difficulties means less time to find sets. Game is in untimed mode by default
    ## @var numHints
    # Number of hints allotted to the user whenever a new game is started.
    ## @var field
    # An instance of a _Field object that the Game object uses to scan for sets,
    # reference field indices for card choices, etc.

    def __init__(self):

        self.numSetsMade = 0
        self.numSetsTotal = 0
        self.setsListTotal = []
        self.setsMadeSoFar = []
        self.cardChoices = []
        self.deckManager = DeckManager()
        self.timedModeFlag = False
        self.gamediff = Difficulty.NOVICE
        self.timeddiff = 0
        self.numHints = 3 if self.gamediff == Difficulty.ADVANCED else 2
        self.field = Field(3,4) if self.gamediff == Difficulty.ADVANCED else Field(3,3)

        self.deckManager.placeCardsOnField(self.field)
        if self.scanSetsOnField() != 4 + (2 if self.gamediff == Difficulty.ADVANCED else 0):
            self.resetGame()

    ## resets all data for the Game, this method was created because it was
    #  preferable than having overhead with creating a brand new instance and garbage collection
    #  If the number of sets found during the scan doesn't satisfy the required number of sets,
    #  redo the reset.
    # @param self The object pointer
    def resetGame(self):

        while True:
            self.numSetsMade = 0
            self.numSetsTotal = 0
            self.numHints = 3 if self.gamediff == Difficulty.ADVANCED else 2
            del self.setsListTotal[:]
            del self.setsMadeSoFar[:]
            del self.cardChoices[:]

            self.deckManager.collectCardsFromField(self.field)
            self.field.reset(3,3+(1 if self.gamediff == Difficulty.ADVANCED else 0)) #reset the existing field instance rather than create a new instance (a new instance doesn't work for some reason)
            self.deckManager.placeCardsOnField(self.field)
            
            if self.scanSetsOnField() == 4 + (2 if self.gamediff == Difficulty.ADVANCED else 0):
                break

    ##Checks over the field array to check all possible sets
    # @param self The object pointer
    # @return The number of sets found during the scan.
    def scanSetsOnField(self):

        rows = len(self.field)
        cols = len(self.field[0])
        for it in itertools.combinations(xrange(rows*cols), 3):
            i,j,k = it[0],it[1],it[2]
            c1 = self.field[i//cols][i%cols]
            c2 = self.field[j//cols][j%cols]
            c3 = self.field[k//cols][k%cols]
            if not self.verifySet([c1, c2, c3]):
                self.setsListTotal.append([i, j, k])
                if len(self.setsListTotal) == 4 + (2 if self.gamediff == Difficulty.ADVANCED else 0):
                    break
        self.numSetsTotal = len(self.setsListTotal)
        return self.numSetsTotal

    ##Given a list of EXACTLY 3 Card Objects, this method checks the attributes of the cards to
    # see if the cards form a given set. If so, return 'None', if not return the 2 attributes that violate the SET rule.
    # @param self The object pointer
    # @param ls The list of Card Objects (of length 3) whose attributes may or may not form a set.
    # @return None if the cards in the list form a set.
    # @return a 2-length tuple of string attributes that violate the set rule.
    def verifySet(self,ls):

        assert len(ls) == 3
        assert type(ls[0]) == Card
        assert type(ls[1]) == Card
        assert type(ls[2]) == Card
        
        d1 = ls[0].__dict__
        d2 = ls[1].__dict__
        d3 = ls[2].__dict__
        for attr in Card.attrdict:
            i,j,k = d1[attr],d2[attr],d3[attr]
            violators = self._verifyHelper([i, j, k])
            if violators:
                assert len(violators) == 2
                return Card.attrdict[attr][violators[0]], Card.attrdict[attr][violators[1]]
                #if the cards picked aren't a set then we return from the function.
                #We return the string attributes that violate the SET rule.

    ## A simple helper method for the verifySet function that actually checks the attributes
    #  @param A 3-length list of set attributes to determine if they violate the set rule of not
    #  @return A 2-length tuple of string attributes that violated the set rule, or None otherwise.
    def _verifyHelper(self,attributes):

        assert len(attributes) == 3
        if attributes[0] == attributes[1] and attributes[0] != attributes[2]:
            return attributes[0], attributes[2]

        if attributes[1] == attributes[2] and attributes[1] != attributes[0]:
            return attributes[1], attributes[0]

        if attributes[0] == attributes[2] and attributes[0] != attributes[1]:
            return attributes[0], attributes[1]

    ## Primary method used for testing the validity of the current card choices.
    #  It returns one of the following: A tuple of strings indicating the attributes
    #  that violated the set rule, or an integer indicating other wise.
    #  @return (1 == Repeated Set, 2 == Successful Set, (str,str) == choices don't form a set)
    def validateSet(self):

        assert len(self.cardChoices)
        choices = [i for i in self.cardChoices]
        if choices in self.setsMadeSoFar:
            return 1
        result = self.verifySet([self.field[i//self.field.cols()][i%self.field.cols()] for i in self.cardChoices])
        if not result:
            self.setsMadeSoFar.append(choices)
            self.numSetsMade+=1
            assert self.numSetsMade == len(self.setsMadeSoFar)
            return 2
        else:
            return result

    ## Primary method for processing _cardChoices. The length of the choice list must be less than 3 upon calling
    #  this function. If the choices passed in the function already exists in the choice list, it is removed.
    #  If the choices list hasn't reached 3 yet, returns 0. Otherwise, we call the validateSet() method and return
    #  the method's return value.
    #  @param self The object pointer
    #  @param i the card id on the field to be added to the card choices.
    #  @return 0 if the choice list hasn't reached length 3 yet
    #  @return 3 if a choice is to be removed from set.)
    #  @return a result from self.validateSet()
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
    def changeGameDifficulty(self,difficulty):
        if self.gamediff == difficulty:
            return False
        if self.gamediff != difficulty:
            if self.gamediff == Difficulty.BEGINNER or difficulty == Difficulty.BEGINNER:
                self.deckManager.collectCardsFromField(self.field)
                self.deckManager.switchDecks()
        self.gamediff = difficulty
        return True

    ##Helper method which calculates the numbers of sets remaining to find.
    # @param self The Object Pointer
    # @return The number of sets remaining on the field, or a negative number representing an error number.

    def callHint(self):
        if not self.numSetsRemaining():
            return HintErrorCode.GAMEOVER
        if not self.numHints:
            return HintErrorCode.OUTOFHINTS
        result = set(map(tuple,self.setsListTotal)) - set(map(tuple,self.setsMadeSoFar))
        if len(result) == 1:
            return HintErrorCode.LASTSET
        result2 = set(result.pop()) - set(self.cardChoices)
        self.numHints-=1
        return result2.pop()
        #Complex function to choose a card on the field that's in a set that hasn't been made yet.
        #A shame that sets aren't indexable...or that you can't have a set of lists...

    def numSetsRemaining(self):

        return self.numSetsTotal-self.numSetsMade