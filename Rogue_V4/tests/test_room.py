'''Test the Room class.'''
# pylint: disable= E0401, C0413
from sys import path
from pathlib import Path

f = Path(__file__).parent.parent
path.append(str(f))

from lib.room import Room
from lib.coord import Coord

def test_repr():
    '''Test the repr method.'''
    c1 = Coord(1, 1)
    c2 = Coord(5, 5)
    room = Room(c1, c2)
    assert repr(room) == "[<1,1>, <5,5>]"

    c3 = Coord(-1, 1)
    c4 = Coord(5, -5)
    room = Room(c3, c4)
    assert repr(room) == "[<-1,1>, <5,-5>]"

def test_contains():
    '''Test the __contains__ method.'''
    c1 = Coord(1, 1)
    c2 = Coord(5, 5)
    room = Room(c1, c2)
    assert Coord(3, 3) in room
    assert Coord(1, 1) in room
    assert Coord(5, 5) in room
    assert Coord(0, 0) not in room
    assert Coord(6, 6) not in room

    room2 = Room(Coord(0, 0), Coord(0, 0))
    assert Coord(0, 0) in room2
    assert Coord(1, 1) not in room2

    c3 = Coord(-1, -4)
    c4 = Coord(5, 5)
    room3 = Room(c3, c4)
    assert Coord(0, 0) in room3
    assert Coord(1, 1) in room3
    assert Coord(-1, -4) in room3
    assert Coord(5, 5) in room3
    assert Coord(-2, -5) not in room3
    assert Coord(6, 6) not in room3
    assert Coord(0, -5) not in room3


def test_center():
    '''Test the center method.'''
    c1 = Coord(1, 1)
    c2 = Coord(5, 5)
    room = Room(c1, c2)
    assert room.center() == Coord(3, 3)

    c3 = Coord(-1, -4)
    c4 = Coord(5, 5)
    room = Room(c3, c4)
    assert room.center() == Coord(2, 0)

def test_intersect():
    '''Test the intersect method.'''

    c1 = Coord(1, 1)
    c2 = Coord(5, 5)
    room = Room(c1, c2)

    c3 = Coord(3, 3)
    c4 = Coord(7, 7)
    room2 = Room(c3, c4)
    # Tests the case where the room 1 top right corner intersects with room 2 bottom left corner.
    assert room.intersect(room2)
    assert room2.intersect(room)

    c5 = Coord(6, 6)
    c6 = Coord(10, 10)
    room3 = Room(c5, c6)
    # Tests the case where room 3 is above to the right of room 1.
    assert not room.intersect(room3)
    assert not room3.intersect(room)

    c7 = Coord(-1, -1)
    c8 = Coord(-3, -3)
    room4 = Room(c7, c8)
    # Tests the case where room 4 is below to the left of room 1.
    assert not room.intersect(room4)
    assert not room4.intersect(room)

    c9 = Coord(0, 0)
    c10 = Coord(0, 0)
    room5 = Room(c9, c10)
    # Tests the case where room 5 is a single point.
    assert not room.intersect(room5)
    assert not room5.intersect(room)

    c11 = Coord(2, 2)
    c12 = Coord(4, 4)
    room6 = Room(c11, c12)
    # Tests the case where room 6 is entirely inside room 1.
    assert room.intersect(room6)
    assert room6.intersect(room)

    c13 = Coord(2, 0)
    c14 = Coord(4, 6)
    room7 = Room(c13, c14)
    # Tests the case where room 7 overlaps room 1 but the corners are outside.
    assert room.intersect(room7)
    assert room7.intersect(room)

    c15 = Coord(1, 1)
    c16 = Coord(9, 3)
    c17 = Coord(0, 0)
    c18 = Coord(1, 8)
    room8 = Room(c15, c16)
    room9 = Room(c17, c18)
    # Tests the case where room 9 overlaps room 8 but the corners and centers are outside.
    assert room8.intersect(room9)
    assert room9.intersect(room8)

    c19 = Coord(1, 2)
    c20 = Coord(2, -8)
    room10 = Room(c19, c20)
    # Tests the case where room 9 overlaps room 8 but the centers are outside.
    assert room8.intersect(room10)
    assert room10.intersect(room8)

    c21 = Coord(1, -1)
    c22 = Coord(2, -2)
    room11 = Room(c21, c22)
    # Tests the case where room 11 is entirely below room 8.
    assert not room8.intersect(room11)
    assert not room11.intersect(room8)
