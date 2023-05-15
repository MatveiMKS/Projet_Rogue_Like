'''Main module of the game. It creates the map and starts the game.'''

import random
from lib.map import Map

if __name__ == "__main__":
    random.seed(2)
    print("#####################")
    m = Map()
    print(m)
    print(m._elem)
