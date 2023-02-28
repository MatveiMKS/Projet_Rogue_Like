'''Main module of the game. It creates the map and starts the game.'''

from map import Map
from coord import Coord

if __name__ == "__main__":
    carte = Map(3, Coord(2,1))
    carte.play()
    