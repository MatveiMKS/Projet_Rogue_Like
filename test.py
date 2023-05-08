import random
import copy


class Coord():

    def __init__(self, x,y):

        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __repr__(self):
        return f"<{self.x},{self.y}>"
   
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

class Map():
   
    empty = " "
    ground = "."
    dir = {'z': Coord(1,0), 's': Coord(0,1), 'd': Coord(1,0), 'q': Coord(-1,0)}

    def __init__(self, size=20, hero=None, nbrooms=7):

        self._mat = []
        for i in range(size):
            self._mat.append([Map.empty]*size)
           

       
        if hero == None:
            self._hero = Hero()

       
        else:
            self._hero = hero
           
        #self._mat[pos.y][pos.x] = self._hero
        self._elem = {}#self._hero : pos}
        self._roomsToReach = []
        self._rooms = []
        self._nbrooms = nbrooms
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self._mat[self._rooms[0].center().y][self._rooms[0].center().x] = self._hero
        self._elem[self._hero] = self._rooms[0].center()
        #self.put(self._rooms[0].center(), self._hero)
        for rooms in self._rooms:
            rooms.decorate(self)

    def __repr__(self):
        string = ""
        for sublist in self._mat:
            for i in sublist:
                string += str(i)
            string += "\n"
       
        return string
   
    def __len__(self):
        return len(self._mat)
       
    def __contains__(self, item):
        if isinstance(item, Coord):
            if item.x < len(self) and item.y < len(self) and item.x >= 0 and item.y >= 0:
                return True  
            return False
        return item in self._elem
   
    def get(self,item):
        self.checkCoord(item)
        return self._mat[item.y][item.x]
   
    def pos(self, item):
        self.checkElement(item)
        return self._elem[item]
   
    def put(self, coord, item):

        self.checkCoord(coord)
        self.checkElement(item)
       
        if self.get(coord) != self.ground:
            raise ValueError("Incorrect cell")
       
        if item in self._elem:
            raise KeyError("Already placed")
       

        self._mat[coord.y][coord.x] = item
        self._elem[item] = coord

    def rm(self, coords):
        if coords in self:
            self._mat[coords.y][coords.x] = Map.ground
            for key, element in self._elem.items():
                if element == coords:
                    del self._elem[key]
                    break

    def move(self, item, way):
        if item in self._elem and self.pos(item)+way in self :
           
            pos_fin = self.pos(item)+way
            if self.get(pos_fin) != self.empty:
                if self.get(pos_fin) != self.ground:
               
                    if isinstance(item,Element):

                        if self.get(pos_fin).meet(item) == True:
                            self.rm(pos_fin)


                else:
                    self.rm(self.pos(item))
                    self.put(pos_fin, item)

    def play(self):
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")

    def addRoom(self, room):
        self._roomsToReach.append(room)
        for ligns in range(room.c1.y, room.c2.y+1):
            for case in range(room.c1.x, room.c2.x+1):
                self._mat[ligns][case] = Map.ground

    def findRoom(self, coord):
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False
   
    def intersectNone(self, room):
        for rooms in self._roomsToReach:
            if room.intersect(rooms):
                return False
        return True
   
    def dig(self, coord):
        self._mat[coord.y][coord.x] = self.ground
        room = self.findRoom(coord)
       
        if room:
            self._rooms.append(room)
            self._roomsToReach.remove(room)
           
    def corridor(self, start, end):

        if start.y > end.y:
            for point in range (start.y, end.y, -1):
                self.dig(Coord(start.x,point))
        else:
            for point in range (start.y, end.y+1):
                self.dig(Coord(start.x,point))
           
        if start.x < end.x:
            for point in range(start.x, end.x+1):
                self.dig(Coord(point, end.y))
        else:
            for point in range(start.x, end.x, -1):
                self.dig(Coord(point, end.y))

    def reach(self):
        starting_room = random.choice(self._rooms)
        roomtoreach = random.choice(self._roomsToReach)
        self.corridor(starting_room.center(), roomtoreach.center())

    def reachAllRooms(self):
        self._rooms.append(self._roomsToReach[0])
        self._roomsToReach.remove(self._roomsToReach[0])
        while len(self._roomsToReach) != 0:
            self.reach()

    def randRoom(self):
        c1 = Coord(random.randint(0, len(self)-3), random.randint(0, len(self)-3))
        w, l = [random.randint(3,8) for _ in range(2)]
        c2 = Coord(min(len(self)-1,c1.x + w), min(len(self)-1, c1.y + l))
        return Room(c1, c2)
   
    def generateRooms(self, n):

        for i in range(n):
            rand_room = self.randRoom()
            if self.intersectNone(rand_room):
                self.addRoom(rand_room)

    def checkCoord(self, item):
        if not(isinstance(item, Coord)):
            raise TypeError('Not a Coord')
        if not(item in self):
            raise IndexError('Out of map coord')
   
    def checkElement(self, item):
        if not(isinstance(item, Element)):
            raise TypeError("Not a Element")

class Element():

    def __init__(self, name, abbrv =None):

        self._name = name
        if abbrv:
            self._abbrv = abbrv
        else :
            self._abbrv = self._name[0]

    def __repr__(self):
        return self._abbrv
   
    def description(self):
        return f"<{self._name}>"
   
    def meet(self, hero):
        raise NotImplementedError("Not implemented yet")

class Creature(Element):
   
    def __init__(self, name, hp, abbrv=None, strength=1):
        Element.__init__(self,name, abbrv)

        self._hp = hp
        self._strength = strength
   
    def description(self):
        return Element.description(self) + f"({self._hp})"
   
    def meet(self, other):
        self._hp -= other._strength
        theGame().addMessage("The " + other._name + " hits the " + self.description())
        if self._hp < 0:
            return True
        return False    

class Hero(Creature):


    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2):
        super().__init__(name, hp, abbrv, strength)

        self._inventory = []



    def description(self):
        return super().description() + str(self._inventory)
   
    def take(self, elem):
        if not isinstance(elem, Equipment):
            raise TypeError("Not an equipment")
           
        self._inventory.append(elem)

class Room():

    def __init__(self, c1, c2):

        self.c1 = c1
        self.c2 = c2


    def __repr__(self):
        return f"[<{self.c1.x},{self.c1.y}>, <{self.c2.x},{self.c2.y}>]"
   
    def __contains__(self, elem):
        return elem.x >= self.c1.x and elem.y >= self.c1.y and elem.x <= self.c2.x and elem.y <= self.c2.y
   
    def center(self):
        midx = (self.c1.x + self.c2.x)//2
        midy = (self.c1.y + self.c2.y)//2
        return Coord(midx, midy)

    def intersect(self, other):
        a = other.c1 in self or other.c2 in self or Coord(other.c2.x, other.c1.y) in self or Coord(other.c1.x, other.c2.y) in self
        b = self.c1 in other or self.c2 in other or Coord(self.c2.x, self.c1.y) in other or Coord(self.c1.x, self.c2.y) in other
        return a or b
   
    def randCoord(self):
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))
   
    def randEmptyCoord(self, map):

        while True:
            coord_r = self.randCoord()
            if map.get(coord_r) == map.ground and coord_r != self.center():
                return coord_r

    def decorate(self, map):
        map.put(self.randEmptyCoord(map), theGame().randEquipment())
        map.put(self.randEmptyCoord(map), theGame().randMonster())

class Equipment(Element):

    def __init__(self, name, abbrv=None):
        super().__init__(name, abbrv)

    def meet(self, hero):
        hero.take(self)
        theGame().addMessage("You pick up a " + self._name)
        return True

class Game():

    equipments = { 0: [ Equipment("potion","!"), Equipment("gold","o") ], 1: [ Equipment("sword"), Equipment("bow") ], 2: [ Equipment("chainmail") ] }
    monsters = { 0: [ Creature("Goblin",4), Creature("Bat",2,"W") ], 1: [ Creature("Ork",6,strength=2), Creature("Blob",10) ], 5: [ Creature("Dragon",20,strength=3) ] }

    def __init__(self, hero=Hero(), level=1):

        self._hero = hero
        self._level = level
        self._floor = None
        self._message = []
        self._messages = []

    def buildFloor(self):
        self._floor = Map(hero=self._hero)

    def addMessage(self, msg):
        self._message.append(msg)

    def readMessages(self):
        res = ""
       
        for messages in self._message:
            res += messages + ". "
            self._message = []
       
        return res
   
    def randElement(self, collection):
        var_exp = random.expovariate(1/self._level)
        res = []
        for liste in collection:
            if var_exp > liste:
                res = (collection[liste])
            else:
                break

        return copy.copy(random.choice(res))
   
    def randMonster(self):
        return self.randElement(self.monsters)
   
    def randEquipment(self):
        return self.randElement(self.equipments)
   
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
    return game