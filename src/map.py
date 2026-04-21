from cons import *
from fltk import *

def loadMap(filename):
    with open(filename, 'r') as f:
        map = []
        for line in f:
            row = [int(x) for x in line.strip().split(',')]
            map.append(row)
        print(map)
        return map

def findSheepInit(map):
    cs = M_CELL_SIZE(map)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == -1:
                return (i*cs, j*cs)
    assert False, "No sheep found in the map"

class Map:
    # return a list of list containing integers representing initial map
        
    def __init__(self, filename):
        self.map = loadMap(filename)
        self.sheep = findSheepInit(self.map)


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
        i, j = self.sheep 
        rectangle(i,j,j-sheep_size,j-sheep_size, couleur="red", remplissage="red")


    
