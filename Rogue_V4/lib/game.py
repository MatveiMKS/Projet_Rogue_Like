'''Contains the Game class, which contains the main game loop and all game logic.
 Also contains the game singleton function theGame.'''

import random
from .hero import Hero
from .map import Map
from . import creature as crt
from .equipment import Equipment


class Game():
    ''' Contains main game loop and all game logic'''

    equipments = { 0: [ Equipment("potion","!"), Equipment("gold","o") ],
                  1: [ Equipment("sword"), Equipment("bow") ],
                  2: [ Equipment("chainmail") ] }
    monsters = { 0: [ crt.Creature("Goblin",4), crt.Creature("Bat",2,"W") ],
                1: [ crt.Creature("Ork",6,strength=2), crt.Creature("Blob",10) ],
                5: [ crt.Creature("Dragon",20,strength=3) ] }

    def __init__(self, hero=None, level=1):
        self._hero = hero if hero else Hero()
        self._level = level
        self._floor = None
        self._messages = []

    def buildFloor(self):
        '''Builds a new floor.'''
        self._floor = Map()

    def addMessage(self, message):
        '''Adds a message to the message list.'''
        if type(message) != str:
            raise TypeError("Message must be a string")
        self._messages.append(message)

    def readMessages(self):
        '''Returns the message list as a string separated by periods.'''
        if len(self._messages) == 0:
            return ""
        messages = ". ".join(self._messages) + "."
        self._messages = []
        return messages

    def randElement(self, collection):
        '''Returns a random element from Collection.'''
        variable_expo = random.expovariate(1/self._level)
        liste_pg_deg = []
        for liste in collection:
            if variable_expo > liste:
                liste_pg_deg = collection[liste]
            else:
                break
        return random.choice(liste_pg_deg)

    def randMonster(self):
        '''Returns a random monster.'''
        return self.randElement(Game.monsters)

    def randEquipment(self):
        '''Returns a random equipment.'''
        return self.randElement(Game.equipments)
        