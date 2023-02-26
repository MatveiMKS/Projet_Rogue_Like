from map import Map
from coord import Coord

if __name__ == "__main__":
    carte = Map(3, Coord(2,1))
    print(carte)

    print(carte['@'])
    print(carte[Coord(2,1)])

    carte[Coord(1,1)] = 'X'
    print(carte)

    carte['X'] = Coord(0,0)
    print(carte)
    
    carte.play()
    