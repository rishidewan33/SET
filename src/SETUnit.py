import unittest

from Game import Game
from Card import Card
from GUIHandler import GUIHandler

class  SETUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.testgame = Game()
        #self.testguihandler = GUIHandler(self.testgame)
        self.testcard = Card(0,0,0,0)

    def testCardImageNumber0(self):
        self.assertEqual(self.testcard.getCardImgNumber(),0)

    def testCardImageNumber1(self):
        self.testcard.shading = 1
        self.assertEqual(self.testcard.getCardImgNumber(),27)

    def testCardImageNumber2(self):
        self.testcard.number = 2
        self.assertEqual(self.testcard.getCardImgNumber(),29)

    def testCardImageNumber3(self):
        self.testcard.number = 3
        self.assertEqual(self.testcard.number,2)
        self.assertEqual(self.testcard.getCardImgNumber(),29)

    def testGameInstance(self):
        self.assertEqual(self.testgame.numSetsTotal,4)
        self.assertEqual(self.testgame.numSetsTotal,4)
        self.assertEqual(self.testgame.numSetsTotal,4)
        self.testgame.changeGameDifficulty(0,True)
        self.assertEqual(len(self.testgame.UseDeck),27)
        self.testgame.changeGameDifficulty(1,True)
        self.assertEqual(self.testgame.beginnerFlag,False)


if __name__ == '__main__':
    unittest.main()

