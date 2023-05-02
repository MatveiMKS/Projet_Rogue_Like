'''File contains theGame function which returns the game singleton.'''

from .game import Game

def theGame(game = Game()):
    '''Returns the game singleton.'''
    return game
