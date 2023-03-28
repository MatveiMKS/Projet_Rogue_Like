'''This module contains the Map class, used to represent a map.'''
from utils import getch
from coord import Coord
#from element import Element
#from creature import Creature
from hero import Hero

from random import randint, choice

class Map():
    '''Used to represent a map.'''
    ground = '.' # class attribute, used to describe an empty cell
    empty = ' ' # class attribute, used to describe an empty cell
    dir = {'z' : Coord(0,-1),
           's' : Coord(0,1),
           'd' : Coord(1,0),
           'q' : Coord(-1,0)} # class attribute, used to describe the directions

    def __init__(self, size = 20, pos = Coord(1,1), hero = None):
        self._mat = [[Map.empty for _ in range(size)] for _ in range(size)]
        # used to initialize the map with ground cells
        self._hero = hero if hero else Hero()
        self._elem = {self._hero : pos} # used to store the elements of the map and their positions
        #self._mat[pos.y][pos.x] = self._hero
        self._roomsToReach = []
        self._rooms = []

    def __repr__(self):
        '''Prints the map line by line.'''
        string = ""
        for sub_list in self._mat:
            for case in sub_list:
                string += str(case)
            string += "\n"
        return string

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        '''Returns True if item's coordinates are in the map, or if item is in the map. 
        Returns False otherwise.'''
        long = len(self)
        if isinstance(item, Coord):
            return (item.x >= 0 and item.x < long) and (item.y >= 0 and item.y < long)
        return item in self._elem

    def get(self, coords):
        '''Returns the element at the coordinates coords.
        Returns None if coords is not in the map.'''
        if coords in self:
            return self._mat[coords.y][coords.x]
        return None

    def pos(self, element):
        '''Returns the coordinates of element. Returns None if element is not in the map.'''
        if element in self._elem:
            return self._elem[element]
        return None

    def put(self, coords, element):
        '''Puts element at the coordinates coords.'''
        if coords in self:
            self._mat[coords.y][coords.x] = element
            self._elem[element] = coords

    def rm(self, coords):
        '''Removes the element at the coordinates coords.'''
        if coords in self:
            self._mat[coords.y][coords.x] = Map.ground
            for key, element in self._elem.items():
                if element == coords:
                    del self._elem[key]
                    break

    def move(self, element, way):
        '''Moves element in the direction way.'''
        if element in self._elem:
            if self.pos(element)+way in self and self.get(self.pos(element) +way) == Map.ground:
                # if the cell is empty
                pos_ini = self.pos(element)
                self.rm(pos_ini)
                self.put(pos_ini+way, element)
            elif self.pos(element)+way in self:
                # if the cell is not empty
                met_element = self.get(self.pos(element) +way)
                if met_element.meet(element):
                    pos_ini = self.pos(element)
                    self.rm(pos_ini + way)


    def __getitem__(self, key):
        '''Returns the element at the coordinates key or the coordinates of the element key.'''
        if isinstance(key, Coord):
            return self.get(key)
        return self.pos(key)

    def __setitem__(self, key, value):
        '''Puts value at the coordinates key or the key to the coordinates value. 
        If the element key already exists, key is moved to coordinates value.'''
        if isinstance(key, Coord):
            self.put(key, value)
        else:
            if key in self._elem:
                pos_ini = self.pos(key)
                self.rm(pos_ini)
                self.put(value, key)

    def addRoom(self, room):
        '''Adds a room to the map.'''
        self._roomsToReach.append(room)
        for i in range(room.c1.x, room.c2.x+1):
            for j in range(room.c1.y, room.c2.y+1):
                self._mat[j][i] = Map.ground

    def findRoom(self, coord):
        '''Returns the room at the coordinates coord.'''
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False

    def intersectNone(self, room):
        '''Returns True if the room doesn't intersect with any other room.
        Returns False otherwise.'''
        for otherRoom in self._roomsToReach:
            if room.intersect(otherRoom):
                return False
        return True

    def dig(self, coord):
        '''Dig the ground at the coordinates coord.
        And if the ground is a room, it is removed from the list of rooms to reach.'''
        self._mat[coord.y][coord.x] = Map.ground
        room = self.findRoom(coord)
        if room:
            self._roomsToReach.remove(room)
            self._rooms.append(room)

    def corridor(self, start : Coord, end : Coord):
        '''Creates a corridor between the coordinates start and end.'''
        dir_x = 1 if end.x > start.x else -1
        dir_y = 1 if end.y > start.y else -1

        for i in range(start.y, end.y+dir_y, dir_y):
            self.dig(Coord(start.x, i))
        for i in range(start.x, end.x+dir_x, dir_x):
            self.dig(Coord(i, end.y))

    def reach(self):
        '''Creates a corridor between a random room and a random room to reach.'''
        if self._rooms and self._roomsToReach:
            room_ini = choice(self._rooms)
            room_fin = choice(self._roomsToReach)
            self.corridor(room_ini.center(), room_fin.center())
            return True
        return False

    def reachAllRooms(self):
        '''Creates a corridor between all the rooms and all the rooms to reach.'''
        if self._roomsToReach:
            self._rooms.append(self._roomsToReach.pop(0))
            while self.reach():
                pass
            return True
        return False
    
    def randRoom(self):
        '''Returns a random room to the map.
        With a size between 3 and 8.'''
        width = randint(3, 8)
        height = randint(3, 8)
        x = randint(0, len(self)-width)
        y = randint(0, len(self)-height)
        salle = Room(Coord(x, y), Coord(x+width, y+height))
        self.addRoom(salle)


    def play(self):
        '''Plays the game.'''
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")
