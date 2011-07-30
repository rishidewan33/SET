import unittest

from Game import Game
from Card import Card
#from GUIHandler import GUIHandler
from Difficulty import Difficulty

class  SETUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.testgame = Game()

    #Test Card Class Functionality
    def testCardImageNumber0(self):
        testCard = Card(0,0,0,0)
        self.assertEqual(testCard.getCardImgNumber(),0)

    def testCardImageNumber1(self):
        testCard = Card(1,0,0,0)
        self.assertEqual(testCard.getCardImgNumber(),27)

    def testCardImageNumber2(self):
        testCard = Card(1,0,0,2)
        self.assertEqual(testCard.getCardImgNumber(),29)

    def testCardImageNumber3(self):
        testCard = Card(1,2,0,0)
        testCard.number = 3
        self.assertEqual(testCard.number,0)
        self.assertEqual(testCard.getCardImgNumber(),45)

    def testCardImageNumber4(self):

        tempCard = Card(2,2,2,2)
        self.assertEqual(tempCard.getCardImgNumber(),80)

    #Test Game Functionality
    def testChangeToNovice(self):
        self.assertEqual(self.testgame.numSetsTotal,4)

        self.assertEqual(self.testgame.changeGameDifficulty(Difficulty.NOVICE),False)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.deckManager.normalDeck.deck),72)
        self.assertEqual(len(self.testgame.deckManager.beginnerDeck.deck),27)
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testChangeToBeginner(self):
        self.assertEqual(self.testgame.changeGameDifficulty(Difficulty.BEGINNER),True)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.deckManager.normalDeck.deck),81)
        self.assertEqual(len(self.testgame.deckManager.beginnerDeck.deck),18)
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testChangeToAdvanced(self):
        self.assertEqual(self.testgame.changeGameDifficulty(Difficulty.ADVANCED),True)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.deckManager.normalDeck.deck),69)
        self.assertEqual(len(self.testgame.deckManager.beginnerDeck.deck),27)
        self.assertEqual(self.testgame.numSetsTotal,6)

    def testNumberOfSetsGenerated1(self):
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testNumberOfSetsGenerated2(self):
        self.testgame.changeGameDifficulty(Difficulty.ADVANCED)
        self.testgame.resetGame()
        self.assertEqual(self.testgame.numSetsTotal,6)

if __name__ == '__main__':
    unittest.main()

