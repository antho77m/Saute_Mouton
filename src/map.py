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
        return map

def find_sheep_init(map):
    cs = M_CELL_SIZE(map)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == -1:
                return (j * cs, i * cs -1)   # x, y
    assert False, "No sheep found in the map"

def valid_map(map):
    # check if the map is valid (contains only -2, -1, 0, 1 2)
    sheep_count = 0
    end_count = 0
    for row in map:
        for cell in row:
            if cell not in [-2, -1, 0, 1,2]:
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
    _solid = [1,2]
    _ice = [2]

        
    def __init__(self, filename):
        self.map = load_map(filename)
        self.sheep = find_sheep_init(self.map)
        self.initial_sheep_position = self.sheep
        self.current_vector = Vector()
        self.current_intensity = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.end = False
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
                    case 2:
                        couleur = "cyan"
                rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size,couleur=couleur, remplissage=couleur)
    
    def show_sheep(self):
        cell_size = M_CELL_SIZE(self.map)
        x, y = self.sheep
        ax = x + cell_size//4
        ay = y + cell_size//2  
        bx = ax + cell_size//2
        by = ay + cell_size//2
        # image(ax, ay,"res/mouton.png", largeur=cell_size, hauteur=cell_size,ancrage="w")
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
                if self.sheep_on_end():
                    self.end = True

            self.sheep = (x, next_y)
            if self.sheep_intersect_solid():
                if self.sheep_on_end():
                    self.end = True
                col_v = True
                next_y = y
                self.velocity_y = 0
                if was_falling and not self._sheep_on_ice():  # ✅ sol normal seulement
                    self.velocity_x = 0
                self.sheep = (x, y)

            x, y = next_x, next_y
            if col_h or col_v:
                break

        return x, y

    def _sheep_on_ice(self):
        x, y = self.sheep
        cell_size = M_CELL_SIZE(self.map)
        ax = x + cell_size // 4
        bx = ax + cell_size // 2
        by = y + cell_size // 2 + cell_size // 2 + 1  

        for cx in [ax, bx]:
            j = int(cx // cell_size)
            i = int(by // cell_size)
            if 0 <= i < len(self.map) and 0 <= j < len(self.map[0]):
                if self.map[i][j] in self._ice:
                    return True
        return False
    
    def sheep_on_end(self):
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
                if self.map[i][j] == -2:
                    return True
        return False
    
    def _is_sheep_not_in_screen(self):
        x, y = self.sheep
        cell_size = M_CELL_SIZE(self.map)
        if x < -cell_size or x > len(self.map[0]) * cell_size:
            return True
        if y < -cell_size or y > len(self.map) * cell_size:
            return True
        return False

    def apply_vec_on_sheep(self, new_vector: Vector):
        """
Applique le vecteur new_vector sur le mouton. Si new_vector n'est pas complet, ne fait rien.
si un vecteur est déjà appliqué alors on déplace le mouton selon le vecteur déjà gerer par la 
        """
        if not new_vector.is_complete() and not self.current_vector.is_complete():
            return
        if self._is_sheep_not_in_screen():
            self.sheep = self.initial_sheep_position
            self.current_vector.clear()
            self.velocity_x = 0
            self.velocity_y = 0
            return
        if not self.current_vector.is_complete() and new_vector.is_complete():
            vec = new_vector.copy()
            intensity = vec.normalize()
            self.current_vector = vec
            speed = min(intensity * 2, 550) / M_FPS
            self.velocity_x = (vec.x2 - vec.x1) * speed
            self.velocity_y = (vec.y2 - vec.y1) * speed - M_GRAVITY / M_FPS

        x, y = self.sheep
        self.velocity_y += M_GRAVITY / M_FPS
        was_falling = self.velocity_y >= 0

        new_x = x + self.velocity_x
        new_y = y + self.velocity_y

        final_x, final_y = self._resolve_collision(x, y, new_x, new_y, was_falling)
        self.sheep = (final_x, final_y)

        if self._sheep_on_ice():
            self.velocity_x *= 0.98
            self.velocity_y = 0  # empêche l'accumulation de gravité quand posé sur la glace (j'avais un bug ou le mouton finissait dans le bloc....)

        if abs(self.velocity_x) < 0.5:
            self.velocity_x = 0

        if self.velocity_x == 0 and self.velocity_y == 0:
            self.current_vector.clear()

    def _simulate_trajectory(self, vx, vy, steps=60):
        """
        Simule la trajectoire du mouton sans le déplacer.
        Retourne une liste de points (x, y) représentant la trajectoire prévue.
        """
        x, y = self.sheep
        points = []

        for _ in range(steps):
            vy += M_GRAVITY / M_FPS
            was_falling = vy >= 0
            new_x = x + vx
            new_y = y + vy

            real_sheep = self.sheep

            self.sheep = (new_x, y)
            if self.sheep_intersect_solid():
                vx *= -0.25
                new_x = x

            self.sheep = (x, new_y)
            if self.sheep_intersect_solid():
                vy = 0
                if was_falling:
                    vx = 0
                new_y = y

            # Restaurer la vraie position
            self.sheep = real_sheep

            x, y = new_x, new_y
            points.append((x, y))

            if vx == 0 and vy == 0:
                break

        return points
    
    def show_trajectory_preview(self, draw_vector):
        """
        Affiche la trajectoire prévue si draw_vector est le vecteur en cours de dessin.
        """
        if draw_vector.is_void() or not draw_vector.is_complete():
            return

        dx = draw_vector.x2 - draw_vector.x1
        dy = draw_vector.y2 - draw_vector.y1
        intensity = (dx**2 + dy**2) ** 0.5
        if intensity == 0:
            return

        speed = min(intensity * 2, 550) / M_FPS
        vx = (dx / intensity) * speed
        vy = (dy / intensity) * speed - M_GRAVITY / M_FPS

        points = self._simulate_trajectory(vx, vy)

        cell_size = M_CELL_SIZE(self.map)
        ox = cell_size // 4 + cell_size // 4
        oy = cell_size // 2 + cell_size // 4

        for i, (x, y) in enumerate(points):
            alpha = 1.0 - (i / len(points))
            if i % 3 == 0:  
                cercle(x + ox, y + oy, 2, couleur="blue", remplissage="blue")

