import unittest

from Game import Game
from Card import Card
#from GUIHandler import GUIHandler

class  SETUnitTestCase(unittest.TestCase):

    testgame = Game()
    testcard = Card(0,0,0,0)

    def testCardImageNumber0(self):
        self.assertEqual(SETUnitTestCase.testcard.getCardImgNumber(),0)

    def testCardImageNumber1(self):
        SETUnitTestCase.testcard.shading = 1
        self.assertEqual(SETUnitTestCase.testcard.getCardImgNumber(),27)

    def testCardImageNumber2(self):
        SETUnitTestCase.testcard.number = 2
        self.assertEqual(SETUnitTestCase.testcard.getCardImgNumber(),29)

    def testCardImageNumber3(self):
        SETUnitTestCase.testcard.number = 3
        self.assertEqual(SETUnitTestCase.testcard.number,2)
        self.assertEqual(SETUnitTestCase.testcard.getCardImgNumber(),29)

    def testGameInstance(self):
        self.assertEqual(SETUnitTestCase.testgame.numSetsTotal,4)
        SETUnitTestCase.testgame.changeGameDifficulty(0,True)
        self.assertEqual(len(SETUnitTestCase.testgame.UseDeck),27)
        SETUnitTestCase.testgame.changeGameDifficulty(1,True)
        self.assertEqual(SETUnitTestCase.testgame.beginnerFlag,False)

if __name__ == '__main__':
    unittest.main()

