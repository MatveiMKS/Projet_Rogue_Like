'''This module contains the Room class.'''''

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
        return (self.c1.x <= other.c2.x and self.c2.x >= other.c1.x
                and self.c1.y <= other.c2.y and self.c2.y >= other.c1.y)
