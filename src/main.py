from fltk import *
from cons import *
from map import *
from graphics import *
from vector import Vector



def main():

    vector = Vector()

    map = Map("res/carte.txt")

    cree_fenetre(M_WIDTH, M_HEIGHT)
    while True:
        mise_a_jour()
        efface_tout()

        map.showMap()
        map.showSheep()
        if vector.is_complete():
            vector.draw()
        
        if vector.is_void():
            coo = ask_clic()
            if coo is not None:
                vector.set_start(coo[0], coo[1])
        elif not vector.is_complete():
            coo = ask_clic()
            if coo is not None:
                vector.set_end(coo[0], coo[1])
            else: 
                x = abscisse_souris()
                y = ordonnee_souris()
                vector.draw_preview(x, y)
        else:
            map.apply_vec_on_sheep(vector)
            vector.clear()
            pass
    ferme_fenetre()


if __name__ == "__main__":
    main()

    

