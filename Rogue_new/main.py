'''Main module of the game. It creates the map and starts the game.'''

import random
from map import Map
import the_game

if __name__ == "__main__":
    random.seed(2)
    print("#####################")
    g = the_game.theGame()
    g.buildFloor()
    Map.play(g._floor)
