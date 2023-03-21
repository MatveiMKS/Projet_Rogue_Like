'''Main module of the game. It creates the map and starts the game.'''

from map import Map
from coord import Coord
from element import Element
from creature import Creature

if __name__ == "__main__":
    m = Map(10)
    m.put(Coord(6, 3), Creature("Goblin", 5, strength=3))
    m.put(Coord(0, 4), Creature("Snake", 5))
    m.put(Coord(7, 7), Creature("Snake", 5))
    m.put(Coord(6, 8), Element("gold", "o"))
    m.put(Coord(4, 8), Element("gold", "o"))
    m.play()
