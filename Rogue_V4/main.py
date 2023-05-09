'''Main module of the game. It creates the map and starts the game.'''

from lib.element import Element
import lib.the_game
import lib.creature
import lib.hero
import lib.equipment


if __name__ == "__main__":

    #test d'appel de checkCoord/CheckElement dans les méthodes

    lib.equipment.Equipment("sword").meet(lib.the_game.theGame()._hero)
    print(lib.the_game.theGame().readMessages())

    try:
        Element("water").meet(lib.hero.Hero())
    except NotImplementedError:
        print("Test passed")

    lib.the_game.theGame().hero = lib.hero.Hero()
    lib.creature.Creature("Goblin", 5).meet(lib.the_game.theGame()._hero)
    print(lib.the_game.theGame().readMessages())
    lib.the_game.theGame()._hero.meet(lib.creature.Creature("Orc", 10))
    print(lib.the_game.theGame().readMessages())
