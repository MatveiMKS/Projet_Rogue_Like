''' Equipement class '''
from .element import Element #can stay
from . import the_game as gm

class Equipment(Element):
    '''Equipement class, inherits from Element class.'''
    def meet(self, hero):
        '''Called when a Hero element meets an element.'''
        hero.take(self)
        gm.theGame().addMessage("You pick up a " + self._name)
        return True
