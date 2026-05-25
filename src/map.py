from cons import *
from fltk import *

from vector import Vector

def load_map(filename):
    """Load a map from a file. The file should contain rows of integers separated by commas.
    Returns a 2D list of integers representing the map.
    """
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
    _solid = [-2,1]

        
    def __init__(self, filename):
        self.map = load_map(filename)
        self.sheep = find_sheep_init(self.map)
        self.current_vector = Vector()
        self.current_intensity = 0
        self.velocity_x = 0
        self.velocity_y = 0
        if not valid_map(self.map):
            exit("Invalid map")

    def __str__(self):
        return str(self.map) + "\nSheep position: " + str(self.sheep) + "\nCurrent vector: " + str(self.current_vector)


    # take a map (List of List of integers)
    def show_map(self):
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
    
    def show_sheep(self):
        cell_size = M_CELL_SIZE(self.map)
        x, y = self.sheep
        ax = x + cell_size//4
        ay = y + cell_size//2  
        bx = ax + cell_size//2
        by = ay + cell_size//2
        rectangle(ax, ay, bx, by, couleur="red", remplissage="red")

    def sheep_intersect_solid(self):
        x, y = self.sheep
        cell_size = M_CELL_SIZE(self.map)
        ax = x + cell_size//4
        ay = y + cell_size//2  
        bx = ax + cell_size//2
        by = ay + cell_size//2
        corners = [(ax, ay), (bx, ay), (ax, by), (bx, by)]
        for cx, cy in corners:
            i = int(cy // cell_size)
            j = int(cx // cell_size)
            if 0 <= i < len(self.map) and 0 <= j < len(self.map[0]):
                if self.map[i][j] in self._solid:
                    return True
        return False

    
    def _resolve_collision(self, old_x, old_y, new_x, new_y, was_falling):
        """
        Déplace le mouton de (old_x, old_y) vers (new_x, new_y) en subdivisant
        le mouvement pour éviter le tunneling. Retourne (final_x, final_y).
        Met à jour velocity_x / velocity_y en cas de collision.
        """
        steps = max(1, int(max(abs(new_x - old_x), abs(new_y - old_y))))
        dx = (new_x - old_x) / steps
        dy = (new_y - old_y) / steps

        x, y = old_x, old_y

        for _ in range(steps):
            next_x = x + dx
            next_y = y + dy

            col_h = False
            col_v = False

            self.sheep = (next_x, y)
            if self.sheep_intersect_solid():
                col_h = True
                next_x = x
                self.velocity_x *= -0.25

            self.sheep = (x, next_y)
            if self.sheep_intersect_solid():
                col_v = True
                next_y = y
                self.velocity_y = 0
                if was_falling:
                    self.velocity_x = 0

            x, y = next_x, next_y

            if col_h or col_v:
                break

        return x, y


    def apply_vec_on_sheep(self, new_vector: Vector):
        if not new_vector.is_complete() and not self.current_vector.is_complete():
            return

        if not self.current_vector.is_complete() and new_vector.is_complete():
            vec = new_vector.copy()
            intensity = vec.normalize()
            self.current_vector = vec
            speed = min(intensity * 2, 500) / M_FPS
            self.velocity_x = (vec.x2 - vec.x1) * speed
            self.velocity_y = (vec.y2 - vec.y1) * speed - M_GRAVITY / M_FPS

        x, y = self.sheep
        self.velocity_y += M_GRAVITY / M_FPS
        was_falling = self.velocity_y >= 0

        new_x = x + self.velocity_x
        new_y = y + self.velocity_y

        final_x, final_y = self._resolve_collision(x, y, new_x, new_y, was_falling)
        self.sheep = (final_x, final_y)

        if self.velocity_x == 0 and self.velocity_y == 0:
            self.current_vector.clear()

    