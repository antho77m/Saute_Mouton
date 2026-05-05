from fltk import *
from cons import *
from map import *
from graphics import *

def main():

    map = Map("res/carte.txt")

    cree_fenetre(M_WIDTH, M_HEIGHT)
    while True:
        mise_a_jour()
        map.show_map()
        map.show_sheep()
        attend_ev()  # bloque l'exécution jusqu'à un clic ou une touche
    
    ferme_fenetre()


if __name__ == "__main__":
    main()

    

