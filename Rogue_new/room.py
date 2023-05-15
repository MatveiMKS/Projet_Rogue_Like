'''This module contains the Room class.'''''
import random #can stay
from coord import Coord #can stay
import the_game

class Room():
    '''A room in the dungeon.'''
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        ''' Returns a string representation of the room.'''
        return f"[{self.c1}, {self.c2}]"

    def __contains__(self, item):
        '''Returns True if item is in the room, False otherwise.'''
        return ((item.x >= self.c1.x and item.x <= self.c2.x)
                and (item.y >= self.c1.y and item.y <= self.c2.y))

    def center(self):
        '''Returns the center of the room.'''
        return Coord((self.c1.x + self.c2.x) // 2, (self.c1.y + self.c2.y) // 2)

    def intersect(self, other):
        '''Returns True if self intersects other, False otherwise.'''
        y_self_bas = min(self.c1.y, self.c2.y)
        y_self_haut = max(self.c1.y, self.c2.y)

        x_self_gauche = min(self.c1.x, self.c2.x)
        x_self_droite = max(self.c1.x, self.c2.x)

        y_other_bas = min(other.c1.y, other.c2.y)
        y_other_haut = max(other.c1.y, other.c2.y)

        x_other_gauche = min(other.c1.x, other.c2.x)
        x_other_droite = max(other.c1.x, other.c2.x)

        if (y_self_bas > y_other_haut or y_self_haut < y_other_bas):
            #if self is below other or self is above other
            return False

        if (x_self_gauche > x_other_droite or x_self_droite < x_other_gauche):
            #if self is to the right of other or self is to the left of other
            return False
        return True

    def randCoord(self):
        '''Returns a random position in the room.'''
        pos_x = random.randint(min(self.c1.x, self.c2.x), max(self.c1.x, self.c2.x))
        pos_y = random.randint(min(self.c1.y, self.c2.y), max(self.c1.y, self.c2.y))
        return Coord(pos_x, pos_y)

    def randEmptyCoord(self, map):
        """A random coordinate inside the room which is free on the map."""
        c = self.randCoord()
        while map.get(c) != map.ground or c == self.center():
            c = self.randCoord()
        return c

    def decorate(self, map):
        """Decorates the room by adding a random equipment and monster."""
        map.put(self.randEmptyCoord(map), the_game.theGame().randEquipment())
        map.put(self.randEmptyCoord(map), the_game.theGame().randMonster())