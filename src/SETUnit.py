import unittest

from Game import Game
from Card import Card
from GUIHandler import GUIHandler

class  SETUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.testgame = Game()
        self.testguihandler = GUIHandler(self.testgame)
        self.testcard = Card(0,0,0,0)

    def testCardImageNumber(self):
        self.assertEqual(self.testcard.getCardImgNumber(),0)
        self.testcard.shading = 1
        self.assertEqual(self.testcard.getCardImgNumber(),27)
        self.testcard.number = 2
        self.assertEqual(self.testcard.getCardImgNumber(),29)
        self.testcard.number = 3
        self.assertEqual(self.testcard.number,2)
        self.assertEqual(self.testcard.getCardImgNumber(),29)




if __name__ == '__main__':
    unittest.main()

