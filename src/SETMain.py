from GUIHandler import GUIHandler
from Game import Game

__author__ = 'Rishi'

def run():
    g = Game()
    gh = GUIHandler(g)
    gh.run()

if __name__ == '__main__':
    run()