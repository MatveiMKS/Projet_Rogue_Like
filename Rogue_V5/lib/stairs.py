from lib.element import Element
from . import the_game as gm

class Stairs(Element):
    '''Stairs class, inherits from Element class.'''
    def __init__(self):
        super().__init__("Stairs", "E")

    def meet(self, hero):
        '''Called when a Hero element meets an element.'''
        gm.theGame().addMessage(f"The {hero._name} goes down.")
        gm.theGame().buildFloor()
        gm.theGame()._level += 1
