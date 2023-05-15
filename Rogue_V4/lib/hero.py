'''This module contains the Hero class.'''

from .creature import Creature
from .equipment import Equipment

class Hero(Creature):
    '''This class represents the hero in the game.'''
    def __init__(self, name = 'Hero', hp = 10, abbrv = '@', strength = 2):
        super().__init__(name, hp, abbrv, strength)
        self._inventory = []

    def take(self, item: Equipment):
        '''Adds item to the inventory.'''
        if not isinstance(item, Equipment):
            raise TypeError(f"Can't take {item} as equipement.")
        self._inventory.append(item)

    def description(self):
        return super().description() + str(self._inventory)

    def health(self):
        '''Returns the health of the hero.'''
        return self._hp

    def take_dammage(self, dammage):
        '''Takes dammage.'''
        self._hp -= dammage

    def dammage(self):
        '''Returns the dammage of the hero.'''
        return self._strength
