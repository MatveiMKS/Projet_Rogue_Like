''' Equipement class '''
from .element import Element
from .the_game import theGame

class Equipment(Element):
    '''Equipement class, inherits from Element class.'''
    def meet(self, hero):
        '''Called when a Hero element meets an element.'''
        hero.take(self)
        theGame().addMessage("You pick up a " + self)
        return True
