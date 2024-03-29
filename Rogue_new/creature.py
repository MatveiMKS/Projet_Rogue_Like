'''This module contains the Creature class.'''

from element import Element #can stay
import the_game as gm

class Creature(Element):
    '''This class represents a creature in the game.'''
    def __init__(self, name, hp, abbrv = None, strength = 1):
        super().__init__(name, abbrv)
        self._hp= hp
        self._strength = strength

    def description(self):
        return super().description() + f"({self._hp})"

    def meet(self, hero):
        '''Called when a Creature element meets an element.'''
        self._hp -= hero._strength
        gm.theGame().addMessage(f"The {hero._name} hits the {self.description()}")
        if self._hp <= 0:
            return True
        return False
    