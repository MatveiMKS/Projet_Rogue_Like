import random
import copy
import abc

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
        
class Element(metaclass=abc.ABCMeta):
    '''This class represents an element in the game.'''
    def __init__(self, name, abbrv = "") -> None:
        self._name = name
        self._abbrv = abbrv if abbrv else name[0]

    def __repr__(self):
        return self._abbrv

    def description(self):
        '''Returns a description of the element.'''
        return f"<{self._name}>"

    def meet(self, hero):
        '''Abstract method called when a Hero element meets an element.'''
        raise NotImplementedError("Not implemented yet")
    
class Equipment(Element):
    '''Equipement class, inherits from Element class.'''
    def meet(self, hero):
        '''Called when a Hero element meets an element.'''
        theGame().addMessage("You pick up a " + self._name)
        hero.take(self)
        return True

class Creature(Element):
    '''This class represents a creature in the game.'''
    def __init__(self, name, hp, abbrv = "", strength = 1):
        super().__init__(name, abbrv)
        self._hp= hp
        self._strength = strength

    def description(self):
        return super().description() + f"({self._hp})"

    def meet(self, hero):
        '''Called when a Creature element meets an element.'''
        self._hp -= hero._strength
        theGame().addMessage(f"The {hero._name} hits the {self.description()}")
        if self._hp < 0:
            return True
        return False
        
class Hero(Creature):
    '''This class represents the hero in the game.'''
    def __init__(self, name = 'Hero', hp = 10, abbrv = '@', strength = 2):
        super().__init__(name, hp, abbrv, strength)
        self._inventory = []

    def take(self, item: Equipment):
        '''Adds item to the inventory.'''
        if not isinstance(item, Equipment):
            raise TypeError(f"Can't take {item} as equipement.")
        self._inventory.append(item)

    def description(self):
        return super().description() + str(self._inventory)

    def health(self):
        '''Returns the health of the hero.'''
        return self._hp

    def take_dammage(self, dammage):
        '''Takes dammage.'''
        self._hp -= dammage

    def dammage(self):
        '''Returns the dammage of the hero.'''
        return self._strength
        
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

    def random_pos(self):
        '''Returns a random position in the room.'''
        pos_x = random.randint(min(self.c1.x, self.c2.x), max(self.c1.x, self.c2.x))
        pos_y = random.randint(min(self.c1.y, self.c2.y), max(self.c1.y, self.c2.y))
        return Coord(pos_x, pos_y)
        
class Map():
    '''Used to represent a map.'''
    ground = '.' # class attribute, used to describe an empty cell
    empty = ' ' # class attribute, used to describe an empty cell
    dir = {'z' : Coord(0,-1),
           's' : Coord(0,1),
           'd' : Coord(1,0),
           'q' : Coord(-1,0)} # class attribute, used to describe the directions

    def __init__(self, size = 20, hero = None, nbrooms = 7):
        self._mat = [[Map.empty for _ in range(size)] for _ in range(size)]
        # used to initialize the map with ground cells

        self._hero = hero if hero else Hero()
        self._elem = {} # used to store the elements of the map and their positions
        self._roomsToReach = []
        self._rooms = []
        self.generateRooms(nbrooms)
        self.reachAllRooms()

        salle1 = self._rooms[0] # put the hero in the first room
        centre_sal1 = salle1.center()
        self._mat[centre_sal1.y][centre_sal1.x] = self._hero
        self._elem[self._hero] = centre_sal1

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

    def checkCoord(self, coords):
        '''Raises a TypeError if coords is not a Coord object 
        or an IndexError if coords is not in the map.'''
        if not isinstance(coords, Coord):
            raise TypeError("coords must be a Coord object")
        if coords not in self:
            raise IndexError("coords must be in the map")
        

    def checkElement(self, element):
        '''Raises a TypeError if element is not an Element object 
        or a KeyError if element is not in the map.'''
        if not isinstance(element, Element):
            raise TypeError("element must be an Element object")

    def get(self, coords):
        '''Returns the element at the coordinates coords.
        Returns None if coords is not in the map.'''
        self.checkCoord(coords)
        if coords in self:
            return self._mat[coords.y][coords.x]
        return None

    def pos(self, element):
        '''Returns the coordinates of element. Returns None if element is not in the map.'''
        self.checkElement(element)
        if element in self._elem:
            return self._elem[element]
        return None

    def put(self, coords, element):
        '''Puts element at the coordinates coords.'''
        self.checkCoord(coords)
        self.checkElement(element)
        
        if self._mat[coords.y][coords.x] != Map.ground:
            raise ValueError("coords must be empty")
        if element in self._elem:
            raise KeyError("element must not be in the map")

        if coords in self:
            self._mat[coords.y][coords.x] = element
            self._elem[element] = coords
            
    def rm(self, coords):
        '''Removes the element at the coordinates coords.'''
        self.checkCoord(coords)
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
            elif (self.pos(element)+way) in self and self.get(self.pos(element) +way) != Map.empty:
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
        for other_room in self._roomsToReach:
            if room.intersect(other_room):
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
            room_ini = random.choice(self._rooms)
            room_fin = random.choice(self._roomsToReach)
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
        x_1 = random.randint(0, len(self)-3)
        y_1 = random.randint(0, len(self)-3)

        x_2 = min(len(self)-1, x_1 + random.randint(3, 8))
        y_2 = min(len(self)-1, y_1 + random.randint(3, 8))
        salle = Room(Coord(x_1, y_1), Coord(x_2, y_2))
        return salle

    def generateRooms(self, nbRooms):
        '''Generates nbRooms rooms to the map.'''
        for _ in range(nbRooms):
            salle = self.randRoom()
            if self.intersectNone(salle):
                self.addRoom(salle)

    def fill_map(self, elements, nb_elements):
        '''Puts nb_elements elements of the list elements in the map.'''
        for _ in range(nb_elements):
            room = random.choice(self._rooms)
            pos = room.random_pos()
            if pos != self._rooms[0].center():
                element = random.choice(elements)
                self[pos] = element

    def play(self):
        '''Plays the game.'''
        print("--- Welcome Hero! ---")
        while self._hero.health() > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")
        
class Game():
    ''' Contains main game loop and all game logic'''
    
    equipments = { 0: [ Equipment("potion","!"), Equipment("gold","o") ],
                  1: [ Equipment("sword"), Equipment("bow") ],
                  2: [ Equipment("chainmail") ] }
    monsters = { 0: [ Creature("Goblin",4), Creature("Bat",2,"W") ],
                1: [ Creature("Ork",6,strength=2), Creature("Blob",10) ],
                5: [ Creature("Dragon",20,strength=3) ] }

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
        return copy.copy(random.choice(liste_pg_deg))

    def randMonster(self):
        '''Returns a random monster.'''
        return self.randElement(Game.monsters)

    def randEquipment(self):
        '''Returns a random equipment.'''
        return self.randElement(Game.equipments)
    
def getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')
   
        
def theGame(game = Game()):
    '''Returns the game singleton.'''
    return game
        

	


	
Equipment("sword").meet(theGame()._hero)
print(theGame().readMessages())

	
try:
   Element("water").meet(Hero())
except NotImplementedError:
   print("Test passed")

	
theGame().hero = Hero()
Creature("Goblin", 5).meet(theGame()._hero)
print(theGame().readMessages())
theGame()._hero.meet(Creature("Orc", 10))
print(theGame().readMessages())