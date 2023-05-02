'''File contains theGame function which returns the game singleton.'''

from . import game

def theGame(game = game.Game()):
    '''Returns the game singleton.'''
    return game
