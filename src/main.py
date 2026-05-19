from fltk import *
from cons import *
from map import *
from graphics import *
from vector import Vector





def main():

    vector = Vector()

    map = Map("res/carte.txt")

    cree_fenetre(M_WIDTH, M_HEIGHT)
    sleep_fps= sleep_for_fps(M_FPS)

    while True:
        mise_a_jour()
        sleep_fps()
        efface_tout()

        map.show_map()
        map.show_sheep()
        if vector.is_complete():
            vector.draw()
        elif not vector.is_void():
            x = abscisse_souris()
            y = ordonnee_souris()
            vector.draw_preview(x, y)
        
        coo = ask_clic()
        if coo is not None:
            print(coo)
            if vector.is_void():
                vector.set_start(coo[0], coo[1])
            elif not vector.is_complete():
                    vector.set_end(coo[0], coo[1])
            else :
                vector.clear()
                
        map.apply_vec_on_sheep(vector)
        if vector.is_complete(): # on clear apres avoir donné le vector à la map pour éviter de réapliquer le même vector plusieurs fois
            vector.clear()
    ferme_fenetre()


if __name__ == "__main__":
    main()

    

