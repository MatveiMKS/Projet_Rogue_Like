'''Main module of the game. It creates the map and starts the game.'''

from lib.element import Element
import lib.game
import lib.creature
import lib.hero
import lib.equipment


if __name__ == "__main__":

    #test d'appel de checkCoord/CheckElement dans les méthodes

    lib.equipment.Equipment("sword").meet(lib.game.theGame()._hero)
    print(lib.game.theGame().readMessages())

    try:
        Element("water").meet(lib.hero.Hero())
    except NotImplementedError:
        print("Test passed")

    lib.game.theGame().hero = lib.hero.Hero()
    lib.creature.Creature("Goblin", 5).meet(lib.game.theGame()._hero)
    print(lib.game.theGame().readMessages())
    lib.game.theGame()._hero.meet(lib.creature.Creature("Orc", 10))
    print(lib.game.theGame().readMessages())
