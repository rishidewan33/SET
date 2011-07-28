import unittest

from Game import Game
from Card import Card
#from GUIHandler import GUIHandler
from Difficulty import Difficulty

class  SETUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.testgame = Game()
        self.testcard = Card(0,0,0,0)

    def testCardImageNumber0(self):
        self.assertEqual(self.testcard.getCardImgNumber(),0)

    def testCardImageNumber1(self):
        self.testcard.shading = 1
        self.assertEqual(self.testcard.getCardImgNumber(),27)

    def testCardImageNumber2(self):
        self.testcard.shading = 1
        self.testcard.number = 2
        self.assertEqual(self.testcard.getCardImgNumber(),29)

    def testCardImageNumber3(self):
        self.testcard.shading = 1
        self.testcard.shape = 2
        self.testcard.number = 3
        self.assertEqual(self.testcard.number,0)
        self.assertEqual(self.testcard.getCardImgNumber(),45)

    def testChangeToNovice(self):
        self.assertEqual(self.testgame.numSetsTotal,4)

        self.testgame.changeGameDifficulty(Difficulty.NOVICE)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.NormalDeck),72)
        self.assertEqual(len(self.testgame.BeginnersDeck),27)
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testChangeToBeginner(self):
        self.testgame.changeGameDifficulty(Difficulty.BEGINNER)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.NormalDeck),81)
        self.assertEqual(len(self.testgame.BeginnersDeck),18)
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testChangeToAdvanced(self):
        self.testgame.changeGameDifficulty(Difficulty.ADVANCED)
        self.testgame.resetGame()
        self.assertEqual(len(self.testgame.NormalDeck),69)
        self.assertEqual(len(self.testgame.BeginnersDeck),27)
        self.assertEqual(self.testgame.numSetsTotal,6)

    def testNumberOfSetsGenerated1(self):
        self.assertEqual(self.testgame.numSetsTotal,4)

    def testNumberOfSetsGenerated2(self):
        self.testgame.changeGameDifficulty(Difficulty.ADVANCED)
        self.testgame.resetGame()
        self.assertEqual(self.testgame.numSetsTotal,6)

if __name__ == '__main__':
    unittest.main()

