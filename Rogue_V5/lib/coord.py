'''This module contains the Coord class.'''
import math

class Coord():
    '''Used to represent coordinates in a 2D space.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return f"<{self.x},{self.y}>"

    def __add__(self,other):
        nv_x = self.x + other.x
        nv_y = self.y + other.y
        return Coord(nv_x, nv_y)

    def __sub__(self,other):
        nv_x = self.x - other.x
        nv_y = self.y - other.y
        return Coord(nv_x, nv_y)

    def distance(self, other):
        '''Returns the distance between self and other.'''
        return math.sqrt((self.x - other.x)^2 + (self.y - other.y)^2)

    def direction(self, other):
        '''Returns the direction from self to other.'''
        diff = other - self
        rapport = diff.x / abs(diff)
        if rapport > 1/math.sqrt(2):
            return Coord(-1,0)
        elif rapport < -1/math.sqrt(2):
            return Coord(1,0)
        elif diff.y > 0:
            return Coord(0,-1)
        else:
            return Coord(0,1)
