class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
        
    def __repr__(self):
        return f"<{self.x},{self.y}>"
        
    def __add__(self,other):
        nvX = self.x + other.x
        nvY = self.y + other.y
        return Coord(nvX, nvY)