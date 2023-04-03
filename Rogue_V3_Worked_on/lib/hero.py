'''This module contains the Hero class.'''

from .creature import Creature

class Hero(Creature):
    '''This class represents the hero in the game.'''
    def __init__(self, name = 'Hero', hp = 10, abbrv = '@', strength = 2):
        super().__init__(name, hp, abbrv, strength)
        self._inventory = []

    def take(self, item):
        '''Adds item to the inventory.'''
        self._inventory.append(item)

    def description(self):
        return super().description() + str(self._inventory)
    