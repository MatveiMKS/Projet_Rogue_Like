'''Main module of the game. It creates the map and starts the game.'''

from lib.creature import Creature
from lib.hero import Hero
from lib.element import Element
from lib.equipment import Equipment
from lib import the_game
import random

if __name__ == "__main__":

    #test d'appel de checkCoord/CheckElement dans les méthodes

    Equipment("sword").meet(the_game.theGame()._hero)
    print(the_game.theGame().readMessages())

    try:
        Element("water").meet(Hero())
    except NotImplementedError:
        print("Test passed")

    the_game.theGame().hero = Hero()
    Creature("Goblin", 5).meet(the_game.theGame()._hero)
    print(the_game.theGame().readMessages())
    the_game.theGame()._hero.meet(Creature("Orc", 10))
    print(the_game.theGame().readMessages())
