from fltk import *

class Vector:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    def __str__(self):
        return f"Vector(({self.x1}, {self.y1}) -> ({self.x2}, {self.y2}))"
        

    def set_start(self, x1:int, y1:int):
        self.x1 = x1
        self.y1 = y1

    def set_end(self, x2:int, y2:int):
        self.x2 = x2
        self.y2 = y2

    def is_void(self):
        return self.x1 is None or self.y1 is None

    def is_complete(self):
        return self.x2 is not None and self.y2 is not None

    def clear(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    '''
    normalize the vector to have a length of 1, keeping the same direction and return intensity
    '''
    def normalize(self):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        length = (dx**2 + dy**2) ** 0.5
        if length == 0:
            return 0
        self.x2 = self.x1 + dx / length
        self.y2 = self.y1 + dy / length
        return length  

    def draw(self, couleur="blue", epaisseur=3):
        if self.is_complete():
            ligne(self.x1, self.y1, self.x2, self.y2, couleur=couleur, epaisseur=epaisseur)

    def draw_preview(self, x, y, couleur="blue", epaisseur=3):
        ligne(self.x1, self.y1, x, y, couleur=couleur, epaisseur=epaisseur)

    def copy(self):
        new_vector = Vector()
        new_vector.x1 = self.x1
        new_vector.y1 = self.y1
        new_vector.x2 = self.x2
        new_vector.y2 = self.y2
        return new_vector