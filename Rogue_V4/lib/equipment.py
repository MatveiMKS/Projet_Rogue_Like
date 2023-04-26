''' Equipement class '''
from  .element   import   Element

class Equipment(Element):
    '''Equipement class, inherits from Element class.'''
    def meet(self, hero):
        '''Called when a Hero element meets an element.'''
        hero.take(self)
        return True
