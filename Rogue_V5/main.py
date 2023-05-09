'''Main module of the game. It creates the map and starts the game.'''

import random
import lib.map

if __name__ == "__main__":
    random.seed(2)
    print("#####################")
    m = lib.map.Map()
    print(m)
    print(m._elem)
