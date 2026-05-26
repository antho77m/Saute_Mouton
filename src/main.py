from random import randint

from fltk import *
from cons import *
from map import *
from graphics import *
from vector import Vector





def main():

    vector = Vector()

    files_maps = ["res/carte.txt", "res/carte2.txt", "res/carte3.txt", "res/carte4.txt", "res/carte5.txt", "res/carte6.txt", "res/carte7.txt"]
    

    rand = randint(0, len(files_maps) - 1)
    print(f"Map choisie : {files_maps[rand]}")

    map = Map(files_maps[rand])

    cree_fenetre(M_WIDTH, M_HEIGHT)
    sleep_fps= sleep_for_fps(M_FPS)

    nb_jump = 0

    while not map.end:
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
            temp = vector.copy()
            temp.set_end(x, y)
            map.show_trajectory_preview(temp)
        
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
            nb_jump += 1
            vector.clear() 
    
    # Affiche un message de fin
    while True:
        mise_a_jour()
        sleep_fps()
        efface_tout()
        texte(M_WIDTH//2, M_HEIGHT//2, f"Félicitations ! Vous avez gagné en {nb_jump} sauts !", couleur="blue", taille=15, ancrage="center")


if __name__ == "__main__":
    main()

    

