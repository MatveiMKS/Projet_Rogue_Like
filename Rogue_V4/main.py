'''Main module of the game. It creates the map and starts the game.'''

from lib.map import Map
from lib.element import Element
from lib.creature import Creature

if __name__ == "__main__":
    m = Map(20)
    list_of_elements= [Element('Gold', 'G'),
                        Element('Silver', 'S'),
                        Creature('Ogre', 5, 'o', 1),
                        Creature('Dragon', 10, 'D', 3)]
    m.fill_map(list_of_elements, 25)
    m.play()
