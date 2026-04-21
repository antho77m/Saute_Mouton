from fltk import *
from cons import *
from map import *
from graphics import *

def main():

    map = Map("res/carte.txt")

    cree_fenetre(M_WIDTH, M_HEIGHT)
    while True:
        mise_a_jour()
        map.showMap()
        map.showSheep()
        attend_ev()  # bloque l'exécution jusqu'à un clic ou une touche
        break
    ferme_fenetre()


if __name__ == "__main__":
    main()

    

