'''This file contains the Element class, which is used to represent an element in the game.'''

import abc

class Element():
    '''This class represents an element in the game.'''
    def __init__(self, name, abbrv = None) -> None:
        self._name = name
        self._abbrv = abbrv if abbrv else name[0]

    def __repr__(self):
        return self._abbrv

    def description(self):
        '''Returns a description of the element.'''
        return f"<{self._name}>"

    def meet(self, hero):
        '''Abstract method called when a Hero element meets an element.'''
        raise NotImplementedError("Not implemented yet")
