from cons import *
from fltk import *

def load_map(filename):
    with open(filename, 'r') as f:
        map = []
        for line in f:
            row = [int(x) for x in line.strip().split(',')]
            map.append(row)
        print(map)
        return map

def find_sheep_init(map):
    cs = M_CELL_SIZE(map)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == -1:
                return (j * cs, i * cs)   # x, y
    assert False, "No sheep found in the map"

def valid_map(map):
    # check if the map is valid (contains only -2, -1, 0, 1)
    sheep_count = 0
    end_count = 0
    for row in map:
        for cell in row:
            if cell not in [-2, -1, 0, 1]:
                return False
            if cell == -1:
                sheep_count += 1
            if cell == 1:
                end_count += 1
    if sheep_count == 1 or end_count == 1:
        return True
    return False



class Map:
    # list of solid cell :
    _solid = [-2]

        
    def __init__(self, filename):
        self.map = load_map(filename)
        self.sheep = find_sheep_init(self.map)
        if not valid_map(self.map):
            exit("Invalid map")


    # take a map (List of List of integers)
    def showMap(self):
        map = self.map 
        cell_size = M_CELL_SIZE(map)
        for i in range(len(map)):
            for j in range(len(map[i])):
                couleur = "white"
                match map[i][j]:
                    case -2:
                        couleur = "orange"
                    case -1:
                        couleur = "white"
                    case 0:
                        couleur = "white"
                    case 1:
                        couleur = "green"
                rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size,couleur=couleur, remplissage=couleur)
    
    def showSheep(self):
        cell_size = M_CELL_SIZE(self.map)
        sheep_size = cell_size // 2

        x, y = self.sheep  # coordonnées en pixels

        ax = x + cell_size//4
        ay = y + cell_size//2
        bx = ax + sheep_size
        by = ay + sheep_size

        rectangle(ax, ay, bx, by, couleur="red", remplissage="red")

    def apply_vec_on_sheep(self, vector):
        # apply the vector on the sheep
        x, y = self.sheep
        dx = vector.x2 - vector.x1
        dy = vector.y2 - vector.y1
        new_x = x + dx
        new_y = y + dy
        self.sheep = (new_x, new_y)
