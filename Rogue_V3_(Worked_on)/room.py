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
