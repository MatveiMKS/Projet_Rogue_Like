'''Main module of the game. It creates the map and starts the game.'''

from lib.map import Map
from lib.element import Element
from lib.creature import Creature
from lib.coord import Coord
from lib.hero import Hero
import random

if __name__ == "__main__":

    #test d'appel de checkCoord/CheckElement dans les méthodes
    random.seed(42)
    m = Map()
    m.checkCoord = lambda x : print("Check coord: " + str(x))
    m.checkElement = lambda x : print("Check element: " + str(x))
    m.get(Coord(0,0))
    m.put(Coord(4,1), Element("."))
    m.rm(Coord(4,1))
    m.pos(m._hero)
