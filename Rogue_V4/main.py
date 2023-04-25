'''Main module of the game. It creates the map and starts the game.'''

from lib.map import Map
from lib.element import Element
from lib.creature import Creature
from lib.coord import Coord
from lib.hero import Hero
import random

if __name__ == "__main__":
    random.seed(42)
    m = Map()
    m.put(Coord(7,4),Hero())
    print(m)
