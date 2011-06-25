import unittest

from Game import Game
from Card import Card
from GUIHandler import GUIHandler

class  SETUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.testgame = Game()
        self.testguihandler = GUIHandler(self.testgame)
        self.testcard = Card(0,0,0,0)

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testCardImageNumber(self):
        self.assertEqual(self.testcard.getCardImgNumber(),0)


if __name__ == '__main__':
    unittest.main()

