import sys
from GUIHandler import GUIHandler
from Game import Game
from ResolutionError import ResolutionError

__author__ = 'Rishi'

def run():
    try:
        g = Game()
        gh = GUIHandler(g) #Link the GUI Handler with the Game instance by wrapping the instance around the Game instance
        gh.run()
    except ResolutionError:
        sys.exit(1)
if __name__ == '__main__':
    run()